import os

from importlib import import_module

from Jcrapy.utils.conf import init_env #,closest_scrapy_cfg
from Jcrapy.settings import Settings

ENVVAR = 'JCRAPY_SETTINGS_MODULE'
DATADIR_CFG_SECTION = 'datadir'


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
        project = os.environ.get('JCRAPY_PROJECT', 'default')
        init_env(project) 

    settings = Settings()
    print('get_project_settings', settings)
    return
    settings_module_path = os.environ.get(ENVVAR)

    if settings_module_path:
        settings.setmodule(settings_module_path, priority='project')

    pickled_settings = os.environ.get("SCRAPY_PICKLED_SETTINGS_TO_OVERRIDE")
    if pickled_settings:
        print('pickled_settings is true')

    scrapy_envvars = {k[7:]: v for k, v in os.environ.items() if
                     k.startswith('SCRAPY_')}
    valid_envvars = {
        'CHECK',
        'PICKLED_SETTINGS_TO_OVERRIDE',
        'PROJECT',
        'PYTHON_SHELL',
        'SETTINGS_MODULE',
    }
    setting_envvars = {k for k in scrapy_envvars if k not in valid_envvars}
    if setting_envvars:
        print('project.get_project_settings', setting_envvars)
    settings.setdict(scrapy_envvars, priority='project')#Q:why don't use settings.update() directly?
    return settings