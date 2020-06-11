"""
Spider Middleware manager

See documentation in docs/topics/spider-middleware.rst
"""
from Jcrapy.utils.conf import build_component_list
from Jcrapy.middleware import MiddlewareManager

class SpiderMiddlewareManager(MiddlewareManager):

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return build_component_list(settings.getwithbase('SPIDER_MIDDLEWARES'))

    def process_start_requests(self, start_requests, spider):
        return self._process_chain('process_start_requests', start_requests, spider)
