"""
Helper functions for dealing with Twisted deferreds
"""
from twisted.internet import defer

def process_chain(cbs, input, *a, **kw):
    """Return a Deferred built by chaining the given callbacks"""
    d = defer.Deferred()
    for x in cbs:
        print('process_chain')
    d.callback(input)
    return d