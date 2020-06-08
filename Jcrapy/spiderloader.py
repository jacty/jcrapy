
from Jcrapy.utils.misc import walk_modules
from Jcrapy.utils.spider import iter_spider_classes

class SpiderLoader:
    def __init__(self, settings):
        self.spider_modules = settings.get('SPIDER_MODULES')
        self._spiders = {}
        self._load_all_spiders()

    def _load_spiders(self, module):
        for spcls in iter_spider_classes(module):
            self._spiders[spcls.name] = spcls

    def _load_all_spiders(self):
        for name in self.spider_modules:
            try:
                for module in walk_modules(name):
                    self._load_spiders(module)
            except ImportError:
                    print('Could not load spiders from module {modname}')
        
    def load(self, spider_name):
        try:
            return self._spiders[spider_name]
        except KeyError:
            raise KeyError("Spider not found: {}".format(spider_name))
