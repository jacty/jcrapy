"""
This module contains the default values for all settings used by Jcrapy.

For more information about these settings you can read the settings
documentation in docs/topics/settings.rst

if you add a setting here remember to:

* add it in alphabetical order
* group similar settings without leaving blank lines
* add its documentation to the available settings documentation
  (docs/topics/settings.rst)

"""

import sys
from importlib import import_module
from os.path import join, abspath, dirname

AJAXCRAWL_ENABLED = False

AUTOTHROTTLE_ENABLED = False
AUTOTHROTTLE_DEBUG = False
AUTOTHROTTLE_MAX_DELAY = 60.0
AUTOTHROTTLE_START_DELAY = 5.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

BOT_NAME = 'Jcrapybot'

CLOSESPIDER_TIMEOUT = 0
CLOSESPIDER_PAGECOUNT = 0
CLOSESPIDER_ITEMCOUNT = 0
CLOSESPIDER_ERRORCOUNT = 0

COMPRESSION_ENABLED = True

CONCURRENT_ITEMS = 100

CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 0

COOKIES_ENABLED = True
COOKIES_DEBUG = False

DEFAULT_ITEM_CLASS = 'Jcrapy.item.Item'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DEPTH_LIMIT = 0
DEPTH_STATS_VERBOSE = False
DEPTH_PRIORITY = 0

DNSCACHE_ENABLED = True
DNSCACHE_SIZE = 10000
DNS_RESOLVER = 'Jcrapy.resolver.CachingThreadedResolver'
DNS_TIMEOUT = 60

DOWNLOAD_DELAY = 0

DOWNLOAD_HANDLERS = {}
DOWNLOAD_HANDLERS_BASE = {
    # 'data': 'Jcrapy.core.downloader.handlers.datauri.DataURIDownloadHandler',
    # 'file': 'Jcrapy.core.downloader.handlers.file.FileDownloadHandler',
    'http': 'Jcrapy.core.downloader.handlers.http.HTTPDownloadHandler',
    # 'https': 'Jcrapy.core.downloader.handlers.http.HTTPDownloadHandler',
    # 's3': 'Jcrapy.core.downloader.handlers.s3.S3DownloadHandler',
    # 'ftp': 'Jcrapy.core.downloader.handlers.ftp.FTPDownloadHandler',
}

DOWNLOAD_TIMEOUT = 180      # 3mins

DOWNLOAD_MAXSIZE = 1024 * 1024 * 1024   # 1024m
DOWNLOAD_WARNSIZE = 32 * 1024 * 1024    # 32m

DOWNLOAD_FAIL_ON_DATALOSS = True

DOWNLOADER = 'Jcrapy.core.downloader.Downloader'

DOWNLOADER_HTTPCLIENTFACTORY = 'Jcrapy.core.downloader.webclient.JcrapyHTTPClientFactory'
DOWNLOADER_CLIENTCONTEXTFACTORY = 'Jcrapy.core.downloader.contextfactory.JcrapyClientContextFactory'
DOWNLOADER_CLIENT_TLS_CIPHERS = 'DEFAULT'
# Use highest TLS/SSL protocol version supported by the platform, also allowing negotiation:
DOWNLOADER_CLIENT_TLS_METHOD = 'TLS'
DOWNLOADER_CLIENT_TLS_VERBOSE_LOGGING = False

DOWNLOADER_MIDDLEWARES = {}

DOWNLOADER_MIDDLEWARES_BASE = {
    # Engine side
    # 'Jcrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    # 'Jcrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    # 'Jcrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    # 'Jcrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'Jcrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    # 'Jcrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    # 'Jcrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    # 'Jcrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    # 'Jcrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    # 'Jcrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    # 'Jcrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    # 'Jcrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    # 'Jcrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    # 'Jcrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
    # Downloader side
}

DOWNLOADER_STATS = True

DUPEFILTER_CLASS = 'Jcrapy.dupefilters.RFPDupeFilter'

EDITOR = 'vi'
if sys.platform == 'win32':
    EDITOR = '%s -m idlelib.idle'

EXTENSIONS = {}

EXTENSIONS_BASE = {
    'Jcrapy.extensions.corestats.CoreStats': 0,
    'Jcrapy.extensions.telnet.TelnetConsole': 0,
    'Jcrapy.extensions.memusage.MemoryUsage': 0,
    'Jcrapy.extensions.memdebug.MemoryDebugger': 0,
    'Jcrapy.extensions.closespider.CloseSpider': 0,
    'Jcrapy.extensions.feedexport.FeedExporter': 0,
    'Jcrapy.extensions.logstats.LogStats': 0,
    'Jcrapy.extensions.spiderstate.SpiderState': 0,
    'Jcrapy.extensions.throttle.AutoThrottle': 0,
}

FEED_TEMPDIR = None
FEEDS = {}
FEED_URI_PARAMS = None  # a function to extend uri arguments
FEED_STORE_EMPTY = False
FEED_EXPORT_ENCODING = None
FEED_EXPORT_FIELDS = None
FEED_STORAGES = {}
FEED_STORAGES_BASE = {
    '': 'Jcrapy.extensions.feedexport.FileFeedStorage',
    'file': 'Jcrapy.extensions.feedexport.FileFeedStorage',
    'stdout': 'Jcrapy.extensions.feedexport.StdoutFeedStorage',
    's3': 'Jcrapy.extensions.feedexport.S3FeedStorage',
    'ftp': 'Jcrapy.extensions.feedexport.FTPFeedStorage',
}
FEED_EXPORTERS = {}
FEED_EXPORTERS_BASE = {
    'json': 'Jcrapy.exporters.JsonItemExporter',
    'jsonlines': 'Jcrapy.exporters.JsonLinesItemExporter',
    'jl': 'Jcrapy.exporters.JsonLinesItemExporter',
    'csv': 'Jcrapy.exporters.CsvItemExporter',
    'xml': 'Jcrapy.exporters.XmlItemExporter',
    'marshal': 'Jcrapy.exporters.MarshalItemExporter',
    'pickle': 'Jcrapy.exporters.PickleItemExporter',
}
FEED_EXPORT_INDENT = 0

