from twisted.internet import defer, reactor

from Jcrapy import Spider
from Jcrapy.spiderloader import SpiderLoader
# from Jcrapy.core.engine import ExecutionEngine
from Jcrapy.signalmanager import SignalManager

from Jcrapy.utils.ossignal import install_shutdown_handlers

class Crawler:

    def __init__(self, spidercls, settings=None):
        self.spidercls = spidercls
        self.settings = settings
        self.signals = SignalManager(self)
        self.crawling = False

    @defer.inlineCallbacks
    def crawl(self, *args):
        #initiate spiderclass from crawler
        self.spider = self.spidercls.from_crawler(self)
        self.engine = ExecutionEngine(self, lambda _: self.stop())
        start_requests = self.spider.start_requests()
        yield self.engine.open_spider(self.spider, start_requests)
        yield defer.maybeDeferred(self.engine.start)

    @defer.inlineCallbacks
    def stop(self):
        """Starts a graceful stop of the crawler and returns a deferred that is
        fired when the crawler is stopped."""
        if self.crawling:
            self.crawling = False
            yield defer.maybeDeferred(self.engine.stop)        
        

class CrawlerRunner:
    """
    This is a convenient helper class that keeps track of, manages and runs
    crawlers inside an already setup :mod:`~twisted.internet.reactor`.

    The CrawlerRunner object must be instantiated with a
    :class:`~Jcrapy.settings.Settings` object.

    This class shouldn't be needed (since Jcrapy is responsible of using it
    accordingly) unless writing scripts that manually handle the crawling
    process. See :ref:`run-from-script` for an example.
    """

    crawlers = property(
        lambda self: self._crawlers
    )

    def __init__(self, settings=None):
        self.settings = settings
        self.spider_loader = SpiderLoader(settings)
        print('CrawlerRunner.__init__', settings)
        return
        self._crawlers = set()
        self._active = set()
        self.bootstrap_failed = False
        self._handle_twisted_reactor()

    def crawl(self, spidername):
        """
        Run a crawler with the provided arguments.

        It will call the given Crawler's :meth:`~Crawler.crawl` method, while
        keeping track of it so it can be stopped later.
        
        """               
        spidercls = self.spider_loader.load(spidername)
        crawler = Crawler(spidercls, self.settings)
        return self._crawl(crawler)

    def _crawl(self, crawler):
        self._crawlers.add(crawler)
        d = crawler.crawl()
        self._active.add(d)
        
        def _done(result):
            self.crawlers.discard(crawler)
            self._active.discard(d)
            self.bootstrap_failed |= not getattr(crawler, 'spider', None)
            return result

        return d.addBoth(_done)

    def stop(self):
        return defer.DeferredList([c.stop() for c in list(self.crawlers)])

    @defer.inlineCallbacks
    def join(self):
        """
        join()

        Returns a deferred that is fired when all managed :attr:`crawlers` have
        completed their executions.
        """
        while self._active:
            yield defer.DeferredList(self._active)
        
    def _handle_twisted_reactor(self):
        pass


class CrawlerProcess(CrawlerRunner):
    """
    A class to run multiple Jcrapy crawlers in a process simultaneously.

    This class extends :class:`~Jcrapy.crawler.CrawlerRunner` by adding support
    for starting a :mod:`~twisted.internet.reactor` and handling shutdown
    signals, like the keyboard interrupt command Ctrl-C. It also configures
    top-level logging.

    This utility should be a better fit than
    :class:`~Jcrapy.crawler.CrawlerRunner` if you aren't running another
    :mod:`~twisted.internet.reactor` within your application.

    The CrawlerProcess object must be instantiated with a
    :class:`~Jcrapy.settings.Settings` object.

    :param install_root_handler: whether to install root logging handler
        (default: True)

    This class shouldn't be needed (since Jcrapy is responsible of using it
    accordingly) unless writing scripts that manually handle the crawling
    process. See :ref:`run-from-script` for an example.
    """

    def __init__(self, settings=None, install_root_handler=True):
        super(CrawlerProcess, self).__init__(settings)
        print('CrawlerProcess.__init__')
        return
        install_shutdown_handlers(self._signal_shutdown)

    def _signal_shutdown(self, signum, _):
        print('CrawlerProcess._signal_shutdown')

    def start(self):
        """
        This method starts a :mod:`~twisted.internet.reactor`, adjusts its pool
        size to :setting:`REACTOR_THREADPOOL_MAXSIZE`, and installs a DNS cache
        based on :setting:`DNSCACHE_ENABLED` and :setting:`DNSCACHE_SIZE`.

        If ``stop_after_crawl`` is True, the reactor will be stopped after all
        crawlers have finished, using :meth:`join`.

        :param boolean stop_after_crawl: stop or not the reactor when all
            crawlers have finished
        """  
        d = self.join() 
        if d.called:
            return
        d.addBoth(self._stop_reactor)
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run(installSignalHandlers=False) #blocking call     

    def _stop_reactor(self):
        print('_stop_reactor')

    def _handle_twisted_reactor(self):
        super()._handle_twisted_reactor()