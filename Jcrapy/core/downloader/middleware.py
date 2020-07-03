from twisted.internet import defer

from Jcrapy.middleware import MiddlewareManager
from Jcrapy.utils.defer import mustbe_deferred
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
                print('DownloaderMiddlewareManager.process_request', method)
            return (yield download_func(request=request, spider=spider))

        @defer.inlineCallbacks
        def process_response(response):
            print('DownloaderMiddlewareManager.process_response')
            return response

        @defer.inlineCallbacks
        def process_exception(failure):
            print('DOWNLOADER_MIDDLEWARES.process_exception')

        deferred = mustbe_deferred(process_request, request)
        # deferred.addErrback(process_exception)
        # deferred.addCallback(process_response)
        return deferred