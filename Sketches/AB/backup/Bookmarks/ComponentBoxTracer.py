#!/usr/bin/python

import Axon
class ComponentBoxTracer(Axon.Component.component):
    Inboxes = {
        "inbox" : "As usual",
        "control": "As usual",
        "_from_outbox" : "Data from wrapped component's outbox 'outbox'",
        "_from_signal" : "Data from wrapped component's outbox 'signal'",
    }
    Outboxes = {
        "outbox" : "As usual",
        "signal": "As usual", 
        "_to_inbox" : "Data from 'inbox' is sent to the wrapped component's inbox 'outbox' here",
        "_to_control" : "Data from 'inbox' is sent to the wrapped component's inbox 'outbox' here",
        "_to_tracer_inbox" : "Tracing information is sent to this inbox",
        "_to_tracer_control" : "Shutdown information gets sent here",
    }
     
    def __init__(self, traced, tracer, **argd):
        super(ComponentBoxTracer, self).__init__(**argd)
        self.traced = traced
        self.tracer = tracer

    def main(self):
        self.link((self,"_to_inbox"),(self.traced,"inbox"))
        self.link((self,"_to_control"),(self.traced,"control"))
        self.link((self.traced,"outbox"),(self,"_from_outbox"))
        self.link((self.traced,"signal"),(self,"_from_signal"))

        self.link((self,"_to_tracer_inbox"), (self.tracer,"inbox"))
        self.link((self,"_to_tracer_control"), (self.tracer,"control"))

        self.addChildren(self.traced,self.tracer)
        self.traced.activate()
        self.tracer.activate()
        childDone = False
        while not childDone:
            if not self.anyReady():
                self.pause()
            yield 1
            
            for data in self.Inbox("inbox"):
                self.send(data, "_to_inbox")
                self.send(["inbox", data], "_to_tracer_inbox")

            for data in self.Inbox("control"):
                self.send(data, "_to_control")
                self.send(["control", data], "_to_tracer_inbox")

            for data in self.Inbox("_from_outbox"):
                self.send(data, "outbox")
                self.send(["outbox", data], "_to_tracer_inbox")

            for data in self.Inbox("_from_signal"):
                self.send(data, "signal")
                self.send(["signal", data], "_to_tracer_inbox")

            if self.traced._isStopped():
                self.removeChild(self.traced) # deregisters all linkages as well
                childDone = True
                self.send(Axon.Ipc.producerFinished(), "_to_tracer_control")
                self.removeChild(self.tracer) # deregisters all linkages as well

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.PureTransformer import PureTransformer
    from Kamaelia.Util.Console import ConsoleEchoer
    
    Pipeline(
        DataSource([1,2,3,4]),
        ComponentBoxTracer(
            PureTransformer(lambda x: str(x) + str(x+1) + "\n"),
            Pipeline(
                PureTransformer(lambda x: repr(x) + "\n"),
                ConsoleEchoer(),
            ),
        ),
        ConsoleEchoer(),
    ).run()


