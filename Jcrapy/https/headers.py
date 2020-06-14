from Jcrapy.utils.datatypes import CaselessDict

class Headers(CaselessDict):
    """Case insensitive http headers dictionary"""

    def __init__(self, seq=None, encoding='utf-8'):
        self.encoding = encoding
        super(Headers, self).__init__(seq)

    def __getitem__(self, key):
        print('Headers.__getitem__')

    def __copy__(self):
        print('Headers.__copy__')
        return self.__class__(self)
    copy = __copy__