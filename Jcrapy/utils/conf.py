import numbers
import os
import sys
from configparser import ConfigParser
from operator import itemgetter

from Jcrapy.constants import ENVVAR
from Jcrapy.settings import BaseSettings
from Jcrapy.utils.python import without_none_values

def build_component_list(compdict, custom=None):
    """Compose a component list from a { class: order } dictionary."""

    def _check_components(complist):
        print('build_component_list._check_components')
        return
        if len({convert(c) for c in complist}) != len(complist):
            raise ValueError('Some paths in {!r} convert to the same object, '
                             'please update your settings'.format(complist))

    def _map_keys(compdict):
        if isinstance(compdict, BaseSettings):
            compbs = BaseSettings()
            for k, v in compdict.items():
                prio = compdict.getpriority(k)
                if compbs.getpriority(k) == prio:
                    raise ValueError('Some paths in {!r} convert to the same '
                                     'object, please update your settings'
                                     ''.format(list(compdict.keys())))
                else:
                    compbs.set(k, v, priority=prio)

            return compbs
        else:
            _check_components(compdict)
            return {convert(k): v for k, v in compdict.items()}

    def _validate_values(compdict):
        """Fail if a value in the components dict is not a real number or None."""
        for name, value in compdict.items():
            if value is not None and not isinstance(value, numbers.Real):
                raise ValueError('Invalid value {} for component {}, please provide '
                                 'a real number or None instead'.format(value, name))


    _validate_values(compdict)
    compdict = without_none_values(_map_keys(compdict))
    return [k for k, v in sorted(compdict.items(), key=itemgetter(1))]


def arglist_to_dict(arglist):
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    return dict(x.split('=', 1) for x in arglist)    

def closest_jcrapy_cfg(path='.', prevpath=None):
    """Return the path of the closest jcrapy.cfg file by traversing the current
    directory and its parents
    """
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, 'Jcrapy.cfg')
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_jcrapy_cfg(os.path.dirname(path), path)


def init_env(project='default', set_syspath=True):
    """Initialize environment to use command-line tool from inside a project
    dir. This sets the Jcrapy settings module and modifies the Python path to
    be able to locate the project module.
    """

    cfg = get_config()

    if cfg.has_option('settings', project):
        os.environ[ENVVAR] = cfg.get('settings', project)


def get_config(use_closet=True):
    """Get Jcrapy config file as a ConfigParser"""

    #TD: ErrorType is needed to be more accurate.
    sources = closest_jcrapy_cfg()
    if sources == "":
        raise NameError("Jcrapy config file is missing!")
    cfg = ConfigParser()
    cfg.read(sources)
    return cfg

