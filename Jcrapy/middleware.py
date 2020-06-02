from collections import defaultdict, deque

from Jcrapy.utils.misc import create_instance, load_object
from Jcrapy.utils.defer import process_chain

class MiddlewareManager:
    """Base class for implementing middleware managers"""

    def __init__(self, *middlewares):
        self.methods = defaultdict(deque)

    @classmethod
    def from_settings(cls, crawler):
        mwlist = ['Jcrapy.spidermiddlewares.httperror.HttpErrorMiddleware']
        middlewares = []
        enabled = []
        for clspath in mwlist:
            mwcls = load_object(clspath)
            mw = create_instance(mwcls, crawler.settings, crawler)
            middlewares.append(mw)
        return cls(*middlewares)

    def _process_chain(self, methodname, obj, *args):
        return process_chain(self.methods[methodname], obj, *args)
