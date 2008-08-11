#!/usr/bin/env python

import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class Router(component):
    """\
    Router([(rule,dest)][,(rule,dest)]...) -> new Router component.
    
    Component that routes incoming messages to destination outboxes according to
    whether or not they pass the specified rules.
    """
    def __init__(self, *routing):
        for (rule,destination) in routing:
            self.Outboxes[destination] = "Routing destination"
        
        super(Router,self).__init__()
        self.routing = routing
        
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return True
        return False
        
    def main(self):
        while not self.shutdown():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                for (rule,destination) in self.routing:
                    if rule(data):
                        self.send(data,destination)
            self.pause()
            yield 1

class TwoWaySplitter(Axon.Component.component):
    Outboxes = { "outbox"  : "",
                 "outbox2" : "",
                 "signal"  : "",
                 "signal2" : "",
               }

    def main(self):
        done=False
        while not done:

            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.send(data, "outbox")
                self.send(data, "outbox2")

            while self.dataReady("control"):
                data = self.recv("control")
                self.send(data, "signal")
                self.send(data, "signal2")
                if isinstance(data, (producerFinished, shutdownMicroprocess)):
                    return

            self.pause()
            yield 1

class ConditionalSplitter(Axon.Component.component): # This is a data tap/siphon/demuxer
    Outboxes = ["true", "false"]
    def condition(self, data): return True
    def true(self,data): self.send(data, "true")
    def false(self,data): self.send(data, "false")
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if self.condition(data):
                    self.true(data)
                else:
                    self.false(data)
            if not self.anyReady():
                self.pause()
            yield 1
