from Axon.Component import component

class PureTransformer(component):
    def __init__(self, function=None):
        super(PureTransformerComponent, self).__init__()
        if function:
            self.processMessage = function
        
    def processMessage(self, msg):
        pass
        
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                returnval = self.processMessage(self.recv("inbox"))
                if returnval != None:
                    self.send(returnval, "outbox")
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), "signal")
                    return
            self.pause()
