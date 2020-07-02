from collections.abc import Mapping

class CaselessDict(dict):

    def __init__(self, seq=None):
        super(CaselessDict, self).__init__()
        if seq:
            self.update(seq)

    def __getitem__(self, key):
        return dict.__getitem__(self, self.normkey(key))

    def __setitem__(self, key, value):
        print('CaselessDict.__setitem__')

    def __delitem__(self, key):
        print('CaselessDict.__delitem__')

    def __contains__(self, key):
        return dict.__contains__(self, self.normkey(key))
    has_key = __contains__

    def __copy__(self):
        print('CaselessDict.__copy__')
    copy = __copy__

    def normkey(self, key):
        """Method to normalize dictionary key access"""
        return key.lower()  

    def normvalue(self, value):
        """Method to normalize values prior to be setted"""
        return value

    def get(self, key, def_val=None):
        return dict.get(self, self.normkey(key), self.normvalue(def_val))      

    def setdefault(self, key, def_val=None):
        print('datatypes.setdefault')

    def update(self, seq):
        seq = seq.items() if isinstance(seq, Mapping) else seq
        iseq = ((self.normkey(k), self.normvalue(v)) for k, v in seq)
        super(CaselessDict, self).update(iseq)

    @classmethod
    def fromkeys(cls, keys, value=None):
        print('datatypes.fromkeys')

    def pop(self,key, *args):
        print('datatypes.pop')