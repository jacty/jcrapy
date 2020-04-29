import os

from importlib import import_module

from Jcrapy.utils.conf import init_env,closest_jcrapy_cfg
from Jcrapy.settings import Settings
from Jcrapy.constants import ENVVAR, valid_envvars



def inside_project():
    jcrapy_module = os.environ.get('JCRAPY_SETTINGS_MODULE')

    if jcrapy_module is not None:
        try:
            import_module(jcrapy_module)
        except ImportError as exc:
            warnings.warn("Cannot import jcrapy settings module %s: %s" % (jcrapy_module, exc))
        else:
            return True
    return bool(closest_jcrapy_cfg())

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