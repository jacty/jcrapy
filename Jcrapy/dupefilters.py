from Jcrapy.utils.request import request_fingerprint

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
        self.fingerprints = set()

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def request_seen(self, request):
        fp = request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        
    def close(self, reason):
        if self.file:
            self.file.close()

    def log(self, request, spider):
        print('RFPDupeFilter.log')