from collections import defaultdict

from Jcrapy.utils.misc import walk_modules
from Jcrapy.utils.spider import iter_spider_classes

class SpiderLoader:
    def __init__(self, settings):
        self.spider_modules = settings.getlist('SPIDER_MODULES')
        self._spiders = {}
        self._found = defaultdict(list)
        self._load_all_spiders()

    def _check_name_duplicates(self):
        dupes = []
        for name, locations in self._found.items():
            dupes.extend([
                "  {cls} named {name!r} (in {module})".format(module=mod, cls=cls, name=name)
                for mod, cls in locations
                if len(locations) > 1
            ])

        if dupes:
            dupes_string = "\n\n".join(dupes)
            print("There are several spiders with the same name:\n\n"
                "{}\n\n This can cause unexpected behavior.".format(dupes_string))

    def _load_spiders(self, module):
        for spcls in iter_spider_classes(module):
            self._found[spcls.name].append((module.__name__, spcls.__name__))
            self._spiders[spcls.name] = spcls

    def _load_all_spiders(self):
        for name in self.spider_modules:
            try:
                for module in walk_modules(name):
                    self._load_spiders(module)
            except ImportError:
                    print('Could not load spiders from module {modname}')

        self._check_name_duplicates()

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)
 
    def load(self, spider_name):
        try:
            return self._spiders[spider_name]
        except KeyError:
            raise KeyError("Spider not found: {}".format(spider_name))
