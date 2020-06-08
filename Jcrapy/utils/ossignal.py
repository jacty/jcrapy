import signal
from twisted.internet import reactor

def install_shutdown_handlers(function):
    """Install the given function as a signal handler for all common shutdown
    signals (such as SIGINT, SIGTERM, etc). If override_sigint is ``False`` the
    SIGINT handler won't be install if there is already a handler in place
    (e.g.  Pdb)
    """
    reactor._handleSignals()
    #TD:Need to check how this part works and what is the target here.
    signal.signal(signal.SIGTERM, function)