import logging
import pprint
import signal
import warnings

from twisted.internet import defer
from zope.interface.exceptions import DoesNotImplement

try:
    # zope >= 5.0 only supports MultipleInvalid
    from zope.interface.exceptions import MultipleInvalid
except ImportError:
    MultipleInvalid = None

from zope.interface.verify import verifyClass

from jcrapy import signals, Spider
from jcrapy.core.engine import ExecutionEngine
from jcrapy.exceptions import ScrapyDeprecationWarning
from jcrapy.interfaces import ISpiderLoader
from jcrapy.settings import overridden_settings
from jcrapy.signalmanager import SignalManager
from jcrapy.utils.log import(
    configure_logging,
    get_scrapy_root_handler,
    install_scrapy_root_handler,
    log_scrapy_info,
    LogCounterHandler,
)
from jcrapy.utils.misc import load_object
from jcrapy.utils.ossignal import install_shutdown_handlers

logger = logging.getLogger(__name__)

class Crawler:
    
    def __init__(self, spidercls, settings=None):
        if isinstance(spidercls, Spider):
            raise ValueError('The spidercls argument must be a class, not an object')

        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)

        self.spidercls = spidercls
        self.settings = settings.copy()
        self.spidercls.update_settings(self.settings)

        self.signals = SignalManager(self)
        self.stats = load_object(self.settings['STATS_CLASS'])(self)

        handler = LogCounterHandler(self, level=self.settings.get('LOG_LEVEL'))
        logging.root.addHandler(handler)

        d = dict(overridden_settings(self.settings))
        # logger.info("Overridden settings:\n%(settings)s",
        #             {'settings': pprint.pformat(d)})
        if get_scrapy_root_handler() is not None:
            # scrapy root handler already installed: update it with new settings
            install_scrapy_root_handler(self.settings)
        # lambda is assigned to Crawler attribute because this way it is not
        # garbage collected after leaving __init__ scope
        self.__remove_handler = lambda: logging.root.removeHandler(handler)
        self.signals.connect(self.__remove_handler, signals.engine_stopped)

        # lf_cls = load_object(self.settings['LOG_FORMATTER'])
        # self.logformatter = lf_cls.from_crawler(self)
        # self.extensions = ExtensionManager.from_crawler(self)

        self.settings.freeze()
        self.crawling = False
        self.spider = None
        self.engine = None

    # @defer.inlineCallbacks
    def crawl(self, *args, **kwargs):
        assert not self.crawling, 'Crawling already taking place'
        self.crawling = True

        self.spider = self._create_spider(*args, **kwargs)
        self.engine = self._create_engine()
        print('crawl', *args, kwargs)

    def _create_spider(self, *args, **kwargs):
        return self.spidercls.from_crawler(self, *args, **kwargs)

    def _create_engine(self):
        return ExecutionEngine(self, lambda _: self.stop())

     
