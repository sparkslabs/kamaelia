from Axon.Component import component

"""\
=================
Pure Transformer component
=================

This component applies a function specified at its creation to messages received (a filter).

Example Usage
-------------

To read in lines of text, convert to upper case and then write to the console.
pipeline(
    ConsoleReader(),
    PureTransformer(lambda x : x.upper()),
    ConsoleEchoer()
).run()
"""

class PureTransformer(component):
    def __init__(self, function=None):
        super(PureTransformer, self).__init__()
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
