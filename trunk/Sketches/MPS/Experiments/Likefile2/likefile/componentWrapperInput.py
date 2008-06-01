#!/usr/bin/env python
#
# Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Axon.ThreadedComponent import threadedadaptivecommscomponent
from Axon.AxonExceptions import noSpaceInBox
import Queue
import threading
import Axon.Ipc

# queuelengths = 0

DEFIN = ["inbox", "control"]
DEFOUT = ["outbox", "signal"]

def addBox(names, boxMap, addBox): # XXX REVIEW: Using the function name as a parameter name
        """Add an extra wrapped box called name, using the addBox function provided
        (either self.addInbox or self.addOutbox), and adding it to the box mapping
        which is used to coordinate message routing within component wrappers."""
        for boxname in names:
            if boxname in boxMap:
                raise ValueError, "%s %s already exists!" % (direction, boxname) # XXX REVIEW: *direction* doesn't actually exist. If this appeared in any other line besides a "raise..." line this would be a problem.
            realboxname = addBox(boxname)
            boxMap[boxname] = realboxname

class componentWrapperInput(threadedadaptivecommscomponent):
    """A wrapper that takes a child component and waits on an event from the foreground, to signal that there is 
    queued data to be placed on the child's inboxes."""
    def __init__(self, child, inboxes = DEFIN):
        super(componentWrapperInput, self).__init__()
        self.child = child

        # This is a map from the name of the wrapped inbox on the child, to the
        # Queue used to convey data into it.
        self.inQueues = dict()

        # This queue is used by the foreground to tell us what queue it has sent us
        # data on, so that we do not need to check all our input queues,
        # and also so that we can block on reading it.
        self.whatInbox = Queue.Queue()
        self.isDead = threading.Event()


        # This sets up the linkages between us and our child, avoiding extra
        # box creation by connecting the "basic two" in the same way as, e.g. a pipeline.
        self.childInboxMapping = dict()
        addBox(inboxes, self.childInboxMapping, self.addOutbox)
        for childSink, parentSource in self.childInboxMapping.iteritems():
            self.inQueues[childSink] = Queue.Queue(self.queuelengths)
            self.link((self, parentSource),(self.child, childSink))

        # This outbox is used to tell the output wrapper when to shut down.
        self.deathbox = self.addOutbox(str(id(self)))

    def main(self):
        while True:
            whatInbox = self.whatInbox.get()
            if not self.pollQueue(whatInbox):
                # a False return indicates that we should shut down.
                self.isDead.set()
                # tells the foreground object that we've successfully processed a shutdown message.
                # unfortunately, whether the child honours it or not is a matter of debate.
                self.send(object, self.deathbox)
                return

    def pollQueue(self, whatInbox):
        """This method checks all the queues from the outside world, and forwards any waiting data
        to the child component. Returns False if we propogated a shutdown signal, true otherwise."""
        parentSource = self.childInboxMapping[whatInbox]
        queue = self.inQueues[whatInbox]
        while not queue.empty():
            if not self.outboxes[parentSource].isFull():
                msg = queue.get_nowait() # won't fail, we're the only one reading from the queue.
                try:
                    self.send(msg, parentSource)
                except noSpaceInBox, e:
                    raise "Box delivery failed despite box (earlier) reporting being not full. Is more than one thread directly accessing boxes?"
                if isinstance(msg, (Axon.Ipc.shutdownMicroprocess, Axon.Ipc.producerFinished)):
                    print "Quietly dieing?"
                    return False
            else:
                # if the component's inboxes are full, do something here. Preferably not succeed.
                break
        return True

if __name__ == "__main__":
    print "Needs testing code"
