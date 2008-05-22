import Axon

class Forwarder(Axon.Component.component):
        Inboxes = {
                "inbox"             : "Received messages are forwarder to outbox",
                "secondary-inbox"   : "Received messages are forwarder to outbox",
                "control"           : "Received messages are forwarder to signal",
                "secondary-control" : "Received messages are forwarder to signal",
        }
        def __init__(self, **argv):
                super(Forwarder, self).__init__(**argv)

        def main(self):
                while True:
                        while self.dataReady("inbox"):
                                data = self.recv("inbox")
                                self.send(data,"outbox")

                        while self.dataReady("secondary-inbox"):
                                data = self.recv("secondary-inbox")
                                self.send(data,"outbox")

                        while self.dataReady("control"):
                                data = self.recv("control")
                                self.send(data, "signal")
                                return

                        while self.dataReady("secondary-control"):
                                data = self.recv("secondary-control")
                                self.send(data, "signal")
                                return

                        if not self.anyReady():
                                self.pause()
                        yield 1
