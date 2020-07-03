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

    def _add_middleware(self, mw):
        super(SpiderMiddlewareManager, self)._add_middleware(mw)
        if hasattr(mw, 'process_spider_input'):
            self.methods['process_spider_input'].append(mw.process_spider_input)
        if hasattr(mw, 'process_start_requests'):
            self.methods['process_start_requests'].appendleft(mw.process_start_requests)
        process_spider_output = getattr(mw, 'process_spider_output', None)
        self.methods['process_spider_output'].appendleft(process_spider_output)
        process_spider_exception = getattr(mw, 'process_spider_exception', None)
        self.methods['process_spider_exception'].appendleft(process_spider_exception)        

    def scrape_response(self, scrape_func, response, request, spider):
        print('SpiderMiddlewareManager.scrape_response')

    def process_start_requests(self, start_requests, spider):
        return self._process_chain('process_start_requests', start_requests, spider)
