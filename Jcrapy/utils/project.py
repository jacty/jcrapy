import os
import warnings

from importlib import import_module

from Jcrapy.utils.const import ENVVAR
from Jcrapy.utils.conf import init_env, closest_file
from Jcrapy.settings import Settings

def inside_project():
    jcrapy_module = os.environ.get(ENVVAR)
    if jcrapy_module is not None:
        try:
            import_module(jcrapy_module)
        except ImportError as exc:
            warnings.warn("Cannot import jcrapy settings module %s: %s" % (jcrapy_module, exc))
        else:
            return True
            
    return bool(closest_file())


def get_project_settings():
    if ENVVAR not in os.environ:
        init_env()

    #initialize default settings from settings.default_settings
    settings = Settings()
    return

    settings_module_path = os.environ.get(ENVVAR)
    if settings_module_path:
        settings.setmodule(settings_module_path, priority='project')
    
    jcrapy_envvars = {k[7:]: v for k, v in os.environ.items() if
                        k.startswith('JCRAPY_')}

    settings.setdict(jcrapy_envvars, priority='project')
    
    return settings        

