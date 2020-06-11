"""
Item pipeline
"""
from Jcrapy.middleware import MiddlewareManager
from Jcrapy.utils.conf import build_component_list

class ItemPipelineManager(MiddlewareManager):
    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return build_component_list(settings.getwithbase('ITEM_PIPELINES'))