"""
Base class for Jcrapy spiders

See documentation in docs/topics/spiders.rst
"""

from Jcrapy.https import Request

class Spider:
    """Base class for Jcrapy spiders. All spiders must inherit from this
    class.
    """    
    def __init__(self):
        #get spider name
        self.name = getattr(self, 'name')

        #self.crawler and self.settings will be set in self._set_crawler
    @classmethod
    def from_crawler(cls, crawler):
        spider = cls()
        spider._set_crawler(crawler)
        return spider

    def _set_crawler(self,crawler):
        self.crawler = crawler
        self.settings = crawler.settings

    def start_requests(self):
        cls = self.__class__
        for url in self.start_urls:
            yield Request(url)

    @staticmethod
    def close(spider, reason):
        print('Spider.close')


