# """
# Scrapy - a web crawling and web scraping framework written for Python
# """

# __all__ = ['__version__', 'version_info', 'twisted_version',
#            'Spider', 'Request', 'FormRequest', 'Selector', 'Item', 'Field']

# # Scrapy version
# import pkgutil
# __version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
# version_info = tuple(int(v) if v.isdigit() else v
#                      for v in __version__.split('.'))
# del pkgutil


# # Ignore noisy twisted deprecation warnings
# # import warnings
# # warnings.filterwarnings('ignore', category=DeprecationWarning, module='twisted')
# # del warnings

# # Apply monkey patches to fix issues in external libraries
# # from scrapy import _monkeypatches
# # del _monkeypatches

# from twisted import version as _txv
# twisted_version = (_txv.major, _txv.minor, _txv.micro)

# # Declare top-level shortcuts
# from jcrapy.spiders import Spider
# # from scrapy.http import Request, FormRequest
# # from scrapy.selector import Selector
# # from scrapy.item import Item, Field

