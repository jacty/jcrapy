from twisted.internet import defer

from Jcrapy.middleware import MiddlewareManager
from Jcrapy.utils.defer import mustbe_deferred
from Jcrapy.utils.conf import build_component_list

class DownloaderMiddlewareManager(MiddlewareManager):

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return build_component_list(settings.getwithbase('DOWNLOADER_MIDDLEWARES'))

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

        deferred = mustbe_deferred(process_request, request)
        deferred.addCallback(process_response)
        return deferred