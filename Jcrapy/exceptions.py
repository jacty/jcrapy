"""
Jcrapy core exceptions

"""

# Internal

# Commands

class UsageError(Exception):
    """To indicate a command-line usage error"""

    def __init__(self, *a):
        super(UsageError, self).__init__(*a)