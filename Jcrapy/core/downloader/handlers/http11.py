from time import time
from urllib.parse import urldefrag

from twisted.internet import reactor
from twisted.web.client import Agent, HTTPConnectionPool

from twisted.web.http_headers import Headers as TxHeaders
from Jcrapy.core.downloader.tls import openssl_methods
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
        from twisted.internet import reactor
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
        from twisted.internet import reactor
        timeout = request.meta.get('download_timeout') or self._connectTimeout
        agent = self._get_agent(request, timeout)

        #request details
        url = urldefrag(request.url)[0]
        method = to_bytes(request.method)
        headers = TxHeaders(request.headers)
        if isinstance(agent, self._TunnelingAgent):
            print('download_request')

        if request.body:
            print('agent.download_request.request.body', request.body)
        else:
            bodyproducer = None
        start_time = time()
        d = agent.request(method, to_bytes(url, encoding='ascii'), headers, bodyproducer)
        # set download latency
        d.addCallback(self._cb_latency, request, start_time)
        # response body is ready to be consumed
        d.addCallback(self._cb_bodyready, request)
        d.addCallback(self._cb_bodydone, request, url)
        # check download timeout
        self._timeout_cl = reactor.callLater(timeout, d.cancel)
        d.addBoth(self._cb_timeout, request, url, timeout)
        return d

    def _cb_timeout(self, result, request, url, timeout):
        print('_cb_timeout')

    def _cb_latency(self, result, request, start_time):
        request.meta['download_latency'] = time() - start_time
        return result 

    def _cb_bodyready(self, txresponse, request):
        # deliverBody hangs for responses without body
        print('_cb_bodyready', txresponse)

    def _cb_bodydone(self, result, request, url):
        print('_cb_bodydone', result)