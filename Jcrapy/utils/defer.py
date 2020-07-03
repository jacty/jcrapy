"""
Helper functions for dealing with Twisted deferreds
"""
import asyncio
import inspect
from functools import wraps

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

def process_chain(cbs, input, *a, **kw):
    """Return a Deferred built by chaining the given callbacks"""
    d = defer.Deferred()
    for x in cbs:
        d.addCallback(x, *a, **kw)
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


def deferred_from_coro(o):
    """Converts a coroutine into a Deferred, or returns the object as is if it isn't a coroutine"""
    if isinstance(o, defer.Deferred):
        return o
    if asyncio.isfuture(o) or inspect.isawaitable(o):
        if not is_asyncio_reactor_installed():
            # wrapping the coroutine directly into a Deferred, this doesn't work correctly with coroutines
            # that use asyncio, e.g. "await asyncio.sleep(1)"
            return defer.ensureDeferred(o)
        else:
            # wrapping the coroutine into a Future and then into a Deferred, this requires AsyncioSelectorReactor
            return defer.Deferred.fromFuture(asyncio.ensure_future(o))
    return o

def deferred_f_from_coro_f(coro_f):
    """ Converts a coroutine function into a function that returns a Deferred.

    The coroutine function will be called at the time when the wrapper is called. Wrapper args will be passed to it.
    This is useful for callback chains, as callback functions are called with the previous callback result.
    """    
    @wraps(coro_f)
    def f(*coro_args, **coro_kwargs):
        return deferred_from_coro(coro_f(*coro_args, **coro_kwargs))
    return f