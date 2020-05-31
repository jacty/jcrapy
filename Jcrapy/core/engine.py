"""
This is the Jcrapy engine which controls the Scheduler, Downloader and Spiders.

For more information see docs/topics/architecture.rst

"""
import logging
# from Jcrapy.core.scheduler import Scheduler
from Jcrapy.utils.reactor import CallLaterOnce

logger = logging.getLogger(__name__)

class ExecutionEngine:

    def __init__(self, crawler, spider_closed_callback):
        self.crawler = crawler
        self._spider_closed_callback = spider_closed_callback
        self.slot = None
        # self.scheduler_cls=Scheduler

    def _next_request(self, spider):
        slot = self.slot
        print('ExecutionEngine._next_request')

    def has_capacity(self):
        """Does the engine have capacity to handle more spiders"""
        return not bool(self.slot)

    def open_spider(self, spider, start_requests=()):
        if not self.has_capacity():
            raise RuntimeError("No free spider slot when opening %r" % spider.name)
        nextcall = CallLaterOnce(self._next_request, spider)
        # scheduler = self.scheduler_cls.from_crawler(self.crawler)
        print('ExecutionEngine.open_spider')  
              
