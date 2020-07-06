"""
Jcrapy core exceptions

"""

# Internal

class NotConfigured(Exception):
    """Indicates a missing configuration situation"""
    pass
class _InvalidOutput(TypeError):
    """
    Indicates an invalid value has been returned by a middleware's processing method.
    Internal and undocumented, it should not be raised or caught by user code.
    """
    pass

class NotSupported(Exception):
    """Indicates a feature or method is not supported"""
    pass

#Commands

class UsageError(Exception):
    """To indicate a command-line usage error"""

    def __init__(self, *a):
        super(UsageError, self).__init__(*a)