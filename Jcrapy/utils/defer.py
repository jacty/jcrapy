"""
Helper functions for dealing with Twisted deferreds
"""
from twisted.internet import defer

def process_chain(cbs, input, *a):
    """Return a Deferred built by chaining the given callbacks"""
    d = defer.Deferred()
    for x in cbs:
        print('process_chain', x)
    d.callback(input)
    return d

def process_parallel(callbacks, input, *a, **kw):
    """Return a Deferred with the output of all successful calls to the given
    callbacks
    """
    dfds = [defer.succeed(input).addCallback(x) for x in callbacks]
    d = defer.DeferredList(dfds)
    d.addCallbacks(lambda r: [x[1] for x in r], lambda f: f.value.subFailure)
    return d