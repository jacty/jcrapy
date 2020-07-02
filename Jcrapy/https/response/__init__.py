"""
This module implements the Response class which is used to represent HTTP
responses in Jcrapy.

See documentation in docs/topics/request-response.rst
"""
from Jcrapy.https.headers import Headers

class Response:

    def __init__(self, url, status=200, headers=None, body=b'', flags=None,
                request=None, certificate=None, ip_address=None):
        self.headers = Headers(headers or {})
        self.status = int(status)
        self._set_body(body)
        self._set_url(url)
        self.request = request
        self.flags = [] if flags is None else list(flags)
        self.certificate = certificate
        self.ip_address = ip_address

    def _set_url(self, url):
        print('Response._set_url', url)

    def _set_body(self, body):
        if body is None:
            self._body = b''
        print('Response._set_body', body)
