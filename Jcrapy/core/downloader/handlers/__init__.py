from Jcrapy.utils.misc import load_object, create_instance

class DownloadHandlers:

    def __init__(self, crawler):
        self._crawler = crawler
        self._schemes = {} #stores acceptable schemes on instancing
        self._handlers = {} #stores instanced handlers for schemes
        self._notconfigured = {} # remembers failed handlers 
        handlers = crawler.settings.getwithbase('DOWNLOAD_HANDLERS')
        for scheme, clspath in handlers.items():
            self._schemes[scheme] = clspath
            self._load_handler(scheme, skip_lazy=True)

    def _load_handler(self, scheme, skip_lazy=False):
        path = self._schemes[scheme]
        dhcls = load_object(path)
        if skip_lazy and getattr(dhcls, 'lazy', True):
            return None

        dh = create_instance(
            objcls=dhcls,
            settings=self._crawler.settings,
            crawler=self._crawler,
            )
        self._handlers[scheme] = dh
        return dh