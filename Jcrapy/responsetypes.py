"""
This module implements a class which returns the appropriate Response class
based on different criteria.
"""
from mimetypes import MimeTypes
from pkgutil import get_data
from io import StringIO

from Jcrapy.https import Response
from Jcrapy.utils.misc import load_object
from Jcrapy.utils.python import to_unicode

class ResponseTypes:
    CLASSES={
        'text/html': 'Jcrapy.https.HtmlResponse',    
    }

    def __init__(self):
        self.classes = {}
        self.mimetypes = MimeTypes()
        mimedata = get_data('Jcrapy', 'mime.types').decode('utf8')
        self.mimetypes.readfp(StringIO(mimedata))
        for mimetype, cls in self.CLASSES.items():
            self.classes[mimetype] = load_object(cls)

    def from_mimetype(self, mimetype):
        """Return the most appropriate Response class for the given mimetype"""
        if mimetype is None:
            return Response
        elif mimetype in self.classes:
            return self.classes[mimetype]
        else:
            print('ResponseTypes.from_mimetype')


    def from_content_type(self, content_type, content_encoding=None):
        """Return the most appropriate Response class from an HTTP Content-Type
        header """
        if content_encoding:
            return Response

        mimetype = to_unicode(content_type).split(';')[0].strip().lower()
        return self.from_mimetype(mimetype)        
        
    def from_headers(self, headers):
        """Return the most appropriate Response class by looking at the HTTP
        headers"""
        cls = Response
        if b'Content-Type' in headers:
            cls = self.from_content_type(
                content_type=headers[b'Content-Type'],
                content_encoding=headers.get(b'Content-Encoding')
                )       

        if cls is Response and b'Content-Disposition' in headers:
            print('from_headers')

        return cls

    def from_args(self, headers=None, url=None, filename=None, body=None):
        """Guess the most appropriate Response class based on
        the given arguments."""
        cls = Response 

        if headers is not None:
            cls = self.from_headers(headers)
        if cls is Response:
            if url is not None:
                print('url is not None')
            elif filename is not None:
                print('filename is not None')
            elif body is not None:
                print('body is not None')
        return cls


