"""
This is the Jcrapy engine which controls the Scheduler, Downloader and Spiders.

For more information see docs/topics/architecture.rst

"""
from twisted.internet import defer, task

from Jcrapy.core.scraper import Scraper
from Jcrapy.utils.misc import load_object
from Jcrapy.utils.reactor import CallLaterOnce

class Slot:

    def __init__(self, start_requests, close_if_idle, nextcall):
        self.nextcall = nextcall
        self.heartbeat = task.LoopingCall(nextcall.schedule)

class ExecutionEngine:

    def __init__(self, crawler, spider_closed_callback):
        self.crawler = crawler
        self._spider_closed_callback = spider_closed_callback
        self.slot = None
        self.scheduler_cls=load_object('Jcrapy.core.scheduler.Scheduler')
        self.scraper = Scraper(crawler)

    def _next_request(self, spider):
        slot = self.slot
        print('ExecutionEngine._next_request')

    def has_capacity(self):
        """Does the engine have capacity to handle more spiders"""
        return not bool(self.slot)

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests=(), close_if_idle=True):
        if not self.has_capacity():
            raise RuntimeError("No free spider slot when opening %r" % spider.name)
        nextcall = CallLaterOnce(self._next_request, spider)
        # scheduler = self.scheduler_cls.from_crawler(self.crawler)
        start_requests = yield self.scraper.spidermw.process_start_requests(start_requests, spider)
        self.slot = Slot(start_requests, close_if_idle, nextcall)
        self.spider = spider
        # yield scheduler.open(spider)
        yield self.scraper.open_spider(spider)
        self.slot.nextcall.schedule()
        self.slot.heartbeat.start(5)  
              
