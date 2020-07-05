"""
This module implements the Request class which is used to represent HTTP
requests in Jcrapy.

See documentation in docs/topics/request-response.rst
"""
from w3lib.url import safe_url_string

from Jcrapy.https.headers import Headers
from Jcrapy.utils.python import to_bytes
from Jcrapy.utils.url import escape_ajax

class Request:
    def __init__(self, url, callback=None, method='GET', headers=None, body=None, cookies=None, meta=None, encoding='utf-8', priority=0, dont_filter=False, errback=None, flags=None, cb_kwargs=None):
        self._encoding = encoding #must be set first
        self.method = str(method).upper()
        self._set_url(url)
        self._set_body(body)
        if not isinstance(priority, int):
            raise TypeError("Request priority not an integer: %r" % priority)
        self.priority = priority

        if callback is not None and not callable(callback):
            raise TypeError('callback must be a callable, got %s' % type(callback).__name__)
        if errback is not None and not callable(errback):
            raise TypeError('errback must be a callable, got %s' % type(errback).__name__)
        self.callback = callback
        self.errback = errback

        self.cookies = cookies or {}
        
        self.headers = Headers(headers or {}, encoding=encoding)
        self.dont_filter = dont_filter

        self._meta = dict(meta) if meta else None
        self._cb_kwargs = dict(cb_kwargs) if cb_kwargs else None
        self.flags = [] if flags is None else list(flags)
    
    @property 
    def meta(self):
        if self._meta is None:
            self._meta = {}
        return self._meta

    def _set_url(self, url):
        if not isinstance(url, str):
            raise TypeError('Request url must be str or unicode, got %s:' % type(url).__name__)
        
        s = safe_url_string(url, self.encoding)
        self.url = escape_ajax(s)

        if ('://' not in self.url) and (not self.url.startswith('data:')):
            raise ValueError('Missing scheme in request url: %s' % self.url)        
    def _set_body(self, body):
        if body is None:
            self.body = b''
        else:
            self.body = to_bytes(body, self.encoding)

    @property
    def encoding(self):
        return self._encoding
    