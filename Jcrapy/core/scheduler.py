from Jcrapy.utils.misc import load_object, create_instance

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
        self.pqclass = pqclass
        self.mqclass = mqclass
        self.crawler = crawler


    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = create_instance(dupefilter_cls, settings, crawler)
        pqclass = load_object(settings['SCHEDULER_PRIORITY_QUEUE'])
        mqclass = load_object(settings['SCHEDULER_MEMORY_QUEUE'])
        return cls(dupefilter, pqclass=pqclass, mqclass=mqclass, crawler=crawler)

    def open(self, spider):
        self.spider = spider
        self.mqs = self._mq()
        return self.df.open()
    def next_request(self):
        request = self.mqs.pop()
        print('Scheduler.next_request')
        return

    def __len__(self):
        print('Scheduler.__len__')

    def _mq(self):
        """ Create a new priority queue instance, with in-memory storage """
        return create_instance(self.pqclass,
                               settings=None,
                               crawler=self.crawler,
                               downstream_queue_cls=self.mqclass,
                               key='')        
