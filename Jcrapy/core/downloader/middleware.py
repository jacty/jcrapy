from Jcrapy.middleware import MiddlewareManager
from Jcrapy.utils.conf import build_component_list

class DownloaderMiddlewareManager(MiddlewareManager):

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return build_component_list(settings.getwithbase('DOWNLOADER_MIDDLEWARES'))