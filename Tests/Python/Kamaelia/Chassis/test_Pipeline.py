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
#
# test suite for Pipeline

import unittest

from Kamaelia.Chassis.Pipeline import Pipeline

from Axon.Component import component
from Axon.Scheduler import scheduler
from Axon.Ipc import producerFinished, shutdownMicroprocess

class MockChild(component):

    def __init__(self):
        super(MockChild,self).__init__()
        self._stopNow = False
        self.wasActivated=False

    def stopNow(self):
        self._stopNow = True
        
    def main(self):
        self.wasActivated=True
        while not self._stopNow:
            yield 1

class Dummy(component):
    def main(self):
        while 1:
            yield 1



class Test_Pipeline(unittest.TestCase):

    def setup_test(self, *children, **otherargs):
        self.setup_initialise(*children,**otherargs)
        self.setup_activate()

    def setup_initialise(self,*children,**otherargs):
        self.children=children[:]

        self.scheduler = scheduler()
        scheduler.run = self.scheduler

            
        self.pipeline = Pipeline(*children, **otherargs)

        self.inSrc = Dummy()
        self.inSrc.link((self.inSrc,"outbox"), (self.pipeline,"inbox"))
        self.inSrc.link((self.inSrc,"signal"), (self.pipeline,"control"))
        
        self.outDest = Dummy()
        self.outDest.link((self.pipeline,"outbox"), (self.outDest,"inbox"))
        self.outDest.link((self.pipeline,"signal"), (self.outDest,"control"))
        
        self.run = self.scheduler.main()

    def setup_activate(self):
        self.pipeline.activate(Scheduler=self.scheduler)
        self.inSrc.activate(Scheduler=self.scheduler)
        self.outDest.activate(Scheduler=self.scheduler)


        
    def sendToInbox(self,data):
        self.inSrc.send(data,"outbox")

    def sendToControl(self,data):
        self.inSrc.send(data,"signal")

    def dataReadyOutbox(self):
        return self.outDest.dataReady("inbox")

    def dataReadySignal(self):
        return self.outDest.dataReady("control")

    def recvOutbox(self):
        return self.outDest.recv("inbox")

    def recvSignal(self):
        return self.outDest.recv("control")

    def collectOutbox(self):
        out=[]
        while self.dataReadyOutbox():
            out.append(self.recvOutbox())
        return out

    def collectSignal(self):
        out=[]
        while self.dataReadySignal():
            out.append(self.recvSignal())
        return out

    def runFor(self, cycles):
        numcycles=cycles*(3+len(self.children))    # approx this many components in the system
        for i in range(0,numcycles): self.run.next()


    def test_PipelineActivatesChildrenOnlyWhenActivated(self):
        """Children are activated as soon as the Pipeline itself is activated, but no sooner."""
        self.setup_initialise(MockChild(), MockChild(), MockChild())

        for child in self.children:
            self.assert_(not child.wasActivated)

        self.setup_activate()
        self.runFor(cycles=1)
        self.runFor(cycles=3)
        
        for child in self.children:
            self.assert_(child.wasActivated)

    def test_PipelineTerminatesOnlyWhenAllChildrenHaveTerminated(self):
        self.setup_test(MockChild(), MockChild(), MockChild())

        self.runFor(cycles=100)

        self.assert_(not self.pipeline._isStopped())
        for child in self.children:
            self.assert_(not self.pipeline._isStopped())

        # stop each child one at a time, and check that it is the only thing to
        # have stopped
        for child in self.children:
            
            # check the pipeline is still running
            self.assert_(not self.pipeline._isStopped())

            child.stopNow()
            self.runFor(cycles=100)

        # by now the pipeline should have stopped too
        self.assert_(self.pipeline._isStopped())

    def test_PipelineChildrenWiredOutboxInbox(self):
        """Pipeline wires up children so one child's "outbox" outbox feeds to the next's "inbox" inbox."""
        self.setup_test(MockChild(), MockChild(), MockChild(), MockChild())

        self.runFor(cycles=100)

        MSG = object()
        self.children[0].send(MSG, "outbox")
        
        for child in self.children[1:-1]:  # all except first and last
            # expect to have received:
            self.assert_(child.recv("inbox") == MSG)
            # now send
            MSG = object()
            child.send(MSG, "outbox")
            
        self.assert_(self.children[-1].recv("inbox") == MSG)

    def test_PipelineChildrenWiredSignalControl(self):
        """Pipeline wires up children so one child's "signal" outbox feeds to the next's "control" inbox."""
        self.setup_test(MockChild(), MockChild(), MockChild(), MockChild())

        self.runFor(cycles=100)

        MSG = object()
        self.children[0].send(MSG, "signal")
        
        for child in self.children[1:-1]:  # all except first and last
            # expect to have received:
            self.assert_(child.recv("control") == MSG)
            # now send
            MSG = object()
            child.send(MSG, "signal")
            
        self.assert_(self.children[-1].recv("control") == MSG)

    def test_PipelineFirstChildWiredToParentInboxes(self):
        """Pipeline wires up the first child's "inbox" and "control" inboxes to receive from the pipeline's "inbox" and "control" inboxes."""
        self.setup_test(MockChild(), MockChild(), MockChild(), MockChild())

        self.runFor(cycles=100)

        MSG = object()
        self.sendToInbox(MSG)
        self.assert_(self.children[0].recv("inbox")==MSG)

        MSG = object()
        self.sendToControl(MSG)
        self.assert_(self.children[0].recv("control")==MSG)

    def test_PipelineLastChildWiredToParentOutboxes(self):
        """Pipeline wires up the last child's "outbox" and "signal" outboxes to send out of the pipeline's "outbox" and "signal" outboxes."""
        self.setup_test(MockChild(), MockChild(), MockChild(), MockChild())

        self.runFor(cycles=100)

        MSG = object()
        self.children[-1].send(MSG,"outbox")
        self.assert_(self.recvOutbox()==MSG)

        MSG = object()
        self.children[-1].send(MSG,"signal")
        self.assert_(self.recvSignal()==MSG)

      
if __name__ == "__main__":
    unittest.main()
    