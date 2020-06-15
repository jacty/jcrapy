from Jcrapy.core.downloader.handlers import DownloadHandlers

class Downloader:
    def __init__(self, crawler):
        self.settings = crawler.settings
        self.slots = {}
        self.active = set()
        self.handlers = DownloadHandlers(crawler)
        print('Downloader.__init__')