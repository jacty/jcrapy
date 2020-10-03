import ipaddress
from contextlib import suppress
from time import time
from io import BytesIO
from urllib.parse import urldefrag

from twisted.internet import reactor, defer, protocol, ssl
from twisted.web.client import Agent, HTTPConnectionPool, ResponseDone, ResponseFailed, URI
from twisted.web.http import _DataLoss, PotentialDataLoss

from twisted.web.http_headers import Headers as TxHeaders
from twisted.web.iweb import IBodyProducer, UNKNOWN_LENGTH
from Jcrapy.core.downloader.tls import openssl_methods
from Jcrapy.https import Headers
from Jcrapy.responsetypes import ResponseTypes
from Jcrapy.utils.misc import create_instance, load_object
from Jcrapy.utils.python import to_bytes

class HTTP11DownloadHandler:
    lazy = False

    def __init__(self, settings, crawler=None):
        self._crawler = crawler
        self._pool = HTTPConnectionPool(reactor, persistent=True)
        self._pool.maxPersistentPerHost = settings.getint('CONCURRENT_REQUESTS_PER_DOMAIN')
        self._pool._factory.noisy = False

        self._sslMethod = openssl_methods[settings.get('DOWNLOADER_CLIENT_TLS_METHOD')]
        self._contextFactoryClass = load_object(settings['DOWNLOADER_CLIENTCONTEXTFACTORY'])
        # try method-aware context factory
        try:
            self._contextFactory = create_instance(
                objcls=self._contextFactoryClass,
                settings=settings,
                crawler=crawler,
                method=self._sslMethod,
                )
        except TypeError:
            msg = """ '%s' does not accept `method` argument.""" %(settings['DOWNLOADER_CLIENTCONTEXTFACTORY'])
            print(msg)
        self._default_maxsize = settings.getint('DOWNLOAD_MAXSIZE')
        self._default_warnsize = settings.getint('DOWNLOAD_WARNSIZE')
        self._fail_on_dataloss = settings.getbool('DOWNLOAD_FAIL_ON_DATALOSS')
        self._disconnect_timeout = 1


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def download_request(self, request, spider):
        """Return a deferred for the HTTP download"""
        agent = JcrapyAgent(
            contextFactory=self._contextFactory,
            pool=self._pool,
            maxsize=getattr(spider, 'download_maxsize', self._default_maxsize),
            warnsize=getattr(spider, 'download_warnsize', self._default_warnsize),
            fail_on_dataloss=self._fail_on_dataloss,
            crawler=self._crawler,
        )
        return agent.download_request(request)

class TunnelingAgent(Agent):
    """An agent that uses a L{TunnelingTCP4ClientEndpoint} to make HTTPS
    downloads. It may look strange that we have chosen to subclass Agent and not
    ProxyAgent but consider that after the tunnel is opened the proxy is
    transparent to the client; thus the agent should behave like there is no
    proxy involved.
    """
    def __init__(self, reactor, proxyConf, contextFactory=None, connectTimeout=None, bindAddress=None, pool=None):
        super(TunnelingAgent, self).__init__(reactor, contextFactory, connectTimeout, bindAddress, pool)
        self._proxyConf = proxyConf
        self._contextFactory = contextFactory

