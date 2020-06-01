"""
Base class for Jcrapy spiders

See documentation in docs/topics/spiders.rst
"""

from Jcrapy import signals
from Jcrapy.https import Request

class Spider:
    """Base class for Jcrapy spiders. All spiders must inherit from this
    class.
    """    
    name = None
    custom_settings = None

    def __init__(self):
        #get spider name
        self.name = getattr(self, 'name')

    @classmethod
    def from_crawler(cls, crawler):
        spider = cls()
        spider._set_crawler(crawler)
        return spider

    def _set_crawler(self,crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        crawler.signals.connect(self.close, signals.spider_closed)

    def start_requests(self):
        cls = self.__class__
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            yield Request(url)

    @staticmethod
    def close(spider, reason):
        print('Spider.close')


