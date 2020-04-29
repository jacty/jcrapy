import os

from importlib import import_module

from Jcrapy.utils.conf import init_env #,closest_scrapy_cfg
from Jcrapy.settings import Settings
from Jcrapy.constants import ENVVAR, valid_envvars



def inside_project():
    scrapy_module = os.environ.get('SCRAPY_SETTINGS_MODULE')
    
    if scrapy_module is not None:
        try:
            import_module(scrapy_module)
        except ImportError as exc:
            warnings.warn("Cannot import scrapy settings module %s: %s" % (scrapy_module, exc))
        else:
            return True
    return bool(closest_scrapy_cfg())

def get_project_settings():
    if ENVVAR not in os.environ:
        init_env('default') 

    settings = Settings()
    settings_module_path = os.environ.get(ENVVAR)

    if settings_module_path:
        settings.setmodule(settings_module_path, priority='project')
    

    jcrapy_envvars = {k[7:]: v for k, v in os.environ.items() if
                     k.startswith('JCRAPY_')}

    setting_envvars = {k for k in jcrapy_envvars if k not in valid_envvars}

    settings.update(jcrapy_envvars, priority='project')
    return settings