"""
Helper functions for dealing with Twisted deferreds
"""
from twisted.internet import defer
from twisted.python import failure

def defer_succeed(result):
    print('defer_succeed')

def defer_result(result):
    print('defer_result',result)
    return
    if isinstance(result, defer.Deferred):
        return result
    elif isinstance(result, failure.Failure):
        return defer_fail(result)
    else:
        return defer_succeed(result)

def mustbe_deferred(f, *args, **kw):
    try:
        result = f(*args, **kw)
    except Exception as e:
        print('error in mustbe_deferred', e)
    else:
        return defer_result(result)    

def process_chain(cbs, input, *a):
    """Return a Deferred built by chaining the given callbacks"""
    d = defer.Deferred()
    for x in cbs:
        print('process_chain',x)
        d.addCallback(x, *a)
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