"""
Spider Middleware manager

See documentation in docs/topics/spider-middleware.rst
"""
from Jcrapy.middleware import MiddlewareManager

class SpiderMiddlewareManager(MiddlewareManager):

    def process_start_requests(self, start_requests, spider):
        return self._process_chain('process_start_requests', start_requests, spider)
