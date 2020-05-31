"""
This module implements the Request class which is used to represent HTTP
requests in Jcrapy.

See documentation in docs/topics/request-response.rst
"""

class Request:
    def __init__(self, url, callback=None, method='GET', headers=None, body=None, cookies=None, meta=None, encoding='utf-8', priority=0, dont_filter=False):

        self._encoding = encoding #must be set first
        self.method = str(method).upper()
        self._set_url(url)
        print('Request.__init__')

    def _set_url(self, url):
        print('_set_url',url)