class JcrapyAgent:
    _Agent = Agent
    _TunnelingAgent = TunnelingAgent

    def __init__(self, contextFactory=None, connectTimeout=10, bindAddress=None, pool=None,
                 maxsize=0, warnsize=0, fail_on_dataloss=True, crawler=None):
        self._contextFactory = contextFactory
        self._connectTimeout = connectTimeout
        self._bindAddress = bindAddress
        self._pool = pool
        self._maxsize = maxsize
        self._warnsize = warnsize
        self._fail_on_dataloss = fail_on_dataloss
        self._txresponse = None
        self._crawler = crawler

    def _get_agent(self, request, timeout):
        bindaddress = request.meta.get('bindaddress') or self._bindAddress
        proxy = request.meta.get('proxy')

        if proxy:
            print('_get_agent', bool(proxy))

        return self._Agent(
            reactor=reactor,
            contextFactory=self._contextFactory,
            connectTimeout=timeout,
            bindAddress=bindaddress,
            pool=self._pool,
            )

    def download_request(self, request):
        timeout = request.meta.get('download_timeout') or self._connectTimeout
        agent = self._get_agent(request, timeout)

        #request details
        url = urldefrag(request.url)[0]
        method = to_bytes(request.method)
        headers = TxHeaders(request.headers)
        if isinstance(agent, self._TunnelingAgent):
            headers.removeHeader(b'Proxy-Authorization')
        if request.body:
            print('agent.download_request.request.body', request.body)
        else:
            bodyproducer = None

        start_time = time()

        print(1, headers)
        d = agent.request(method, to_bytes(url, encoding='ascii'), headers, bodyproducer)

        # set download latency
        d.addCallback(self._cb_latency, request, start_time)
        # response body is ready to be consumed
        d.addCallback(self._cb_bodyready, request)
        d.addCallback(self._cb_bodydone, request, url)
        print('download_request')
        return
        # check download timeout
        self._timeout_cl = reactor.callLater(timeout, d.cancel)
        d.addBoth(self._cb_timeout, request, url, timeout)
        return d

    def _cb_timeout(self, result, request, url, timeout):
        if self._timeout_cl.active():
            self._timeout_cl.cancel()
            return result
        # if self._txresponse:

        print('_cb_timeout', self._txresponse)

    def _cb_latency(self, result, request, start_time):
        request.meta['download_latency'] = time() - start_time
        return result 

    def _cb_bodyready(self, txresponse, request):
        # deliverBody hangs for responses without body
        print('_cb_bodyready', txresponse)
        return
        if txresponse.length == 0:
            print('_cb_bodyready', txresponse.length)

        maxsize = request.meta.get('download_maxsize', self._maxsize)
        warnsize = request.meta.get('download_warnsize', self._warnsize)
        expected_size = txresponse.length if txresponse.length != UNKNOWN_LENGTH else -1
        fail_on_dataloss = request.meta.get('download_fail_on_dataloss', self._fail_on_dataloss)

        if maxsize and expected_size > maxsize:
            err_msg = 'maxsize reached'
            txresponse._transport._producer.loseConnection()
            raise defer.CancelledError(err_msg)

        def _cancel(_):
            print('_cancel')
            txresponse._transport._producer.abortConnection()

        d = defer.Deferred(_cancel)
        txresponse.deliverBody(
            _ResponseReader(
                finished=d,
                txresponse=txresponse,
                request=request,
                maxsize=maxsize,
                warnsize=warnsize,
                fail_on_dataloss=fail_on_dataloss,
                crawler=self._crawler,
            )
        )
        self._txresponse = txresponse
        return d

    def _cb_bodydone(self, result, request, url):
        print('_cb_bodydone')
        headers = Headers(result["txresponse"].headers.getAllRawHeaders())
        respcls = ResponseTypes().from_args(headers=headers, url=url, body=result["body"])
        response = respcls(
            url=url,
            status=int(result["txresponse"].code),
            headers=headers,
            body=result["body"],
            flags=result["flags"],
            certificate=result["certificate"],
            ip_address=result["ip_address"],
        )
        if result.get("failure"):
            result["failure"].value.response = response
            return result["failure"]
        return response

class _ResponseReader(protocol.Protocol):

    def __init__(self, finished, txresponse, request, maxsize, warnsize, fail_on_dataloss, crawler):
        self._finished = finished
        self._txresponse = txresponse
        self._request = request
        self._bodybuf = BytesIO()
        self._maxsize = maxsize
        self._warnsize = warnsize
        self._fail_on_dataloss = fail_on_dataloss
        self._fail_on_dataloss_warned = False
        self._reached_warnsize = False
        self._bytes_received = 0
        self._certificate = None
        self._ip_address = None
        self._crawler = crawler 

    def _finish_response(self, flags=None, failure=None):
        self._finished.callback({
            "txresponse": self._txresponse,
            "body": self._bodybuf.getvalue(),
            "flags": flags,
            "certificate": self._certificate,
            "ip_address": self._ip_address,
            "failure": failure,
        })

    def connectionMade(self):
        if self._certificate is None:
            with suppress(AttributeError):
                print('connectionMade', self.transport._producer.getPeerCertificate())

        if self._ip_address is None:
            self._ip_address = ipaddress.ip_address(self.transport._producer.getPeer().host)

    def dataReceived(self, bodyBytes):
        # This maybe called several times after cancel was called with buffered data.
        if self._finished.called:
            return

        self._bodybuf.write(bodyBytes)
        self._bytes_received += len(bodyBytes)

        if self._maxsize and self._bytes_received > self._maxsize:
            print('Received bytes larger than download.')
            # Clear buffer earlier to avoid keeping data in memory for a long time.
            self._bodybuf.truncate(0)
            self._finished.cancel()

    def connectionLost(self, reason):
        if self._finished.called:
            return 

        if reason.check(ResponseDone):
            self._finish_response()
            return

        if reason.check(PotentialDataLoss):
            self._finish_response(flags=["partial"])
            return

        if reason.check(ResponseFailed) and any(r.check(_DataLoss) for r in reason.value.reasons):
            if not self._fail_on_dataloss:
                self._finish_response(flags=["dataloss"])
                return

        self._finished.errback(reason)

