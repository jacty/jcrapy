import os
import sys
from configparser import ConfigParser

def arglist_to_dict(arglist):
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    return dict(x.split('=', 1) for x in arglist)    

def closest_scrapy_cfg(path='.', prevpath=None):
    """Return the path of the closest jcrapy.cfg file by traversing the current
    directory and its parents
    """
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, 'Jcrapy.cfg')
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_scrapy_cfg(os.path.dirname(path), path)


def init_env(project='default', set_syspath=True):
    """Initialize environment to use command-line tool from inside a project
    dir. This sets the Jcrapy settings module and modifies the Python path to
    be able to locate the project module.
    """

    cfg = get_config()

    if cfg.has_option('settings', project):
        os.environ['JCRAPY_SETTINGS_MODULE'] = cfg.get('settings', project)


def get_config(use_closet=True):
    """Get Jcrapy config file as a ConfigParser"""

    #TD: ErrorType is needed to be more accurate.
    sources = closest_scrapy_cfg()
    if sources == "":
        raise NameError("Jcrapy config file is missing!")
    cfg = ConfigParser()
    cfg.read(sources)
    return cfg

