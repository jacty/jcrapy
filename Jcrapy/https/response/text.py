from Jcrapy.https.response import Response

_NONE = object()

class TextResponse(Response):

    _DEFAULT_ENCODING = 'ascii'
    _cached_decoded_json = _NONE

    def __init__(self, *args, **kwargs):
        self._encoding = kwargs.pop('encoding', None)
        self._cached_benc = None
        self._cached_ubody = None
        self._cached_selector = None
        super(TextResponse, self).__init__(*args, **kwargs)
    