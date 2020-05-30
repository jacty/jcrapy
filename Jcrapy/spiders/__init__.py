"""
Base class for Jcrapy spiders

See documentation in docs/topics/spiders.rst
"""


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
        # crawler.signals.connect(self.close, signals.spider_closed)


