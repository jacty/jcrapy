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
    #TD:project maybe have different values
    cfg = get_config()
    print('init_env', cfg)
    return
    if cfg.has_option('settings', project):
        os.environ['SCRAPY_SETTINGS_MODULE'] = cfg.get('settings', project)
    closest = closest_scrapy_cfg()

    if closest:
        projdir = os.path.dirname(closest)
        if set_syspath and projdir not in sys.path:
            sys.path.append(projdir)
    else:
        print('scrapy.cfg is not found.')

def get_config(use_closet=True):
    """Get Jcrapy config file as a ConfigParser"""

    #TD: Warning need to be prettied to be more catchy.
    sources = closest_scrapy_cfg()
    if sources == "":
        print('Jcrapy config file is missing!')
        return
    cfg = ConfigParser()
    cfg.read(sources)
    return cfg

