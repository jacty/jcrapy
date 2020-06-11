import numbers
import os
import sys
from configparser import ConfigParser
from operator import itemgetter
from .const import ENVVAR

from Jcrapy.settings import BaseSettings
from Jcrapy.utils.python import without_none_values

def build_component_list(compdict):
    """Compose a component list from a { class: order } dictionary."""

    def _validate_values(compdict):
        """Fail if a value in the components dict is not a real number or None."""     
        for name, value in compdict.items(): 
            if value is not None and not isinstance(value, numbers.Real):
                raise ValueError('Invalid value {} for component {}, please provide a real number or None instead'.format(value, name))  
    
    _validate_values(compdict)
    compdict = without_none_values(compdict)
    return [k for k, v in sorted(compdict.items(), key=itemgetter(1))]

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
