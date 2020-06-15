import json
import copy
from collections.abc import MutableMapping #for iteration from items()
from importlib import import_module

from Jcrapy.settings import default_settings
###
# Setting priorities mapping. In this version, priorities must be a number.
# SETTINGS_PRIORITIES = {
#     'default': 0,
#     'command': 10,
#     'project': 20,
#     'spider': 30,
#     'cmdline': 40,
# }
###

class SettingsAttribute:

    """Class for storing data related to settings attributes.

    This class is intended for internal usage, you should try Settings class
    for settings configuration, not this one.
    """
    def __init__(self, value, priority):
        self.value = value
        if isinstance(self.value, BaseSettings):
            print('SettingsAttribute.__init__')
        else:
            self.priority = priority

    def set(self, value, priority):
        self.value = value
        if priority >= self.priority:
            if isinstance(self.value, BaseSettings):
                print('SettingsAttribute.set',value, priority, self.priority)
            self.value = value
            self.priority = priority

    def __str__(self):
        return "<SettingsAttribute value={self.value!r} ".format(self=self)

    __repr__ = __str__

class BaseSettings(MutableMapping):
    
    def __init__(self, values=None, priority=20):
        self.frozen = False
        self.attributes = {}
        if values:
            self.update(values, priority)
    
    def __getitem__(self, opt_name):
        if opt_name not in self:
            return None
        return self.attributes[opt_name].value
 
    def __contains__(self, name):
        return name in self.attributes

    def get(self, name, default=None):
        return self[name] if self[name] is not None else default

    def getbool(self, name, default=False):
        got = self.get(name, default)
        try:
            return bool(int(got))
        except ValueError:
            if got in ("True", "true"):
                return True
            if got in ("False", "false"):
                return False
            raise ValueError("Supported values for boolean settings "
                             "are 0/1, True/False, '0'/'1', "
                             "'True'/'False' and 'true'/'false'")

    def getint(self, name, default=0):

        return int(self.get(name, default))  
    
    def getfloat(self, name, default=0.0):

        return float(self.get(name, default))

    def getlist(self, name, default=None):
        
        value = self.get(name, default or [])
        if isinstance(value, str):
            value = value.split(',')
        return list(value)

    def getdict(self, name, default=None):
        
        value = self.get(name, default or {})
        if isinstance(value, str):
            value = json.loads(value)
        return dict(value)        

    def getwithbase(self, name):
        """Get a composition of a dictionary-like setting and its `_BASE`
        counterpart.

        :param name: name of the dictionary-like setting
        :type name: string
        """
        compbs = BaseSettings()
        compbs.update(self[name + '_BASE'])
        compbs.update(self[name])   
        return compbs     

    def __setitem__(self, name, value):
        print('BaseSettings.__setitem__')

    def set(self, name, value, priority=20):
        """
        Settings should be populated *before* configuring the Crawler object
        (through the :meth:`~Jcrapy.crawler.Crawler.configure` method),
        otherwise they won't have any effect.

        :param name: the setting name
        :type name: string

        :param value: the value to associate with the setting
        :type value: any
        """  
        if name not in self: 
            if isinstance(value, SettingsAttribute):
                print('BaseSettings.set()')
            else:   
                self.attributes[name] = SettingsAttribute(value, priority)
        else:
            #custom settings replace relevant default settings.
            self.attributes[name].set(value, priority)

    def setmodule(self, module, priority=20):
        """
        Deliver uppercased settings to self.set().
        """ 
        if isinstance(module, str):
            module = import_module(module)

        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key), priority)

    def update(self, values, priority=20):
        """
        :param values: the settings names and values
        :type values: dict or string or :class:`~Jcrapy.settings.BaseSettings`

        """
        for name, value in values.items():
            self.set(name, value)

    def __delitem__(self, name):
        print('BaseSettings.__delitem__')

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        print('BaseSettings.__len__')

class Settings(BaseSettings):
    """
    This object stores Jcrapy settings for the configuration of <internal
    components>, and can be used for any further customization.

    """
    def __init__(self, values=None):
        super(Settings, self).__init__()
        
        # Assign default settings to Settings
        if values is None:
            self.setmodule(default_settings) 

        for name, val in self.items():
            if isinstance(val, dict):
                self.set(name, BaseSettings(val, 0), 0)

                

    
    

        