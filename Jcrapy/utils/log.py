from twisted.python.failure import Failure

def failure_to_exc_info(failure):
    """Extract exc_info from Failure instances"""
    if isinstance(failure, Failure):
        return (failure.type, failure.value, failure.getTracebackObject())    