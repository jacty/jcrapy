import copy
from collections.abc import MutableMapping
from importlib import import_module

from settings import default_settings

SETTINGS_PRIORITIES = {
    'default': 0,
    'command': 10,
    'project': 20,
    'spider': 30,
    'cmdline': 40,
}

def get_settings_priority(priority):
    """
    Small helper function that looks up a given string priority in the
    :attr:`~Jcrapy.settings.SETTINGS_PRIORITIES` dictionary and returns its
    numerical value, or directly returns a given numerical priority.
    """
    if isinstance(priority, str):
        return SETTINGS_PRIORITIES[priority]
    else:
        return priority   

class SettingsAttribute:

    """Class for storing data related to settings attributes.

    This class is intended for internal usage, you should try Settings class
    for settings configuration, not this one.
    """
    def __init__(self, value, priority):
        self.value = value
        if isinstance(self.value, BaseSettings):
            print('self.value is BaseSettings')
        else:
            self.priority = priority

    def set(self, value, priority):
        """Sets value if priority is higher or equal than current priority."""

        if priority >= self.priority:
            if isinstance(self.value, BaseSettings):
                print('SettingsAttribute.set()', self.value, value)
                return
                value = BaseSettings(value, priority=priority)
            self.value = value
            self.priority = priority

    def __str__(self):
        return "<SettingsAttribute value={self.value!r} " \
               "priority={self.priority}>".format(self=self)

    __repr__ = __str__  

