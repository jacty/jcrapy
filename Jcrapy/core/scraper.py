from Jcrapy.core.spidermw import SpiderMiddlewareManager

class Scraper:

    def __init__(self, crawler):
        self.spidermw = SpiderMiddlewareManager.from_settings(crawler)