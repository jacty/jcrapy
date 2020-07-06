from Jcrapy.exceptions import NotConfigured, NotSupported
from Jcrapy.utils.httpobj import urlparse_cached
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

    def _get_handler(self, scheme):
        """Lazy-load the downloadhandler for a scheme
        only on the first request for that scheme.
        """
        if scheme in self._handlers:
            return self._handlers[scheme]
        if scheme in self._notconfigured:
            return None
        if scheme not in self._schemes:
            self._notconfigured[scheme] = 'no handler available for that scheme'
            return None

        return self._load_handler(scheme)        

    def _load_handler(self, scheme, skip_lazy=False):
        path = self._schemes[scheme]
        print('_load_handler', path)

    def download_request(self, request, spider):
        scheme = urlparse_cached(request).scheme
        handler = self._get_handler(scheme)
        if not handler:
            raise NotSupported("Unsupported URL scheme '%s': %s" % (scheme, self._notconfigured[scheme]))
        return handler.download_request(request, spider)

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