from queuelib import queue

def _jcrapy_non_serialization_queue(queue_class):

    class JcrapyRequestQueue(queue_class):
        @classmethod
        def from_crawler(cls, crawler, *args, **kwargs):
            return cls()

    return  JcrapyRequestQueue

LifoMemoryQueue = _jcrapy_non_serialization_queue(queue.LifoMemoryQueue)