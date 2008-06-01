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

from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
import Axon.Ipc
import Queue

queuelengths = 0

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


class componentWrapperOutput(AdaptiveCommsComponent):
    """A component which takes a child component and connects its outboxes to queues, which communicate
    with the likefile component."""
    def __init__(self, child, inputHandler, outboxes = DEFOUT):
        super(componentWrapperOutput, self).__init__()
        self.queuelengths = queuelengths
        self.child = child
        self.addChildren(self.child)

        # This queue maps from the name of the outbox on the child which is to be wrapped,
        # to the Queue which conveys that data to the foreground thread.
        self.outQueues = dict()

        # set up notification from the input handler to kill us when appropriate.
        # we cannot rely on shutdown messages being propogated through the child.
        self.isDead = inputHandler.isDead
        self.deathbox = self.addInbox(str(id(self)))
        self.link((inputHandler, inputHandler.deathbox), (self, self.deathbox))

        # This sets up the linkages between us and our child, avoiding extra
        # box creation by connecting the "basic two" in the same way as, e.g. a pipeline.
        self.childOutboxMapping = dict()
        addBox(outboxes, self.childOutboxMapping, self.addInbox)

        for childSource, parentSink in self.childOutboxMapping.iteritems():
            self.outQueues[childSource] = Queue.Queue(self.queuelengths)
            self.link((self.child, childSource),(self, parentSink))

    def main(self):
#        print "componentWrapperOutput", self.child
        self.child.activate()
        while True:
            self.pause()
            yield 1
            self.sendPendingOutput()
            if self.dataReady(self.deathbox):
                return


    def sendPendingOutput(self):
        """This method will take any outgoing data sent to us from a child component and stick it on a queue 
        to the outside world."""
        for childSource, parentSink in self.childOutboxMapping.iteritems():
            queue = self.outQueues[childSource]
            while self.dataReady(parentSink):
                if not queue.full():
                    msg = self.recv(parentSink)
                    # TODO - what happens when the wrapped component terminates itself? We keep on going. Not optimal.
                    queue.put_nowait(msg)
                else:
                    break
                    # permit a horrible backlog to build up inside our boxes. What could go wrong?




if __name__ == "__main__":
    print "Needs better testing"
