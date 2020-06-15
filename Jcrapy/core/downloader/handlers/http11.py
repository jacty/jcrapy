from twisted.internet import reactor
from twisted.web.client import Agent, HTTPConnectionPool

from Jcrapy.core.downloader.tls import openssl_methods
from Jcrapy.utils.misc import create_instance, load_object

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

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)