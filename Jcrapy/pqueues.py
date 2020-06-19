
from Jcrapy.utils.misc import create_instance
class JcrapyPriorityQueue:
    """A priority queue implemented using multiple internal queues (typically,
    FIFO queues). It uses one internal queue for each priority value. The internal
    queue must implement the following methods:

        * push(obj)
        * pop()
        * close()
        * __len__()

    ``__init__`` method of JcrapyPriorityQueue receives a downstream_queue_cls
    argument, which is a class used to instantiate a new (internal) queue when
    a new priority is allocated.

    Only integer priorities should be used. Lower numbers are higher
    priorities.

    startprios is a sequence of priorities to start with. If the queue was
    previously closed leaving some priority buckets non-empty, those priorities
    should be passed in startprios.

    """    
    @classmethod
    def from_crawler(cls, crawler, downstream_queue_cls, key, startprios=()):
        return cls(crawler, downstream_queue_cls, key, startprios)

    def __init__(self, crawler, downstream_queue_cls, key, startprios=()):
        self.crawler = crawler
        self.downstream_queue_cls = downstream_queue_cls
        self.key = key
        self.queues = {}
        self.curprio = None
        self.init_prios(startprios)

    def init_prios(self, startprios):
        if not startprios:
            return 

    def pop(self):
        if self.curprio is None:
            return
        q = self.queues[self.curprio]
        m = q.pop()
        if not q:
            del self.queues[self.curprio]
            q.close()
            prios = [p for p, q in self.queues.items() if q]
            self.curprio = min(prios) if prios else None
        return m

    def qfactory(self, key):
        return create_instance(self.downstream_queue_cls,
                                None,
                                self.crawler,
                                self.key + '/' +str(key))

    def priority(self, request):
        return -request.priority

    def push(self, request):
        priority = self.priority(request)
        if priority not in self.queues:
            self.queues[priority] = self.qfactory(priority)
        q = self.queues[priority]
        q.push(request) # this may fail(eg. serialization error)
        if self.curprio is None or priority < self.curprio:
            self.curprio = priority


