"""Helper functions which don't fit anywhere else"""
from importlib import import_module
from pkgutil import iter_modules

# _ITERABLE_SINGLE_VALUES = dict, BaseItem, str, bytes

def load_object(path):
    """Load an object given its absolute object path, and return it.

    object can be the import path of a class, function, variable or an
    instance, e.g. 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module) 

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))
        
    return obj

def walk_modules(path):
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For example: walk_modules('jcrapy.utils')
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

def create_instance(objcls, settings, crawler, *args, **kwargs):
    if settings is None:
        if crawler is None:
            raise ValueError("Specify at least one of settings and crawler.")
        settings = crawler.settings
    if crawler and hasattr(objcls, 'from_crawler'):
        return objcls.from_crawler(crawler, *args, **kwargs)
    else:
        print('Error in misc.py')
    # elif hasattr(objcls, 'from_settings'):
    #     return objcls.from_settings(settings, *args, **kwargs)
    # else:
    #     return objcls(*args, **kwargs)