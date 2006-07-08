#!/usr/bin/env python

# service wrapper
# wrapper that turns something into a service


from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

def Service(component, services):
    cat = CAT.getcat()
    for (name, boxname) in services.items():
        
        try:
            cat.registerService(name, component, boxname)
        except ServiceAlreadyExists, e:
            print "***************************** ERROR *****************************"
            print "An attempt to reuse service names happened."
            print "This is incorrect usage."
            print 
            traceback.print_exc(3)
            print "***************************** ERROR *****************************"

            raise e

    return component


class Subscribe(component):
    """\
    Subscribes to a service, and forwards what it receives to its outbox.
    Also forwards anything that arrives at its inbox to its outbox.
    
    Unsubscribes when shutdown.
    """
        
    Outboxes = { "outbox"     : "",
                 "signal"     : "shutdown signalling",
                 "_toService" : "request to service",
               }
        
    def __init__(self, servicename, *requests):
        """\
        Subscribe to the specified service, wiring to it, then sending the specified messages.
        Requests are of the form ("ADD", request, destination)
        """
        super(Subscribe,self).__init__()
        self.servicename = servicename
        self.requests    = requests
        
        
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False
    
    
    def main(self):
        
        cat = CAT.getcat()
        service = cat.retrieveService(self.servicename)
        linkage = self.link((self,"_toService"),service)
        
        # subscribe
        for request in self.requests:
            self.send( ("ADD", request, (self,"inbox")) , "_toService")
            
        # now go quiescent and simply forward data
        shutdown=False
        while not shutdown:
            while self.dataReady("inbox"):
                self.send(self.recv("inbox"), "outbox")
                
            shutdown = self.shutdown()
            
            self.pause()
            yield 1
        
        # unsubscribe
        for request in self.requests[-1:-len(self.requests)-1:-1]:
            self.send( ("REMOVE", request, (self,"inbox")) , "_toService")
            

if __name__ == "__main__":
    
    from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
    
    class DummyService(AdaptiveCommsComponent):
        def main(self):
            outboxes = {}
            linkages = {}
            params   = {}
            
            while 1:
                while self.dataReady("inbox"):
                    req = self.recv("inbox")
                    if req[0] == "ADD":
                        param, dest = req[1],req[2]
                        outboxes[dest] = self.addOutbox("outbox")
                        linkages[dest] = self.link( (self,outboxes[dest]), dest)
                        params[dest] = param
                        
                for dest in params.keys():
                    self.send( params[dest], outboxes[dest] )
                    
                yield 1
                
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import pipeline
    
    pipeline( Subscribe("SERVICE1", 5),
              ConsoleEchoer(),
            ).activate()
    
    pipeline( Subscribe("SERVICE1", 1),
              ConsoleEchoer(),
            ).activate()
    
    Service(DummyService(), {"SERVICE1":"inbox"}).run()
    