"""
This is the Jcrapy engine which controls the Scheduler, Downloader and Spiders.

For more information see docs/topics/architecture.rst

"""
from time import time

from twisted.internet import defer, task
from twisted.python.failure import Failure

# from Jcrapy.https import Response, Request
from Jcrapy.utils.misc import load_object
from Jcrapy.core.scraper import Scraper
from Jcrapy.utils.reactor import CallLaterOnce
from Jcrapy.utils.log import failure_to_exc_info

class Slot:

    def __init__(self, start_requests, close_if_idle, nextcall, scheduler):
        self.closing = False
        self.inprogress = set()
        self.start_requests = start_requests
        self.close_if_idle = close_if_idle
        self.nextcall = nextcall
        self.scheduler = scheduler
        self.heartbeat = task.LoopingCall(nextcall.schedule)

    def add_request(self, request):
        self.inprogress.add(request)

    def remove_request(self, request):
        self.inprogress.remove(request)
        self._maybe_fire_closing()

    def close(self):
        self.closing = defer.Deferred() #self.closing turned True
        self._maybe_fire_closing()
        return self.closing

    def _maybe_fire_closing(self):
        if self.closing and not self.inprogress:
            if self.nextcall:
                self.nextcall.cancel()
                if self.heartbeat.running:
                    self.heartbeat.stop()
            self.closing.callback(None)

class ExecutionEngine:

    def __init__(self, crawler, spider_closed_callback):
        self.crawler = crawler
        self.settings = crawler.settings
        ###
        # TD: Log related
        # self.signals = crawler.signals
        # self.logformatter = crawler.logformatter
        ###
        self.slot = None
        self.spider = None
        self.running = False
        self.paused = False
        self.scheduler_cls= load_object(self.settings['SCHEDULER'])
        downloader_cls = load_object(self.settings['DOWNLOADER'])
        self.downloader = downloader_cls(crawler)
        self.scraper = Scraper(crawler)
        self._spider_closed_callback = spider_closed_callback

    @defer.inlineCallbacks
    def start(self):
        """Start the execution engine"""
        if self.running:
            raise RuntimeError("Engine already running")
        self.running = True
        yield defer.Deferred()

    def stop(self):
        print('Engine.stop')
        if not self.running:
            raise RuntimeError('Engine not running')
        self.running = False
        dfd = self._close_all_spiders()
        return dfd

    def close(self):
        print('Engine.close')
        """Close the execution engine gracefully.

        If it has already been started, stop it. In all cases, close all spiders
        and the downloader.
        """
        if self.running:
            return self.stop() 
        elif self.open_spiders:
            return self._close_all_spiders()
        else:
            return defer.succeed(self.downloader.close())       

    def _next_request(self, spider):
        slot = self.slot
        if not slot:
            return 

        if self.paused:
            return

        while not self._needs_backout():
            if not self._next_request_from_scheduler(spider):
                break

        if slot.start_requests and not self._needs_backout():
            try:
                request = next(slot.start_requests)
            except StopIteration:
                slot.start_requests = None
            else:
                self.crawl(request, spider)
        
        if self.spider_is_idle(spider) and slot.close_if_idle:
            self._spider_idle(spider)

    def _needs_backout(self):
        slot = self.slot
        return not self.running \
            or slot.closing \
            or self.downloader.needs_backout() \
            or self.scraper.slot.needs_backout()

    def _next_request_from_scheduler(self, spider):
        slot = self.slot
        # fetch request from queues
        request = slot.scheduler.next_request()
        if not request:
            return
        d = self._download(request, spider)
        d.addBoth(self._handle_downloader_output, request, spider)
        d.addBoth(lambda _: slot.remove_request(request))
        d.addBoth(lambda _: slot.nextcall.schedule())
        return d
    
    def _handle_downloader_output(self, response, request, spider):
        print('_handler_downloader_output', response)  

    def spider_is_idle(self, spider):
        if self.slot.start_requests is not None:
            return False

    @property
    def open_spiders(self):
        return [self.spider] if self.spider else []
    
    def has_capacity(self):
        return not bool(self.slot)

    def crawl(self, request, spider):
        if spider not in self.open_spiders:
            raise RuntimeError("Spider %r not opened when crawling: %s" % (spider.name, request))
        self.schedule(request, spider)
        self.slot.nextcall.schedule()

    def schedule(self, request, spider):
        self.slot.scheduler.enqueue_request(request)

    def download(self, request, spider):
        d = self._download(request, spider)
        d.addBoth(self._downloaded, self.slot, request, spider)
        return d  

    def _downloaded(self, response, slot, request, spider):
        print('engine._downloaded')      

    def _download(self, request, spider):
        slot = self.slot
        slot.add_request(request)

        def _on_success(response):
            print('_on_success')
        def _on_complete(_):
            slot.nextcall.schedule()
            return _

        dwld = self.downloader.fetch(request, spider)
        dwld.addCallbacks(_on_success)
        dwld.addBoth(_on_complete)
        return dwld

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests=(), close_if_idle=True):
        if not self.has_capacity():
            raise RuntimeError("No free spider slot when opening %r" % spider.name)
        nextcall = CallLaterOnce(self._next_request, spider)
        scheduler = self.scheduler_cls.from_crawler(self.crawler)

        start_requests = yield self.scraper.spidermw.process_start_requests(start_requests, spider)

        slot = Slot(start_requests, close_if_idle, nextcall, scheduler)
        self.slot = slot
        self.spider = spider
        yield scheduler.open(spider)
        yield self.scraper.open_spider(spider)
        slot.nextcall.schedule()
        slot.heartbeat.start(5)  
    
    def _spider_idle(self, spider):
        print('Engine._spider_idle')

    def close_spider(self, spider, reason='canceled'):
        """Close (cancel) spider and clear all its outstanding requests"""
        print('Engine.close_spider')
        slot = self.slot
        if slot.closing:
            return slot.closing

        dfd = slot.close()

        def log_failure(msg):
            def errback(failure):
                print(failure)
            return errback

        dfd.addBoth(lambda _: self.downloader.close())
        dfd.addErrback(log_failure('Downloader close failure'))

        dfd.addBoth(lambda _: self.scraper.close_spider(spider))
        dfd.addErrback(log_failure('Scraper close failure'))

        dfd.addBoth(lambda _: slot.scheduler.close(reason))
        dfd.addErrback(log_failure('Scheduler close failure'))

        dfd.addBoth(lambda _: setattr(self, 'slot', None))
        dfd.addErrback(log_failure('Error while unassigning slot'))

        dfd.addBoth(lambda _: setattr(self, 'spider', None))
        dfd.addErrback(log_failure('Error while unassigning spider'))

        dfd.addBoth(lambda _: self._spider_closed_callback(spider))

        return dfd

    def _close_all_spiders(self):
        print('engine._close_all_spiders')
        dfds = [self.close_spider(s, reason='shutdown') for s in self.open_spiders]
        dlist = defer.DeferredList(dfds)
        return dlist
