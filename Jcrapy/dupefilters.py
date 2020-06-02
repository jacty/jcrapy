class BaseDupeFilter:
    
    @classmethod
    def from_settings(cls, settings):
        print('BaseDupeFilter.from_settings')
    
class RFPDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self, path=None, debug=False):
        pass

    @classmethod
    def from_settings(cls, settings):
        return cls()