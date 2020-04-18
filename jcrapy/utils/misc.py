"""Helper functions which don't fit anywhere else"""
from importlib import import_module
from pkgutil import iter_modules

# _ITERABLE_SINGLE_VALUES = dict, BaseItem, str, bytes

def load_object(path):
    """Load an object given its absolute object path, and return it.

    object can be the import path of a class, function, variable or an
    instance, e.g. 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """
    print('load_object', path)    

def walk_modules(path):
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For example: walk_modules('scrapy.utils')
    """
    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                print('ispkg=true')
                # mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)    
    return mods