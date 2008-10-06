#!/usr/bin/env python
# RETIRED
print """
/Sketches/filereading/Chassis:

 This file has been retired.
 It is retired because it is now part of the main code base.
 If you want to use this, you should be using Kamaelia.Chassis.Carousel
 
 This file now deliberately exits to encourage you to fix your code :-)
"""

import sys
sys.exit(0)
#

import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, newComponent


class Carousel(component):
    """Encapsulates a changing carousel of components. The current component is wired
       such that it's inbox and outbox are exported  as "inbox" and "outbox".
       When the component emits producerFinished on its 'signal' output, a 'next' message is
       sent from 'requestNext'.

       Whenever arguments are received on 'next' eg. (but not necessarily) in response to
       a 'next' request, the components are destroyed and replaced with new ones, created
       with the arguments specified.

       After initialisation, Carousel will wait for the first  set of instructions, unless you
       set the make1stRequest argument, in which case it will issue a 'next' request immediately

       A factory method that takes a single argument should be supplied to create the components
       for the carousel.
       If you want to support more complex argument forms, you'll need to put a wrapper in.
    """

    Inboxes = { "inbox" : "child's inbox",
                "next" : "single argument for factory method new child component",
                "control" : "",
                "_control" : "for child to signal 'producerFinished' or 'shutdownMicroprocess' to Carousel"
              }
    Outboxes = { "outbox" : "child's outbox",
                 "signal" : "",
                 "_signal" : "for signalling 'shutdownMicroprocess' to child",
                 "requestNext" : "for requesting new child component"
               }

    def __init__(self, componentFactory, make1stRequest=False):
        super(Carousel, self).__init__()
        
        self.factory = componentFactory
        self.childDone = False

        self.make1stRequest = make1stRequest

        
    def main(self):
        if self.make1stRequest:
            self.requestNext()
        
        while not self.shutdown():
            self.handleFinishedChild()
            
            yield 1  # gap important - to allow shutdown messages to propogate to the child
            
            yield self.handleNewChild()

        self.unplugChildren()
#        print"Carousel done"
            
    def requestNext(self):
#        print "REQUESTING NEXT"
        self.send( "NEXT", "requestNext" )
    


    def handleFinishedChild(self):
        if self.dataReady("_control"):
            msg = self.recv("_control")

            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                if not self.childDone:
                    self.childDone = True
                    self.requestNext()
                self.unplugChildren()

    

    def handleNewChild(self):
        if self.dataReady("next"):
            arg = self.recv("next")

            # purge old child and any control messages that may have come from the old child
            while self.dataReady("_control"):
                self.recv("_control")

            self.unplugChildren()

            # create new child
            newChild = self.factory(arg)
            self.addChildren( newChild )
            
            # set flag for handleFinishedChild's sake
            self.childDone = False

            # wire it in
            self.link( (self,     "inbox"),   (newChild, "inbox"),  passthrough=1 )
            self.link( (self,     "_signal"), (newChild, "control")  )
            
            self.link( (newChild, "outbox"),  (self,     "outbox"), passthrough=2 )
            self.link( (newChild, "signal"),  (self,     "_control") )
            
            # return it to be yielded
            return newComponent(*(self.children))
        return 1


    def unplugChildren(self):
        for child in self.childComponents():
            self.send( shutdownMicroprocess(self), "_signal" )
            self.postoffice.deregisterlinkage(thecomponent=child)
            self.removeChild(child)


    def shutdown(self):
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send( msg, "signal")
                return True
        return False


if __name__ == "__main__":
    pass
