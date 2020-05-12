import os
import sys
from configparser import ConfigParser

def closest_jcrapy_cfg(path='.', prevpath=None):
    """Return the path to the closest Jcrapy.cfg file by traversing the current
    directory and its parents
    """   
    if path == prevpath: 
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, 'Jcrapy.cfg')
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_jcrapy_cfg(os.path.dirname(path), path)


def init_env(project='default', set_syspath=True, use_closest=True):
    """Initialize environment to use command-line tool from inside a project
    dir. This sets the Jcrapy settings module and modifies the Python path to
    be able to locate the project module.
    """
    closest = closest_jcrapy_cfg()
    if closest:
        projdir = os.path.dirname(closest)
        if set_syspath and projdir not in sys.path:
            sys.path.append(projdir)

    if use_closest and closest:
        cfg = get_config(closest)
    else:
        cfg = get_config()

    if cfg.has_option('settings', project):
        os.environ['JCRAPY_SETTINGS_MODULE'] = cfg.get('settings', project)
    

def get_config(closest=None):
    """Get Jcrapy config file as a ConfigParser"""
    sources = get_sources(closest)
    cfg = ConfigParser()
    cfg.read(sources)
    return cfg

def get_sources(closest=None):
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
        os.path.expanduser('~/.config')
    sources = ['/etc/Jcrapy.cfg', xdg_config_home + '/Jcrapy.cfg',
                os.path.expanduser('~/.Jcrapy.cfg')]

    if closest:
        sources.append(closest)
    return sources
