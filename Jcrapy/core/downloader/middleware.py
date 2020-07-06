from twisted.internet import defer

from Jcrapy.exceptions import _InvalidOutput
from Jcrapy.https import Request, Response
from Jcrapy.middleware import MiddlewareManager
from Jcrapy.utils.defer import mustbe_deferred, deferred_from_coro
from Jcrapy.utils.conf import build_component_list

class DownloaderMiddlewareManager(MiddlewareManager):

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return build_component_list(settings.getwithbase('DOWNLOADER_MIDDLEWARES'))

    def _add_middleware(self, mw):
        if hasattr(mw, 'process_request'):
            self.methods['process_request'].append(mw.process_request)
        if hasattr(mw, 'process_response'):
            print('DownloaderMiddlewareManager._add_middleware')
        if hasattr(mw, 'process_exception'):
            print('DownloaderMiddlewareManager._add_middleware')

    def download(self, download_func, request, spider):
        @defer.inlineCallbacks
        def process_request(request):
            for method in self.methods['process_request']:
                response = yield deferred_from_coro(method(request=request,spider=spider))
                if response is not None and not isinstance(response, (Response, Request)):
                    raise _InvalidOutput(
                        "Middleware %s.process_request must return None, Response or Request, got %s" % (method.__self.__.__class__.__name__, response.__class__.__name__)
                        )
                if response:
                    return response
            return (yield download_func(request=request, spider=spider))

        @defer.inlineCallbacks
        def process_response(response):
            print('DownloaderMiddlewareManager.process_response')
            return response

        @defer.inlineCallbacks
        def process_exception(failure):
            exception = failure.value
            for method in self.methods['process_exception']:
                response = yield deferred_from_coro(method(request=request, exc=exception, spider=spider))
                if response is not None and not isinstance(response, (Response, Request)):
                    raise _InvalidOutput("Middleware %s.process_exception must return None, Response or Request, got %s") % (method.__self__.__class__.__name__, type(response))
                if response:
                    return response
            return failure

        deferred = mustbe_deferred(process_request, request)
        deferred.addErrback(process_exception)
        deferred.addCallback(process_response)
        return deferred