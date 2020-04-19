# -*- coding: utf-8 -*-
from collections import defaultdict

from zope.interface import implementer
from interfaces import ISpiderLoader

@implementer(ISpiderLoader)
class SpiderLoader:
    """
    SpiderLoader is a class which locates and loads spiders
    in a Scrapy project.
    """
    def __init__(self, settings):
        self.spider_modules = settings.getlist('SPIDER_MODULES')
        self.warn_only = settings.getbool('SPIDER_LOADER_WARN_ONLY')
        self._spiders = {}
        self._found = defaultdict(list)
        self._load_all_spiders()

    def _check_name_duplicates(self):
        for name, locations in self._found.items():
            print('SpiderLoader._check_name_duplicates', name, locations)

    def _load_spiders(self, module):
        print('SpiderLoader._load_spiders')

    def _load_all_spiders(self):
        for name in self.spider_modules:
            print('SpiderLoader._load_all_spiders', name)
        self._check_name_duplicates()

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def load(self, spider_name):
        print('SpiderLoader.load')

    def find_by_request(self, request):
        print('SpiderLoader.find_by_request')

    def list(self):
        print('SpiderLoader.list')

