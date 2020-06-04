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

def process_parallel(callbacks, input, *a, **kw):
    """Return a Deferred with the output of all successful calls to the given
    callbacks
    """
    dfds = [defer.succeed(input).addCallback(x, *a, **kw) for x in callbacks]
    d = defer.DeferredList(dfds, fireOnOneErrback=1, consumeErrors=1)
    d.addCallbacks(lambda r: [x[1] for x in r], lambda f: f.value.subFailure)
    return d