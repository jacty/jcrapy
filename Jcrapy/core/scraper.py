from collections import deque

from twisted.internet import defer
from Jcrapy.utils.misc import load_object
from Jcrapy.core.spidermw import SpiderMiddlewareManager

class Slot:

    def __init__(self, max_active_size=5000000):
        self.max_active_size = max_active_size
        self.queue = deque()
        self.active = set()
        self.active_size = 0
        self.itemproc_size = 0
        self.closing = None

    def is_idle(self):
        return not (self.queue or self.active)

class Scraper:

    def __init__(self, crawler):
        self.slot = None
        self.spidermw = SpiderMiddlewareManager.from_settings(crawler)
        itemproc_cls = load_object(crawler.settings['ITEM_PROCESSOR'])
        self.itemproc = itemproc_cls.from_settings(crawler)
        self.concurrent_items = crawler.settings.getint('CONCURRENT_ITEMS')
        self.crawler = crawler

    @defer.inlineCallbacks
    def open_spider(self, spider):
        """Open the given spider for scraping and allocate resources for it"""
        self.slot = Slot(self.crawler.settings.getint('SCRAPER_SLOT_MAX_ACTIVE_SIZE'))
        yield self.itemproc.open_spider(spider)

    def close_spider(self, spider):
        """Close a spider being scraped and release its resources"""
        slot = self.slot
        slot.closing = defer.Deferred()
        slot.closing.addCallback(self.itemproc.close_spider)
        self._check_if_closing(spider, slot)
        return slot.closing 

    def _check_if_closing(self, spider, slot):
        if slot.closing and slot.is_idle():
            slot.closing.callback(spider)           