import json
import copy
from collections.abc import MutableMapping #for iteration from items()
from importlib import import_module

from Jcrapy.settings import default_settings

class SettingsAttribute:

    """Class for storing data related to settings attributes.

    This class is intended for internal usage, you should try Settings class
    for settings configuration, not this one.
    """
    def __init__(self, value):
        self.value = value

    def set(self, value):
        self.value = value

    def __str__(self):
        return "<SettingsAttribute value={self.value!r} ".format(self=self)

    __repr__ = __str__

class BaseSettings(MutableMapping):
    def __init__(self, values=None):
        self.frozen = False
        self.attributes = {}
        if values:
            print('BaseSettings.__init__.update()')
            self.update(values, priority)
    
    def __getitem__(self, opt_name):
        if opt_name not in self:
            return None
        return self.attributes[opt_name].value
 
    def __contains__(self, name):
        return name in self.attributes

    def get(self, name, default=None):
        return self[name] if self[name] is not None else default

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

    def set(self, name, value):
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
            self.attributes[name] = SettingsAttribute(value)
        else:
            #custom settings replace relevant default settings.
            self.attributes[name].set(value)

    def setmodule(self, module):
        """
        Deliver uppercased settings to self.set().
        """ 
        if isinstance(module, str):
            module = import_module(module)

        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def update(self, values):
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

        