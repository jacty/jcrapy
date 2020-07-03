"""
Item pipeline
"""
from Jcrapy.middleware import MiddlewareManager
from Jcrapy.utils.conf import build_component_list
from Jcrapy.utils.defer import deferred_f_from_coro_f

class ItemPipelineManager(MiddlewareManager):
    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return build_component_list(settings.getwithbase('ITEM_PIPELINES'))

    def _add_middleware(self, pipe):
        super(ItemPipelineManager, self)._add_middleware(pipe)
        if hasattr(pipe, 'process_item'):
            self.methods['process_item'].append(deferred_f_from_coro_f(pipe.process_item))

    def process_item(self, item, spider):
        print('ItemPipelineManager.process_item')