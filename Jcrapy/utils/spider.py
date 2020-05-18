import inspect

from Jcrapy.spiders import Spider

def iter_spider_classes(module):
    for obj in vars(module).values():
        if inspect.isclass(obj) and\
            issubclass(obj, Spider) and \
            obj.__module__ == module.__name__ and \
            getattr(obj, 'name', None):
            yield obj
                