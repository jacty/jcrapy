import os
import sys
from configparser import ConfigParser
from .const import ENVVAR

def closest_file(filename='Jcrapy.cfg' ,path='.', prevpath=None):
    """Return the path to the closest filename file by traversing the current
    directory and its parents
    """
    if filename == '' :
        print('Argument filename cannot be empty!')

    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    file = os.path.join(path, filename)
    if os.path.exists(file):
        return file
    return closest_file(filename,os.path.dirname(path), path)

def init_env(project='default'):
    """Setting environment value to locate settings.
    """
    closest = closest_file()
    cfg = get_config(closest)

    if cfg.has_option('settings', project):
        os.environ[ENVVAR] = cfg.get('settings', project)
    
def get_config(closest=None):
    """Get Jcrapy config file as a ConfigParser"""
    sources = get_sources(closest)
    cfg = ConfigParser()
    cfg.read(sources)
    return cfg

def get_sources(closest=None):
    sources = []
    if closest:
        sources.append(closest)
    return sources
