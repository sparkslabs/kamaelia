import Axon

class TransformerSplitter(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Outboxes = {"outbox" : "",
                "signal" : "",
                "rejects" : ""
               }
    def __init__(self, filters=()):
        super(TransformerSplitter, self).__init__()
        self.filters = filters
        for filter in self.filters:
            self.addOutbox(filter[1])

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                rejected = True
                for filter in self.filters:
                    data, send = filter[0](data)
                    if send:
                        rejected = False
                        self.send(data, filter[1])
                        break
                if rejected:
                    self.send(data, "rejects")
            if not self.anyReady():
                self.pause()
            yield 1

