#!/usr/bin/env python

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

