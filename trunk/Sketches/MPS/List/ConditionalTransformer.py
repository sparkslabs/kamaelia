#!/usr/bin/python
# -*- coding: utf-8 -*-

import Axon
from Axon.AxonExceptions import normalShutdown

class ConditionalTransformer(Axon.Component.component): 
    Inboxes = {
        "inbox": "Messages matching condition reach us here",
        "control": "Shutdown messages reach us here",
    }
    Outboxes = {
        "outbox": "Any messages we send here are tagged on their way out the tagging processor as being from us",
        "signal": "We pass on shutdown messages here",
        "toprocessor" : "To subscribe to process messages",
    }
    condition=None
    process=None
    def __init__(self, processor=None, tag=None, condition=None, process=None,**argd):
        [ argd.__setitem__(k,i) for k,i in locals().iteritems() if (k != "self") and (i!=None)]
        super(ConditionalTransformer, self).__init__(**argd)
        if self.process is None:
            self.process = self.processMessage
        if self.condition is None:
            self.condition = self.shouldProcessMessage

    @staticmethod
    def shouldProcessMessage(message):
        return True

    @staticmethod
    def processMessage(message):
        return message

    def main(self):
        self.link((self,"toprocessor"), (self.processor, "processor"))
        yield 1
        request = ( self.tag, self.condition, self )
        self.send(request, "toprocessor")
        process = self.process
        try:
            while not self.dataReady("control"):
                for message in self.Inbox("inbox"):
                    self.send(process(message), "outbox")
                if not self.anyReady():
                    self.pause()
                yield 1
        except normalShutdown:
            pass
        if self.dataReady("control"):
            self.send(self.recv("control"), "signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

if __name__ == "__main__":
    from TaggingPluggableProcessor import TaggingPluggableProcessor
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Util.PureTransformer import PureTransformer

    TPP = TaggingPluggableProcessor()

    Pipeline(ConsoleReader(),
             PureTransformer(lambda x: int(x)),
             TPP,
             ConsoleEchoer()).activate()

    ConditionalTransformer(TPP, "EVEN", lambda x: x % 2==0, lambda x: "Even ! " + str(x)).activate()

    def isodd(x): return x % 2==1
    def format_as_odd(x): return "Odd ! " + str(x)

    ConditionalTransformer(TPP, "ODD", isodd, format_as_odd).activate()

    class Divisible3(ConditionalTransformer):
       @staticmethod
       def condition(x):
           return x % 3 == 0
       @staticmethod
       def process(x):
           return "Divisible by 3 ! " + str(x)

    class Divisible(ConditionalTransformer):
        divisor = 4
        
        def shouldProcessMessage(self, message):
            return (message % self.divisor) == 0

        def processMessage(self, message):
            return "Divisible by "+str(self.divisor) + " ! " + str(message)

    Divisible3(TPP, "THREE").activate()
    Divisible(TPP, "FOUR").activate()
    Divisible(TPP, "FIVE", divisor = 5).run()

