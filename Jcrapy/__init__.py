# """
# Jcrapy - a web crawling and web scraping framework written for Python
# """

__all__ = ['__version__']

# Jcrapy version

__version__ = "1.0.0"
version_info = tuple(int(v) if v.isdigit() else v
                     for v in __version__.split('.'))

from twisted import version as _txv
twisted_version = (_txv.major, _txv.minor, _txv.micro)

# Declare top-level shortcuts
from Jcrapy.spiders import Spider

