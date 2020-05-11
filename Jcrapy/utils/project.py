import os

from utils.const import ENVVAR
from settings import Settings
def get_project_settings():

    #initialize default settings from settings.default_settings
    settings = Settings()
    
    print('get_project_settings', settings.attributes)

