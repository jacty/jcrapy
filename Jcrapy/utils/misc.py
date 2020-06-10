"""Helper functions which don't fit anywhere else"""
from importlib import import_module
from pkgutil import iter_modules

def walk_modules(path):
    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        #__path__ is a symbol of package
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods
