"""
Base class for Jcrapy spiders

See documentation in docs/topics/spiders.rst
"""


class Spider:
    """Base class for Jcrapy spiders. All spiders must inherit from this
    class.
    """    
    name = None
    custom_settings = None

    def __init__(self, name=None, **kwargs):
        print('Spider.__init__')