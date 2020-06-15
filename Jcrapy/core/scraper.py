
from twisted.internet import defer
from Jcrapy.utils.misc import load_object
from Jcrapy.core.spidermw import SpiderMiddlewareManager


class Scraper:

    def __init__(self, crawler):
        self.slot = None
        self.spidermw = SpiderMiddlewareManager.from_settings(crawler)
        itemproc_cls = load_object(crawler.settings['ITEM_PROCESSOR'])
        self.itemproc = itemproc_cls.from_settings(crawler)
        print('Scraper.__init__')

    @defer.inlineCallbacks
    def open_spider(self, spider):
        """Open the given spider for scraping and allocate resources for it"""
        yield self.itemproc.open_spider(spider)        