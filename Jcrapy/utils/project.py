import os

from utils.const import ENVVAR
from utils.conf import init_env
from settings import Settings

def get_project_settings():
    if ENVVAR not in os.environ:
        init_env()
    #initialize default settings from settings.default_settings
    settings = Settings()
    settings_module_path = os.environ.get(ENVVAR)
    if settings_module_path:
        settings.setmodule(settings_module_path, priority='project')
    
    jcrapy_envvars = {k[7:]: v for k, v in os.environ.items() if
                        k.startswith('JCRAPY_')}

    settings.setdict(jcrapy_envvars, priority='project')
    
    return settings        

