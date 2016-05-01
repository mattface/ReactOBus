import logging
import threading
import zmq

LOG = logging.getLogger("ReactOBus.lib.inputs")


class Input(threading.Thread):
    name = ""

    @classmethod
    def select(cls, classname, options):
        for sub in cls.__subclasses__():
            if sub.name == classname:
                return sub(options)
        raise NotImplementedError

    def setup(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class ZMQPull(Input):
    name = "ZMQPull"

    def __init__(self, options):
        super().__init__()
        self.url = options["url"]

    def setup(self):
        LOG.debug("Setting up %s", self.name)
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.PULL)
        LOG.debug("Listening on %s", self.url)
        self.sock.bind(self.url)

    def run(self):
        self.setup()
        while True:
            pass

    def __del__(self):
        # TODO: is it really useful to drop all messages
        self.sock.close(linger=0)
        self.context.term()