#!/usr/bin/env python

# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""\
================================================
Components to help build Services (EXPERIMENTAL)
================================================

These components make it easier to build and use public services, registered
with the Coordinating Assistant Tracker.

Note: These components are EXPERIMENTAL and are likely to under go substantial
change


Register Service
----------------

A function that registers specified inboxes on a component as named services
with the Coordinating Assistant Tracker (CAT). Returns the component, so can
be dropped in where you would ordinarily use a component.



Example Usage:
~~~~~~~~~~~~~~

Create and activate MyComponent instance, registering its "inbox" inbox with the
CAT as a service called "MyService"::
    
    RegisterService( MyComponent(), {"MyService":"inbox"} ).activate()
    
    

How does it work?
~~~~~~~~~~~~~~~~~

This method registers the component you provide with the CAT. It register the
inboxes on it that you specify using the names that you specify.



Subscibe To Service
-------------------

A component that connects to a public service and sends a fixed format message
to it requesting to subscribe to a set of 'things' it provides. 



Example Usage:
~~~~~~~~~~~~~~

Subscribe to a (fictional) "TV Channels Service", asking for three channels. The
tv channel data is then recorded::
    
    pipeline(
        SubscribeTo( "TV Channels Service", ["BBC ONE", "BBC TWO", "ITV"] ),
        RecordChannels(),
        ).run()

The message sent to the "TV Channels Service" will be::
    
    ("ADD", ["BBC ONE", "BBC TWO", "ITV"], ( <theSubscribeToComponent>, "inbox" ) )



How does it work?
~~~~~~~~~~~~~~~~~

Describe more detail here




Connect To Service
------------------

A component that connects to a public service. Any data you send to its inbox
gets sent to the service.



Example Usage
~~~~~~~~~~~~~
::
    
    pipeline( MyComponentThatSendMessagesToService(),
            ConnectTo("Name of service"),
            ).run()



How does it work?
~~~~~~~~~~~~~~~~~

Describe in more detail here.
"""

from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

def RegisterService(component, services):
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
            

class ToService(component):
    def __init__(self, toService):
        super(ToService,self).__init__()
        self.serviceName = toService
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False
    
    def main(self):
        cat = CAT.getcat()
        service = cat.retrieveService(self.serviceName)
        
        linkage = self.link( (self, "inbox"), service, passthrough=1 )
        
        shutdown=False
        while not shutdown:
            shutdown = self.shutdown()
            self.pause()
            yield 1
            


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
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    Pipeline( Subscribe("SERVICE1", 5),
              ConsoleEchoer(),
            ).activate()
    
    Pipeline( Subscribe("SERVICE1", 1),
              ConsoleEchoer(),
            ).activate()
    
    RegisterService(DummyService(), {"SERVICE1":"inbox"}).run()
    