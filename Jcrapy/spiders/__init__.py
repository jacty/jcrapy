"""
Base class for Jcrapy spiders

See documentation in docs/topics/spiders.rst
"""
# import logging
# import warnings

from Jcrapy import signals
from Jcrapy.http import Request
from Jcrapy.utils.trackref import object_ref
# from scrapy.utils.url import url_is_from_spider

class Spider(object_ref):
    """Base class for scrapy spiders. All spiders must inherit from this
    class.
    """

    name = None
    custom_settings = None

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

#     @property
#     def logger(self):
#         logger = logging.getLogger(self.name)
#         return logging.LoggerAdapter(logger, {'spider': self})

#     def log(self, message, level=logging.DEBUG, **kw):
#         """Log the given message at the given log level

#         This helper wraps a log call to the logger within the spider, but you
#         can use it directly (e.g. Spider.logger.info('msg')) or use any other
#         Python logger too.
#         """
#         self.logger.log(level, message, **kw)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)        
        spider._set_crawler(crawler)
        return spider

    def _set_crawler(self, crawler):
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
            yield Request(url, dont_filter=True)

#     def parse(self, response):
#         raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))

    @classmethod
    def update_settings(cls, settings):
        settings.update(cls.custom_settings or {}, priority='spider')

#     @classmethod
#     def handles_request(cls, request):
#         return url_is_from_spider(request.url, cls)

    @staticmethod
    def close(spider, reason):
        print('Spider.close')
#         closed = getattr(spider, 'closed', None)
#         if callable(closed):
#             return closed(reason)

#     def __str__(self):
#         return "<%s %r at 0x%0x>" % (type(self).__name__, self.name, id(self))

#     __repr__ = __str__


# # Top-level imports
# from scrapy.spiders.crawl import CrawlSpider, Rule  # noqa: F401
# from scrapy.spiders.feed import XMLFeedSpider, CSVFeedSpider  # noqa: F401
# from scrapy.spiders.sitemap import SitemapSpider  # noqa: F401
