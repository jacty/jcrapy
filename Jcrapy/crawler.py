from Jcrapy import Spider
from Jcrapy.spiderloader import SpiderLoader
from Jcrapy.signalmanager import SignalManager

class Crawler:

    def __init__(self, spidercls, settings=None):
        self.spidercls = spidercls
        self.settings = settings
        self.signals = SignalManager(self)

    def crawl(self, *args):
        #initiate spiderclass from crawler
        self.spider = self.spidercls.from_crawler(self)
        print('Crawler.crawl')
        

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
    def _get_spider_loader(self,settings):        
        return SpiderLoader(settings.frozencopy())

    def __init__(self, settings=None):
        self.settings = settings
        self.spider_loader = self._get_spider_loader(settings)
        self._crawlers = set()
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
        print('CrawlerRunner._crawl',crawler)
        
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

    def _signal_shutdown(self, signum, _):
        print('CrawlerProcess._signal_shutdown')

    def _handle_twisted_reactor(self):
        super()._handle_twisted_reactor()