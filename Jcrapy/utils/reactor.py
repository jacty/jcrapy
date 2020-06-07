from twisted.internet import reactor

class CallLaterOnce:
    """Schedule a function to be called in the next reactor loop, but only if
    it hasn't been already scheduled since the last time it ran.
    """

    def __init__(self, func, *a, **kw):
        self._func = func
        self._a = a
        self._call = None
        
    def schedule(self, delay=0):
        if self._call is None:
            self._call = reactor.callLater(delay, self)

    def __call__(self):
        self._call = None
        return self._func(*self._a)