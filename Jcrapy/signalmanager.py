from pydispatch import dispatcher

class SignalManager:

    def __init__(self, sender=dispatcher.Anonymous):
        self.sender = sender

    def connect(self, receiver, signal, **kwargs):
        """
        Connect a receiver function to a signal.

        The signal can be any object, although Jcrapy comes with some
        predefined signals that are documented in the :ref:`topics-signals`
        section.

        :param receiver: the function to be connected
        :type receiver: callable

        :param signal: the signal to connect to
        :type signal: object
        """
        kwargs.setdefault('sender', self.sender)
        return dispatcher.connect(receiver, signal, **kwargs)