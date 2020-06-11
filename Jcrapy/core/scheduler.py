from Jcrapy.dupefilters import RFPDupeFilter

class Scheduler:
    """
    Jcrapy Scheduler.

    Scheduler uses two PriorityQueue instances, configured to work in-memory
    and on-disk (optional). When on-disk queue is present, it is used by
    default, and an in-memory queue is used as a fallback for cases where
    a disk queue can't handle a request (can't serialize it).

    :setting:`SCHEDULER_MEMORY_QUEUE` and
    :setting:`SCHEDULER_DISK_QUEUE` allow to specify lower-level queue classes
    which PriorityQueue instances would be instantiated with, to keep requests
    on disk and in memory respectively.

    Overall, Scheduler is an object which holds several PriorityQueue instances
    (in-memory and on-disk) and implements fallback logic for them.
    Also, it handles dupefilters.
    """
    def __init__(self, dupefilter, crawler=None):
        self.df = dupefilter
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dupefilter = RFPDupeFilter.from_settings(settings)
        return cls(dupefilter, crawler=crawler)

    def open(self, spider):
        self.spider = spider
        return self.df.open()
