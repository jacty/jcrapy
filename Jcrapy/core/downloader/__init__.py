import random
from time import time
from collections import deque

from twisted.internet import defer, task

from Jcrapy.utils.defer import mustbe_deferred
from Jcrapy.utils.httpobj import urlparse_cached
from Jcrapy.core.downloader.middleware import DownloaderMiddlewareManager
from Jcrapy.core.downloader.handlers import DownloadHandlers

class Slot:
    """Downloader slot"""
    def __init__(self, concurrency, delay, randomize_delay):
        self.concurrency = concurrency
        self.delay = delay
        self.randomize_delay = randomize_delay

        self.active = set()
        self.queue = deque()
        self.transferring = set()
        self.lastseen = 0
        self.latercall = None

    def free_transfer_slots(self):
        return self.concurrency - len(self.transferring)

    def download_delay(self):
        if self.randomize_delay:
            return random.uniform(0.5 * self.delay, 1.5 * self.delay)
        return self.delay

def _get_concurrency_delay(concurrency, spider, settings):
    delay = settings.getfloat('DOWNLOAD_DELAY')
    if hasattr(spider, 'download_delay'):
        print('_get_concurrency_delay','download_delay')

    if hasattr(spider, 'max_concurrent_requests'):
        print('_get_concurrency_delay', 'max_concurrent_requests')
    return concurrency, delay



class Downloader:

    DOWNLOAD_SLOT = 'download_slot'

    def __init__(self, crawler):
        self.settings = crawler.settings
        self.slots = {}
        self.active = set()
        self.handlers = DownloadHandlers(crawler)
        self.total_concurrency = self.settings.getint('CONCURRENT_REQUESTS')
        self.domain_concurrency = self.settings.getint('CONCURRENT_REQUESTS_PER_DOMAIN')
        self.ip_concurrency = self.settings.getint('CONCURRENT_REQUESTS_PER_IP')
        self.randomize_delay = self.settings.getbool('RANDOMIZE_DOWNLOAD_DELAY')
        self.middleware = DownloaderMiddlewareManager.from_settings(crawler)
        self._slot_gc_loop = task.LoopingCall(self._slot_gc)
        self._slot_gc_loop.start(60)

    def fetch(self, request, spider):
        def _deactivate(response):
            self.active.remove(request)
            return response

        self.active.add(request)
        dfd = self.middleware.download(self._enqueue_request, request, spider)
        return dfd.addBoth(_deactivate)

    def needs_backout(self):
        return len(self.active) >= self.total_concurrency

    def _get_slot(self, request, spider):
        key = self._get_slot_key(request, spider)
        if key not in self.slots:
            conc = self.ip_concurrency if self.ip_concurrency else self.domain_concurrency
            conc, delay = _get_concurrency_delay(conc, spider, self.settings)
            self.slots[key] = Slot(conc, delay, self.randomize_delay)
        
        return key, self.slots[key]

    def _get_slot_key(self, request, spider):
        if self.DOWNLOAD_SLOT in request.meta:
            return request.meta[self.DOWNLOAD_SLOT]

        key = urlparse_cached(request).hostname or ''
        if self.ip_concurrency:
            key = dnscache.get(key, key)
        return key

    def _enqueue_request(self, request, spider):
        key, slot = self._get_slot(request, spider)
        request.meta[self.DOWNLOAD_SLOT] = key
        def _deactivate(response):
            print('_enqueue_request._deactivate')

        slot.active.add(request)
        deferred = defer.Deferred().addBoth(_deactivate)
        slot.queue.append((request, deferred))
        self._process_queue(spider, slot)
        return deferred
    
    def _process_queue(self, spider, slot):
        from twisted.internet import reactor
        if slot.latercall and slot.latercall.active():
            return 

        now = time()
        delay = slot.download_delay()
        if delay:
            print('_process_queue', not delay)

        while slot.queue and slot.free_transfer_slots() > 0:
            slot.lastseen = now
            request, deferred = slot.queue.popleft()
            dfd = self._download(slot, request, spider)
            dfd.chainDeferred(deferred)
            if delay:
                self._process_queue(spider, slot)
                break

    def _download(self, slot, request, spider):
        dfd = mustbe_deferred(self.handlers.download_request, request, spider)
        
        def _downloaded(response):
            return response
        dfd.addCallback(_downloaded)
        slot.transferring.add(request)
        def finish_transferring(_):
            print('finish_transferring')
            return _
        return dfd.addBoth(finish_transferring)

    def close(self):
        self._slot_gc_loop.stop()
        for slot in self.slots.values():
            slot.close()

    def _slot_gc(self, age=60):
        mintime = time() - age
        for key, slot in list(self.slots.items()):
            print('Downloader._slot_gc', key, slot)
            if not slot.active and slot.lastseen + slot.delay < mintime:
                self.slots.pop(key).close()        
