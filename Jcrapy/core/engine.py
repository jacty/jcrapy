"""
This is the Jcrapy engine which controls the Scheduler, Downloader and Spiders.

For more information see docs/topics/architecture.rst

"""
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
        self.running = False

    def _next_request(self, spider):
        slot = self.slot

        self._next_request_from_scheduler(spider)


        if slot.start_requests:
            try:
                request = next(slot.start_requests)
            except StopIteration as e:
                slot.start_requests = None
            except Exception as e:
                slot.start_requests = None
                print('Error in Engine._next_request')
            else:
                self.crawl(request, spider)

    def _next_request_from_scheduler(self, spider):
        slot = self.slot
        request = slot.scheduler.next_request()
        if not request:
            return
        d = self._download(request, spider)
        print('_next_request_from_scheduler')
    
    def has_capacity(self):
        return not bool(self.slot)

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests=（）, close_if_idle=True):
        if not self.has_capacity():
            raise RuntimeError(f"No free spider slot when opening {spider.name !r}")
        nextcall = CallLaterOnce(self._next_request, spider)
        scheduler = self.scheduler_cls.from_crawler(self.crawler)
        start_requests = yield self.scraper.spidermw.process_start_requests(start_requests, spider)
        self.slot = Slot(start_requests, close_if_idle, nextcall, scheduler)
        self.spider = spider
        yield scheduler.open(spider)
        yield self.scraper.open_spider(spider)
        self.slot.heartbeat.start(5)  
    
    def crawl(self, request, spider):
        self.schedule(request, spider)

    def schedule(self, request, spider):
        self.slot.scheduler.enqueue_request(request)

    def _download(self, request, spider):
        self.slot.add_request(request)

        def _on_success(response):
            print('_on_success')

        def _on_complete(_):
            print('_on_complete')

        dwld = self.downloader.fetch(request, spider)
        # dwld.addCallbacks(_on_success)
        # dwld.addBoth(_on_complete)
        print('_download', dwld)




