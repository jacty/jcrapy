class CaselessDict(dict):

    def __init__(self, seq=None):
        super(CaselessDict, self).__init__()
        if seq:
            self.update(seq)

    def __getitem__(self, key):
        print('CaselessDict.__getitem__')

    def __setitem__(self, key, value):
        print('CaselessDict.__setitem__')

    def __delitem__(self, key):
        print('CaselessDict.__delitem__')

    def __contains__(self, key):
        print('CaselessDict.__contains__')
    has_key = __contains__

    def __copy__(self):
        print('CaselessDict.__copy__')
    copy = __copy__