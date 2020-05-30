class BaseDupeFilter:
    pass
    
class RFPDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self):
        print('RFPDupeFilter.__init__')    