class BaseSettings(MutableMapping):
    """
    Instances of this class behave like dictionaries, but store priorities
    along with their ``(key, value)`` pairs, and can be frozen (i.e. marked
    immutable).

    Key-value entries can be passed on initialization with the ``values``
    argument, and they would take the ``priority`` level (unless ``values`` is
    already an instance of :class:`~Jcrapy.settings.BaseSettings`, in which
    case the existing priority levels will be kept).  If the ``priority``
    argument is a string, the priority name will be looked up in
    :attr:`~Jcrapy.settings.SETTINGS_PRIORITIES`. Otherwise, a specific integer
    should be provided.

    Once the object is created, new settings can be loaded or updated with the
    :meth:`~Jcrapy.settings.BaseSettings.set` method, and can be accessed with
    the square bracket notation of dictionaries, or with the
    :meth:`~Jcrapy.settings.BaseSettings.get` method of the instance and its
    value conversion variants. When requesting a stored key, the value with the
    highest priority will be retrieved.
    """
    def __init__(self, values=None, priority='project'):
        self.frozen = False
        self.attributes = {}
        self.update(values, priority)

    def __getitem__(self, opt_name):
        if opt_name not in self:
            return None
        return self.attributes[opt_name].value
    
    def __contains__(self, name):
        return name in self.attributes

    def get(self, name, default=None):
        """
        Get a setting value without affecting its original type.

        :param name: the setting name
        :type name: string

        :param default: the value to return if no setting is found
        :type default: any
        """
        print('BaseSettings.get')
        return self[name] if self[name] is not None else default  
    
    def getbool(self, name, default=False):
        """
        Get a setting value as a boolean.

        ``1``, ``'1'``, `True`` and ``'True'`` return ``True``,
        while ``0``, ``'0'``, ``False``, ``'False'`` and ``None`` return ``False``.

        For example, settings populated through environment variables set to
        ``'0'`` will return ``False`` when using this method.

        :param name: the setting name
        :type name: string

        :param default: the value to return if no setting is found
        :type default: any
        """
        print('BaseSettings.getbool')
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
    def getinit(self, name, default=0):
        print('BaseSettings.getint')

    def getfloat(self, name, default=0.0):
        print('BaseSettings.getfloat')  

    def getlist(self, name, default=None):
        """
        Get a setting value as a list. If the setting original type is a list, a
        copy of it will be returned. If it's a string it will be split by ",".

        For example, settings populated through environment variables set to
        ``'one,two'`` will return a list ['one', 'two'] when using this method.

        :param name: the setting name
        :type name: string

        :param default: the value to return if no setting is found
        :type default: any
        """
        print('BaseSettings.getlist')
        value = self.get(name, default or [])
        if isinstance(value, str):
            value = value.split(',')
        return list(value) 

    def getdict(self, name, default=None):
        print('BaseSettings.getdict')

    def getwithbase(self, name):
        """Get a composition of a dictionary-like setting and its `_BASE`
        counterpart.

        :param name: name of the dictionary-like setting
        :type name: string
        """
        print('BaseSettings.getwithbase')
        compbs = BaseSettings()
        compbs.update(self[name + '_BASE'])
        compbs.update(self[name])
        return compbs

    def getpriority(self, name):
        """
        Return the current numerical priority value of a setting, or ``None`` if
        the given ``name`` does not exist.

        :param name: the setting name
        :type name: string
        """
        print('BaseSettings.getpriority')
        if name not in self:
            return None
        return self.attributes[name].priority


    def maxpriority(self):
        print('BaseSettings.maxpriority')

    def __setitem__(self, name, value):
        print('BaseSettings.__setitem__')

    def set(self, name, value, priority='project'):
        """
        Store a key/value attribute with a given priority.

        Settings should be populated *before* configuring the Crawler object
        (through the :meth:`~Jcrapy.crawler.Crawler.configure` method),
        otherwise they won't have any effect.

        :param name: the setting name
        :type name: string

        :param value: the value to associate with the setting
        :type value: any

        :param priority: the priority of the setting. Should be a key of
            :attr:`~Jcrapy.settings.SETTINGS_PRIORITIES` or an integer
        :type priority: string or int
        """

        self._assert_mutability()
        priority = get_settings_priority(priority)

        if name not in self:
            if isinstance(value, SettingsAttribute):
                print('value is SettingsAttribute')
            else:
                self.attributes[name] = SettingsAttribute(value, priority)
        else:
            self.attributes[name].set(value, priority)

        
    def setdict(self, values, priority='project'):
        print('BaseSettings.setdict')
        self.update(values, priority)

    def setmodule(self, module, priority='project'):
        """
        Store settings from a module with a given priority.

        This is a helper function that calls
        :meth:`~Jcrapy.settings.BaseSettings.set` for every globally declared
        uppercase variable of ``module`` with the provided ``priority``.

        :param module: the module or the path of the module
        :type module: module object or string

        :param priority: the priority of the settings. Should be a key of
            :attr:`~Jcrapy.settings.SETTINGS_PRIORITIES` or an integer
        :type priority: string or int
        """
        self._assert_mutability()

        if isinstance(module, str):
            print('BaseSettings.setmodule')
            return
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key), priority)

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
            print('BaseSettings.update')
        if values is not None:
            if isinstance(values, BaseSettings):
                print('BaseSettings.update')
                for name, value in values.items():
                    self.set(name, value, values.getpriority(name))
            else:
                for name, value in values.items():
                    self.set(name, value, priority)

    def delete(self):
        print('BaseSettings.delete')

    def __delitem__(self):
        print('BaseSettings.__delitem__')

    def _assert_mutability(self):
        if self.frozen:
            raise TypeError("Trying to modify an immutable Settings object")

    def copy(self):
        """
        Make a deep copy of current settings.

        This method returns a new instance of the :class:`Settings` class,
        populated with the same values and their priorities.

        Modifications to the new object won't be reflected on the original
        settings.
        """
        print('BaseSettings.copy')
        return copy.deepcopy(self)

    def freeze(self):
        """
        Disable further changes to the current settings.

        After calling this method, the present state of the settings will become
        immutable. Trying to change values through the :meth:`~set` method and
        its variants won't be possible and will be alerted.
        """
        self.frozen = True
        
    def frozencopy(self):
        """
        Return an immutable copy of the current settings.

        Alias for a :meth:`~freeze` call in the object returned by :meth:`copy`.
        """
        copy = self.copy()
        copy.freeze()
        return copy

    def __iter__(self):
        return iter(self.attributes)

    def __len__():
        print('BaseSettings.__len__')
        return len(self.attributes)

class Settings(BaseSettings):
    """
    This object stores Jcrapy settings for the configuration of internal
    components, and can be used for any further customization.

    It is a direct subclass and supports all methods of
    :class:`~Jcrapy.settings.BaseSettings`. Additionally, after instantiation
    of this class, the new object will have the global default settings
    described on :ref:`topics-settings-ref` already populated.
    """

    def __init__(self, values=None, priority='project'):
        # Do not pass kwarg values here. We don't want to promote user-defined
        # dicts, and we want to update, not replace, default dicts with the
        # values given by the user
        super(Settings, self).__init__()
        self.setmodule(default_settings, 'default')               
        # Promote default dictionaries to BaseSettings instances for per-key
        # priorities

        for name, val in self.items():
            if isinstance(val, dict):
                self.set(name, BaseSettings(val, 'default'), 'default')

        self.update(values, priority)

def iter_default_settings():
    """Return the default settings as an iterator of (name, value) tuples"""
    for name in dir(default_settings):
        if name.isupper():
            yield name, getattr(default_settings, name)

def overridden_settings(settings):
    """Return a dict of the settings that have been overridden"""    
    
    for name, defvalue in iter_default_settings():
        value = settings[name]
        if not isinstance(defvalue, dict) and value != defvalue:
            yield name, value