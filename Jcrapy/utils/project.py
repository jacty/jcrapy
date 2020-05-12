import os

from utils.const import ENVVAR
from utils.conf import init_env
from settings import Settings
def get_project_settings():
    if ENVVAR not in os.environ:
        init_env()
    #initialize default settings from settings.default_settings
    settings = Settings()
    settings_module_path = os.environ.get(ENVVAR)# Should be None?
    print('->>>get_project_settings', settings_module_path)

