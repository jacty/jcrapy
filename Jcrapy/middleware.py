from collections import defaultdict, deque

from Jcrapy.utils.misc import create_instance, load_object
from Jcrapy.utils.defer import process_parallel, process_chain

class MiddlewareManager:
    """Base class for implementing middleware managers"""

    def __init__(self, *middlewares):
        self.middlewares = middlewares
        self.methods = defaultdict(deque)
        for mw in middlewares:
            self._add_middleware(mw)

    @classmethod
    def from_settings(cls, crawler):
        #get all the components removing None value ones.
        mwlist = cls._get_mwlist_from_settings(crawler.settings)
        middlewares = []
        for clspath in mwlist:
            try:
                mwcls = load_object(clspath)
                mw = create_instance(mwcls, crawler.settings, crawler)
                middlewares.append(mw)
            except:
                print('Error in middleware.from_settings', clspath)
        return cls(*middlewares)

    def _add_middleware(self, mw):
        if hasattr(mw, 'open_spider'):
            self.methods['open_spider'].append(mw.open_spider)
        if hasattr(mw, 'close_spider'):
            self.methods['close_spider'].appendleft(mw.close_spider)

    def _process_chain(self, methodname, obj, *args):
        return process_chain(self.methods[methodname], obj, *args)

    def open_spider(self, spider):
        return process_parallel(self.methods['open_spider'], spider)

    def close_spider(self, spider):
        return process_parallel(self.methods['close_spider'], spider)