FEED_STORAGE_FTP_ACTIVE = False
FEED_STORAGE_S3_ACL = ''

FILES_STORE_S3_ACL = 'private'
FILES_STORE_GCS_ACL = ''

FTP_USER = 'anonymous'
FTP_PASSWORD = 'guest'
FTP_PASSIVE_MODE = True

HTTPCACHE_ENABLED = False
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_MISSING = False
HTTPCACHE_STORAGE = 'Jcrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_ALWAYS_STORE = False
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_IGNORE_SCHEMES = ['file']
HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS = []
HTTPCACHE_DBM_MODULE = 'dbm'
HTTPCACHE_POLICY = 'Jcrapy.extensions.httpcache.DummyPolicy'
HTTPCACHE_GZIP = False

HTTPPROXY_ENABLED = True
HTTPPROXY_AUTH_ENCODING = 'latin-1'

IMAGES_STORE_S3_ACL = 'private'
IMAGES_STORE_GCS_ACL = ''

ITEM_PROCESSOR = 'Jcrapy.pipelines.ItemPipelineManager'

ITEM_PIPELINES = {}
ITEM_PIPELINES_BASE = {}

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FORMATTER = 'Jcrapy.logformatter.LogFormatter'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
LOG_STDOUT = False
LOG_LEVEL = 'DEBUG'
LOG_FILE = None
LOG_SHORT_NAMES = False

SCHEDULER_DEBUG = False

LOGSTATS_INTERVAL = 60.0

MAIL_HOST = 'localhost'
MAIL_PORT = 25
MAIL_FROM = 'Jcrapy@localhost'
MAIL_PASS = None
MAIL_USER = None

MEMDEBUG_ENABLED = False        # enable memory debugging
MEMDEBUG_NOTIFY = []            # send memory debugging report by mail at engine shutdown

MEMUSAGE_CHECK_INTERVAL_SECONDS = 60.0
MEMUSAGE_ENABLED = True
MEMUSAGE_LIMIT_MB = 0
MEMUSAGE_NOTIFY_MAIL = []
MEMUSAGE_WARNING_MB = 0

METAREFRESH_ENABLED = True
METAREFRESH_IGNORE_TAGS = []
METAREFRESH_MAXDELAY = 100

NEWSPIDER_MODULE = ''

RANDOMIZE_DOWNLOAD_DELAY = True

REACTOR_THREADPOOL_MAXSIZE = 10

REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 20  # uses Firefox default setting
REDIRECT_PRIORITY_ADJUST = +2

REFERER_ENABLED = True
REFERRER_POLICY = 'Jcrapy.spidermiddlewares.referer.DefaultReferrerPolicy'

RETRY_ENABLED = True
RETRY_TIMES = 2  # initial response + 2 retries = 3 requests
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
RETRY_PRIORITY_ADJUST = -1

ROBOTSTXT_OBEY = False
ROBOTSTXT_PARSER = 'Jcrapy.robotstxt.ProtegoRobotParser'
ROBOTSTXT_USER_AGENT = None

SCHEDULER = 'Jcrapy.core.scheduler.Scheduler'
SCHEDULER_DISK_QUEUE = 'Jcrapy.squeues.PickleLifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'Jcrapy.squeues.LifoMemoryQueue'
SCHEDULER_PRIORITY_QUEUE = 'Jcrapy.pqueues.JcrapyPriorityQueue'

SCRAPER_SLOT_MAX_ACTIVE_SIZE = 5000000

SPIDER_LOADER_CLASS = 'Jcrapy.spiderloader.SpiderLoader'
SPIDER_LOADER_WARN_ONLY = False



SPIDER_MIDDLEWARES = {}

SPIDER_MIDDLEWARES_BASE = {
    # Engine side
    # 'Jcrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    # 'Jcrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    # 'Jcrapy.spidermiddlewares.referer.RefererMiddleware': 700,
    # 'Jcrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    # 'Jcrapy.spidermiddlewares.depth.DepthMiddleware': 900,
    # Spider side
}
SPIDER_MODULES = []

STATS_CLASS = 'Jcrapy.statscollectors.MemoryStatsCollector'
STATS_DUMP = True

STATSMAILER_RCPTS = []

TEMPLATES_DIR = abspath(join(dirname(__file__), '..', 'templates'))

URLLENGTH_LIMIT = 2083

USER_AGENT = 'Jacty0219@qq.com'

TELNETCONSOLE_ENABLED = 1
TELNETCONSOLE_PORT = [6023, 6073]
TELNETCONSOLE_HOST = '127.0.0.1'
TELNETCONSOLE_USERNAME = 'Jcrapy'
TELNETCONSOLE_PASSWORD = None

TWISTED_REACTOR = None

SPIDER_CONTRACTS = {}
SPIDER_CONTRACTS_BASE = {
    'Jcrapy.contracts.default.UrlContract': 1,
    'Jcrapy.contracts.default.CallbackKeywordArgumentsContract': 1,
    'Jcrapy.contracts.default.ReturnsContract': 2,
    'Jcrapy.contracts.default.ScrapesContract': 3,
}
