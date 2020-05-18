"""Helper functions which don't fit anywhere else"""
from importlib import import_module
from pkgutil import iter_modules

def walk_modules(path):
    mods = []
    mod = import_module(path)
    mods .append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods

def load_object(path):

    dot = path.rindex('.')
    module, name = path[:dot], path[dot+1:]
    mod = import_module(module)
    
    obj = getattr(mod, name)
    
    return obj