class CrawlerRunner:
    """
    This is a convenient helper class that keeps track of, manages and runs
    crawlers inside an already setup :mod:`~twisted.internet.reactor`.

    The CrawlerRunner object must be instantiated with a
    :class:`~scrapy.settings.Settings` object.

    This class shouldn't be needed (since Scrapy is responsible of using it
    accordingly) unless writing scripts that manually handle the crawling
    process. See :ref:`run-from-script` for an example.
    """
    crawlers = property(
        lambda self: self._crawlers,
        doc="Set of :class:`crawlers <scrapy.crawler.Crawler>` started by "
            ":meth:`crawl` and managed by this class."
    )

    @staticmethod
    def _get_spider_loader(settings):
        """ Get SpiderLoader instance from settings """
        cls_path = settings.get('SPIDER_LOADER_CLASS')
        loader_cls = load_object(cls_path)
        excs = (DoesNotImplement, MultipleInvalid) if MultipleInvalid else DoesNotImplement

        try:
            verifyClass(ISpiderLoader, loader_cls)
        except excs:
            warnings.warn(
                'SPIDER_LOADER_CLASS (previously named SPIDER_MANAGER_CLASS) does '
                'not fully implement scrapy.interfaces.ISpiderLoader interface. '
                'Please add all missing methods to avoid unexpected runtime errors.',
                category=ScrapyDeprecationWarning, stacklevel=2
            )

        return loader_cls.from_settings(settings.frozencopy())

    def __init__(self, settings=None):
        if isinstance(settings, dict) or settings is None:
            print('CrawlerRunner', isinstance(settings, dict))
        self.settings = settings
        self.spider_loader = self._get_spider_loader(settings)
        self._crawlers = set()
        self._active = set()
        self.bootstrap_failed = False
        self._handle_twisted_reactor()

    @property
    def spider(self):
        print('CrawlerRunner.spider')

    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        """
        Run a crawler with the provided arguments.

        It will call the given Crawler's :meth:`~Crawler.crawl` method, while
        keeping track of it so it can be stopped later.

        If ``crawler_or_spidercls`` isn't a :class:`~scrapy.crawler.Crawler`
        instance, this method will try to create one using this parameter as
        the spider class given to it.

        Returns a deferred that is fired when the crawling is finished.

        :param crawler_or_spidercls: already created crawler, or a spider class
            or spider's name inside the project to create it
        :type crawler_or_spidercls: :class:`~scrapy.crawler.Crawler` instance,
            :class:`~scrapy.spiders.Spider` subclass or string

        :param list args: arguments to initialize the spider

        :param dict kwargs: keyword arguments to initialize the spider
        """
        if isinstance(crawler_or_spidercls, Spider):
            raise ValueError(
                'The crawler_or_spidercls argument cannot be a spider object, '
                'it must be a spider class (or a Crawler object)')
        crawler = self.create_crawler(crawler_or_spidercls)
        return self._crawl(crawler, *args, **kwargs)

    def _crawl(self, crawler, *args, **kwargs):
        self.crawlers.add(crawler)
        d = crawler.crawl(*args, **kwargs)
        print('CrawlerRunner._crawl', crawler)
        def _done(result):
            print('CrawlerRunner._crawl._done')

    def create_crawler(self, crawler_or_spidercls):
        """
        Return a :class:`~scrapy.crawler.Crawler` object.

        * If ``crawler_or_spidercls`` is a Crawler, it is returned as-is.
        * If ``crawler_or_spidercls`` is a Spider subclass, a new Crawler
          is constructed for it.
        * If ``crawler_or_spidercls`` is a string, this function finds
          a spider with this name in a Scrapy project (using spider loader),
          then creates a Crawler instance for it.
        """
        if isinstance(crawler_or_spidercls, Spider):
            raise ValueError(
                'The crawler_or_spidercls argument cannot be a spider object, '
                'it must be a spider class (or a Crawler object)')        
        if isinstance(crawler_or_spidercls, Crawler):
            print('CrawlerRunner.create_crawler')
        return self._create_crawler(crawler_or_spidercls)

    def _create_crawler(self, spidercls):
        if isinstance(spidercls, str):
            spidercls = self.spider_loader.load(spidercls)
        return Crawler(spidercls, self.settings)

    def stop(self):
        print('CrawlerRunner.stop')

    @defer.inlineCallbacks
    def join(self):
        print('CrawlerRunner.join')

    def _handle_twisted_reactor(self):
        if self.settings.get("TWISTED_REACTOR"):
            print('CrawlerRunner._handle_twisted_reactor')


class CrawlerProcess(CrawlerRunner):
    """
    A class to run multiple scrapy crawlers in a process simultaneously.

    This class extends :class:`~scrapy.crawler.CrawlerRunner` by adding support
    for starting a :mod:`~twisted.internet.reactor` and handling shutdown
    signals, like the keyboard interrupt command Ctrl-C. It also configures
    top-level logging.

    This utility should be a better fit than
    :class:`~scrapy.crawler.CrawlerRunner` if you aren't running another
    :mod:`~twisted.internet.reactor` within your application.

    The CrawlerProcess object must be instantiated with a
    :class:`~scrapy.settings.Settings` object.

    :param install_root_handler: whether to install root logging handler
        (default: True)

    This class shouldn't be needed (since Scrapy is responsible of using it
    accordingly) unless writing scripts that manually handle the crawling
    process. See :ref:`run-from-script` for an example.
    """

    def __init__(self, settings=None, install_root_handler=True):
        super(CrawlerProcess, self).__init__(settings)
        install_shutdown_handlers(self._signal_shutdown)
        configure_logging(self.settings, install_root_handler)
        # log_scrapy_info(self.settings)
        
    def _signal_shutdown(self, signum, _):
        print('CrawlerProcess._signal_shutdown')

    def _signal_kill(self, signum, _):
        print('CrawlerProcess._signal_kill')

    def start(self, stop_after_crawl=True):
        print('CrawlerProcess.start')

    def _graceful_stop_reactor(self):
        print('CrawlerProcess._graceful_stop_reactor')

    def _stop_reactor(self, _=None):
        print('CrawlerProcess._stop_reactor')

    def _handle_twisted_reactor(self):
        if self.settings.get("TWISTED_REACTOR"):
            print('CrawlerProcess._handle_twisted_reactor')
        super()._handle_twisted_reactor()
