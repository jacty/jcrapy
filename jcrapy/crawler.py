import logging

from twisted.internet import defer
from zope.interface.exceptions import DoesNotImplement

try:
    # zope >= 5.0 only supports MultipleInvalid
    from zope.interface.exceptions import MultipleInvalid
except ImportError:
    MultipleInvalid = None

from zope.interface.verify import verifyClass

from interfaces import ISpiderLoader
from utils.misc import load_object

logger = logging.getLogger(__name__)

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
        print('CrawlerRunner.crawl')

    def _crawl(self, crawler, *args, **kwargs):
        print('CrawlerRunner._crawl')
        def _done(result):
            print('CrawlerRunner._crawl._done')

    def create_crawler(self, crawler_or_spidercls):
        print('CrawlerRunner.create_crawler')

    def _create_crawler(self, spidercls):
        print('CrawlerRunner._create_crawler')

    def stop(self):
        print('CrawlerRunner.stop')

    @defer.inlineCallbacks
    def join(self):
        print('CrawlerRunner.join')

    def _handle_twisted_reactor(self):
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
        print('CrawlerProcess.__init__')
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
