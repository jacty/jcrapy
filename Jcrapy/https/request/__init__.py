"""
This module implements the Request class which is used to represent HTTP
requests in Jcrapy.

See documentation in docs/topics/request-response.rst
"""
from w3lib.url import safe_url_string


class Request:
    def __init__(self, url, callback=None, method='GET', headers=None, body=None, cookies=None, meta=None, encoding='utf-8', priority=0, dont_filter=False):
        print('Request.__init__')
        self._encoding = encoding #must be set first
        self.method = str(method).upper()
        self._set_url(url)
        # self._set_body(body)


    def _set_url(self, url):
        if not isinstance(url, str):
            raise TypeError('Request url must be str or unicode, got %s:' % type(url).__name__)
        s = safe_url_string(url, self.encoding)
        
        if ('://' not in s) and (not s.startswith('data:')):
            raise ValueError('Missing scheme in request url: %s' % s)        

    def _set_body(self, body):
        if body is None:
            self._body = b''
        else:
            self._body = to_bytes(body, self.encoding)

    @property
    def encoding(self):
        return self._encoding
    