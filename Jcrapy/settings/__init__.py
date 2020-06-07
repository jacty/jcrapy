import json
import copy

from importlib import import_module
from Jcrapy.settings import default_settings

class SettingsAttribute:

    """Class for storing data related to settings attributes.

    This class is intended for internal usage, you should try Settings class
    for settings configuration, not this one.
    """
    def __init__(self, value, priority):
        self.value = value
        if isinstance(self.value, BaseSettings):
            print('SettingsAttribute.__init__', isinstance(self.value, BaseSettings))
        else:
            self.priority = priority

    def __str__(self):
        return "<SettingsAttribute value={self.value!r} " \
               "priority={self.priority}>".format(self=self)

    __repr__ = __str__

class BaseSettings:
    def __init__(self, values=None):
        self.frozen = False
        self.attributes = {}
        if values:
            print('BaseSettings.__init__.update()')
            self.update(values, priority)
    
    def __getitem__(self, opt_name):
        print('BaseSettings.__getitem__')
        if opt_name not in self:
            return None
        return self.attributes[opt_name].value
 
    def __contains__(self, name):
        print('BaseSettings.__contains__')
        return name in self.attributes

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
        print('set', name)
        return
        if name not in self:
            if isinstance(value, SettingsAttribute):
                print('BaseSettings.set', name, value) 
            else:
                self.attributes[name] = SettingsAttribute(value, priority)
        else:
            self.attributes[name].set(value, priority)

    def setdict(self, values, priority='project'):
        self.update(values, priority)

    def setmodule(self, module):
        """
        Deliver uppercased settings to self.set().
        """ 
        if isinstance(module, str):
            module = import_module(module)

        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def update(self, values, priority='project'):
        """
        Store key/value pairs with a given priority.

        This is a helper function that calls
        :meth:`~Jcrapy.settings.BaseSettings.set` for every item of ``values``
        with the provided ``priority``.

        If ``values`` is a string, it is assumed to be JSON-encoded and parsed
        into a dict with ``json.loads()`` first. If it is a
        :class:`~Jcrapy.settings.BaseSettings` instance, the per-key priorities
        will be used and the ``priority`` parameter ignored. This allows
        inserting/updating settings with different priorities with a single
        command.

        :param values: the settings names and values
        :type values: dict or string or :class:`~Jcrapy.settings.BaseSettings`

        :param priority: the priority of the settings. Should be a key of
            :attr:`~Jcrapy.settings.SETTINGS_PRIORITIES` or an integer
        :type priority: string or int
        """
        self._assert_mutability()
        if isinstance(values, str):
            print('BaseSettings.update', values)
        elif values is not None:
            if isinstance(values, BaseSettings):
                print('BaseSettings.update1', isinstance(values, BaseSettings))
            else:
                for name, value in values.items():
                    self.set(name, value, priority)

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
        print('Settings.__init__')
        return
        self.update(values, priority)
        