"""
This is the Jcrapy engine which controls the Scheduler, Downloader and Spiders.

For more information see docs/topics/architecture.rst

"""
from time import time

from twisted.internet import defer, task

from Jcrapy.core.scraper import Scraper
from Jcrapy.utils.misc import load_object
from Jcrapy.utils.reactor import CallLaterOnce

class Slot:

    def __init__(self, start_requests, close_if_idle, nextcall):
        self.start_requests = iter(start_requests)
        self.close_if_idle = close_if_idle
        self.nextcall = nextcall
        self.heartbeat = task.LoopingCall(nextcall.schedule)

class ExecutionEngine:

    def __init__(self, crawler, spider_closed_callback):
        self.crawler = crawler
        self._spider_closed_callback = spider_closed_callback
        self.slot = None
        self.running = False
        self.paused = False
        self.scheduler_cls=load_object('Jcrapy.core.scheduler.Scheduler')
        self.scraper = Scraper(crawler)

    @defer.inlineCallbacks
    def start(self):
        """Start the execution engine"""
        if self.running:
            raise RuntimeError("Engine already running")
        self.start_time = time()
        self.running = True
        self._closewait = defer.Deferred()
        yield self._closewait

    def _next_request(self, spider):
        slot = self.slot

        if self.paused:
            return

        if slot.start_requests and not self._needs_backout(spider):
            try:
                request = next(slot.start_requests)
            except StopIteration:
                slot.start_requests = None
            else:
                self.crawl(request, spider)
        
        if self.spider_is_idle(spider) and slot.close_if_idle:
            self._spider_idle(spider)

    def _needs_backout(self, spider):
        slot = self.slot
        return not self.running

    def spider_is_idle(self, spider):
        if self.slot.start_requests is not None:
            return False

    @property
    def open_spiders(self):
        return [self.spider] if self.spider else []
    
    def crawl(self, request, spider):
        if spider not in self.open_spiders:
            raise RuntimeError("Spider %r not opened when crawling: %s" % (spider.name, request))
        self.slot.nextcall.schedule()        

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests=(), close_if_idle=True):
        nextcall = CallLaterOnce(self._next_request, spider)
        scheduler = self.scheduler_cls.from_crawler(self.crawler)
        start_requests = yield self.scraper.spidermw.process_start_requests(start_requests, spider)
        self.slot = Slot(start_requests, close_if_idle, nextcall)
        self.spider = spider
        yield scheduler.open(spider)
        yield self.scraper.open_spider(spider)
        self.slot.nextcall.schedule()
        self.slot.heartbeat.start(5)  
    
    def _spider_idle(self, spider):
        print('_spider_idle')