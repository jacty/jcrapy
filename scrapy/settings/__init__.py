from collections.abc import MutableMapping

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
    :attr:`~scrapy.settings.SETTINGS_PRIORITIES` dictionary and returns its
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
    
    def set():
        print('BaseSettings.set()')    
class BaseSettings(MutableMapping):
    """
    Instances of this class behave like dictionaries, but store priorities
    along with their ``(key, value)`` pairs, and can be frozen (i.e. marked
    immutable).

    Key-value entries can be passed on initialization with the ``values``
    argument, and they would take the ``priority`` level (unless ``values`` is
    already an instance of :class:`~scrapy.settings.BaseSettings`, in which
    case the existing priority levels will be kept).  If the ``priority``
    argument is a string, the priority name will be looked up in
    :attr:`~scrapy.settings.SETTINGS_PRIORITIES`. Otherwise, a specific integer
    should be provided.

    Once the object is created, new settings can be loaded or updated with the
    :meth:`~scrapy.settings.BaseSettings.set` method, and can be accessed with
    the square bracket notation of dictionaries, or with the
    :meth:`~scrapy.settings.BaseSettings.get` method of the instance and its
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
        print('get')  
    
    def getbool(self, name, default=False):
        print('getbool')  

    def getinit(self, name, default=0):
        print('getint')

    def getfloat(self, name, default=0.0):
        print('getfloat')  

    def getlist(self, name, default=None):
        print('getlist')  

    def getdict(self, name, default=None):
        print('getdict')

    def getwithbase(self, name):
        print('getwithbase')

    def getpriority(self, name):
        print('getpriority')

    def maxpriority(self):
        print('maxpriority')

    def __setitem__(self, name, value):
        print('__setitem__')

    def set(self, name, value, priority='project'):
        """
        Store a key/value attribute with a given priority.

        Settings should be populated *before* configuring the Crawler object
        (through the :meth:`~scrapy.crawler.Crawler.configure` method),
        otherwise they won't have any effect.

        :param name: the setting name
        :type name: string

        :param value: the value to associate with the setting
        :type value: any

        :param priority: the priority of the setting. Should be a key of
            :attr:`~scrapy.settings.SETTINGS_PRIORITIES` or an integer
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
            print('name is in self')

    def setdict(self, values, priority='project'):
        self.update(values, priority)

    def setmodule(self, module, priority='project'):
        """
        Store settings from a module with a given priority.

        This is a helper function that calls
        :meth:`~scrapy.settings.BaseSettings.set` for every globally declared
        uppercase variable of ``module`` with the provided ``priority``.

        :param module: the module or the path of the module
        :type module: module object or string

        :param priority: the priority of the settings. Should be a key of
            :attr:`~scrapy.settings.SETTINGS_PRIORITIES` or an integer
        :type priority: string or int
        """
        self._assert_mutability()
        if isinstance(module, str):
            print('setmodule')
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key), priority)

    def update(self, values, priority='project'):
        """
        Store key/value pairs with a given priority.

        This is a helper function that calls
        :meth:`~scrapy.settings.BaseSettings.set` for every item of ``values``
        with the provided ``priority``.

        If ``values`` is a string, it is assumed to be JSON-encoded and parsed
        into a dict with ``json.loads()`` first. If it is a
        :class:`~scrapy.settings.BaseSettings` instance, the per-key priorities
        will be used and the ``priority`` parameter ignored. This allows
        inserting/updating settings with different priorities with a single
        command.

        :param values: the settings names and values
        :type values: dict or string or :class:`~scrapy.settings.BaseSettings`

        :param priority: the priority of the settings. Should be a key of
            :attr:`~scrapy.settings.SETTINGS_PRIORITIES` or an integer
        :type priority: string or int
        """
        self._assert_mutability()
        if isinstance(values, str):
            print('update')
        if values is not None:
            if isinstance(values, BaseSettings):
                print('values is BaseSettings')
            else:
                for name, value in values.items():
                    print('update1', name, value)

    def delete(self):
        print('delete')

    def __delitem__(self):
        print('__delitem__')

    def _assert_mutability(self):
        if self.frozen:
            raise TypeError("Trying to modify an immutable Settings object")

    def copy():
        print('copy')

    def freeze(self):
        print('freeze')

    def frozencopy(self):
        print('frozencopy')

    def __iter__(self):
        print('__iter__')

    def __len__():
        print('__len__')
class Settings(BaseSettings):
    """
    This object stores Scrapy settings for the configuration of internal
    components, and can be used for any further customization.

    It is a direct subclass and supports all methods of
    :class:`~scrapy.settings.BaseSettings`. Additionally, after instantiation
    of this class, the new object will have the global default settings
    described on :ref:`topics-settings-ref` already populated.
    """

    def __init__(self, values=None, priority='project'):
        # Do not pass kwarg values here. We don't want to promote user-defined
        # dicts, and we want to update, not replace, default dicts with the
        # values given by the user
        super(Settings, self).__init__()
        self.setmodule(default_settings, 'default')
