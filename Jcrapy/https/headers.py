from Jcrapy.utils.datatypes import CaselessDict

class Headers(CaselessDict):
    """Case insensitive http headers dictionary"""

    def __init__(self, seq=None, encoding='utf-8'):
        self.encoding = encoding
        super(Headers, self).__init__(seq)

    def normkey(self, key):
        """Normalize key to bytes"""
        return self._tobytes(key.title())

    def normvalue(self, value):
        """Normalize values to bytes"""
        if value is None:
            value = []
        elif isinstance(value, (str, bytes)):
            value = [value]
        elif not hasattr(value, '__iter__'):
            value = [value]

        return [self._tobytes(x) for x in value]

    def _tobytes(self, x):
        if isinstance(x, bytes):
            return x
        elif isinstance(x, str):
            return x.encode(self.encoding)
        elif isinstance(x, int):
            return str(x).encode(self.encoding)
        else:
            raise TypeError('Unsupported value type: {}'.format(type(x)))            
    def __getitem__(self, key):
        try:
            return super(Headers, self).__getitem__(key)[-1]
        except IndexError:
            return None

    def get(self, key, def_val=None):
        try:
            return super(Headers, self).get(key, def_val)[-1]
        except IndexError:
            return None

    def getlist(self, key, def_val=None):
        try:
            return super(Headers, self).__getitem__(key)
        except KeyError:
            if def_val is not None:
                return self.normvalue(def_val)
            return []

    def setlist(self, key, list_):
        print('headers.setlist')

    def setlistdefault(self, key, default_list=()):
        print('headers.setlistdefault')

    def appendlist(self, key, value):
        print('headers.appendlist')

    def items(self):
        return ((k, self.getlist(k)) for k in self.keys())

    def values(self):
        print('headers.values')

    def to_string(self):
        print('headers.to_string')

    def to_unicode_dict(self):
        print('headers.to_unicode_dict')
            
    def __copy__(self):
        print('Headers.__copy__')
        return self.__class__(self)
    copy = __copy__