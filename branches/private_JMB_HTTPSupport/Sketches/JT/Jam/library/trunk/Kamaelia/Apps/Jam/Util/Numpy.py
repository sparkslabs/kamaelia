import Axon

class TypeConverter(Axon.Component.component):
    type = None
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                if self.type != None:
                    self.send(data.astype(self.type), "outbox")
            if not self.anyReady():
                self.pause()
            yield 1
