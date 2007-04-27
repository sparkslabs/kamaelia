#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
Component Carousel Chassis.

This chassis component is for making a carousel of components. It gets its name
from a broadcast carousel - where a programme (or set of programmes) is
broadcast one after another, often on a loop. Alternatively, think of public
information screens which display a looping carousel of slides of information.

You gain reusability from things that are not directly reusable and normally
come to a halt. For example, make a carousel of file reader components, and you
can read from more than one file, one after another. The carousel will make a
new file reader component every time you make new request.

The Carousel automatically sends a "NEXT" message when a component finishes, to
prompt you make a new request.



EXAMPLE USAGE : A reusable file reader

    def makeFileReader(filename):
        return ReadFileAdapter(filename = filename, ...other args... )

    reusableFileReader = Carousel componentFactory = makeFileReader)

Whenever you send a filename to the "next" inbox of the reusableFileReader
component, it will read that file. You can do this as many times as you wish.



HOW DOES IT WORK?

The carousel chassis creates and encapsulates (as a child) the component you
want it to, and lets it get on with it.

Anything sent to the carousel's "inbox" inbox is passed onto the child
component. Anything the child sends out appears at the carousel's "outbox" and
"signal" outboxes.

If the child sends an Axon.Ipc.shutdownMicroprocess or Axon.Ipc.producerFinished
message then the carousel gets rid of that component and sends a "NEXT" message
to its "requestNext" outbox. It does not pass the message on.

Another component, such as a Chooser, can respond to this message by sending
the new set of arguments (for the factory function) to the carousel's "next"
inbox. The carousel then uses your factory function to create a new child
component. This way, a sequence of operations can be automatically chained
together.

If the argument source needs to receive a "NEXT" message before sending its
first set of arguments, then set the argument make1stRequest=True when creating
the carousel.

You can send new orders to the "next" inbox at any time. The carousel will
immediately unwire that child (and create the new one) and ask the old child to
shut down by sending an Axon.Ipc.shutdownMicroprocess message to its "control"
inbox.

The carousel will shutdown in response to an Axon.Ipc.shutdownMicroprocess or
Axon.Ipc.producerFinished message. It will also terminate any child component
in the same way as described above.

"""

import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, newComponent


class Carousel(component):
    """
    Carousel(componentFactory,[make1stRequest]) -> new Carousel component
        
    Create a Carousel component that makes child components one at a time
    (in carousel fashion) using the supplied factory function.

    Keyword arguments:
    componentFactory -- function that takes a single argument and returns a component
    make1stRequest -- if True, Carousel will send an initial "NEXT" request. (default=False)
    """

    Inboxes = { "inbox"    : "child's inbox",
                "next"     : "requests to replace child",
                "control"  : "",
                "_control" : "internal use: to receive 'producerFinished' or 'shutdownMicroprocess' from child"
              }
    Outboxes = { "outbox"      : "child's outbox",
                 "signal"      : "",
                 "_signal"     : "internal use: for sending 'shutdownMicroprocess' to child",
                 "requestNext" : "for requesting new child component"
               }

    def __init__(self, componentFactory, make1stRequest=False):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Carousel, self).__init__()
        
        self.factory = componentFactory
        self.childDone = False

        self.make1stRequest = make1stRequest

        
    def main(self):
        """Main loop"""
        if self.make1stRequest:
            self.requestNext()
        
        while not self.shutdown():
            self.handleFinishedChild()
            
            yield 1  # gap important - to allow shutdown messages to propogate to the child
            
            yield self.handleNewChild()
            
            if not self.dataReady("next") and not self.dataReady("control") and not self.dataReady("_control"):
                self.pause()
        
        self.unplugChildren()

            
    def requestNext(self):
        """Sends 'next' out the 'requestNext' outbox"""
        self.send( "NEXT", "requestNext" )
    


    def handleFinishedChild(self):
        """
        Unplugs the child if a shutdownMicroprocess or producerFinished message is
        received from it. Also sends a "NEXT" request if one has not already been sent.
        """
        if self.dataReady("_control"):
            msg = self.recv("_control")

            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                if not self.childDone:
                    self.childDone = True
                    self.requestNext()
                self.unplugChildren()

    

    def handleNewChild(self):
        """
        If data received on "next" inbox, removes any existing child and creates and wires
        in a new one.

        Received data is passed as an argument to the factory function (supplied at
        initialisation) that creates the new child.
        """
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
        """
        Sends 'shutdownMicroprocess' to children and unwires and disowns them.
        """
        for child in self.childComponents():
            self.send( shutdownMicroprocess(self), "_signal" )
            self.unlink(thecomponent=child)
            self.removeChild(child)


    def shutdown(self):
        """
        Returns True if a shutdownMicroprocess or producerFinished message was received.
        """
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send( msg, "signal")
                return True
        return False


__kamaelia_components__ = ( Carousel, )

if __name__ == "__main__":
    pass
