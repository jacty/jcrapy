from time import time
from twisted.internet import defer, task

from Jcrapy.core.downloader.middleware import DownloaderMiddlewareManager
from Jcrapy.core.downloader.handlers import DownloadHandlers

class Downloader:
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
