class BaseDupeFilter:
    
    @classmethod
    def from_settings(cls, settings):
        print('BaseDupeFilter.from_settings')

    def open(self): #can return deferred
        pass
    
class RFPDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self, path=None, debug=False):
        self.file = None

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def close(self, reason):
        if self.file:
            self.file.close()