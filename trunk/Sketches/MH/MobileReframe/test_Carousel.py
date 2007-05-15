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

# test suite for Carousel

import unittest

#from Kamaelia.Chassis.Carousel import Carousel
from CarouselRewrite import Carousel

from Axon.Component import component
from Axon.Scheduler import scheduler
from Axon.Ipc import producerFinished, shutdownMicroprocess

class MockChild(component):

    def __init__(self, childList, arg=None):
        super(MockChild,self).__init__()
        self.arg=arg
        self.stopNow = False
        childList.append(self)
        self.wasActivated=False

    def main(self):
        self.wasActivated=True
        while not self.stopNow:
            yield 1

class Dummy(component):
    def main(self):
        while 1:
            yield 1

class Test_Carousel(unittest.TestCase):

    def setup_test(self, **args):
        self.children=[]

        self.scheduler = scheduler()
        scheduler.run = self.scheduler

        if "componentFactory" not in args:
            def defaultFactory(arg,parent=self):
                child = MockChild(self.children, arg)
                return child
        
            args["componentFactory"]=defaultFactory
            
        self.carousel = Carousel(**args)

        self.inSrc = Dummy()
        self.inSrc.link((self.inSrc,"outbox"), (self.carousel,"inbox"))
        self.inSrc.link((self.inSrc,"signal"), (self.carousel,"control"))
        
        self.outDest = Dummy()
        self.outDest.link((self.carousel,"outbox"), (self.outDest,"inbox"))
        self.outDest.link((self.carousel,"signal"), (self.outDest,"control"))
        
        self.nextFbk = Dummy()
        self.nextFbk.link((self.carousel,"requestNext"), (self.nextFbk,"inbox"))
        self.nextFbk.link((self.nextFbk,"outbox"), (self.carousel,"next"))

        self.carousel.activate(Scheduler=self.scheduler)
        self.inSrc.activate(Scheduler=self.scheduler)
        self.outDest.activate(Scheduler=self.scheduler)
        self.nextFbk.activate(Scheduler=self.scheduler)

        self.run = self.scheduler.main()

    def sendToInbox(self,data):
        self.inSrc.send(data,"outbox")

    def sendToControl(self,data):
        self.inSrc.send(data,"signal")

    def sendToNext(self,data):
        self.nextFbk.send(data,"outbox")

    def dataReadyOutbox(self):
        return self.outDest.dataReady("inbox")

    def dataReadySignal(self):
        return self.outDest.dataReady("control")

    def dataReadyRequestNext(self):
        return self.nextFbk.dataReady("inbox")

    def recvOutbox(self):
        return self.outDest.recv("inbox")

    def recvSignal(self):
        return self.outDest.recv("control")

    def recvRequestNext(self):
        return self.nextFbk.recv("inbox")

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

    def collectRequestNext(self):
        out=[]
        while self.dataReadyRequestNext():
            out.append(self.recvRequestNext())
        return out

    def runFor(self, cycles):
        numcycles=cycles*5    # approx this many components in the system
        for i in range(0,numcycles): self.run.next()



    def test_byDefaultDoesNothing(self):
        """Carousel initialises. By default it does nothing."""
        self.setup_test()

        self.runFor(cycles=100)

        self.assert_(self.children==[], "Carousel should create no children")
        self.assert_(not self.dataReadyOutbox(), "Carousel should have sent nothing to its 'outbox' outbox")
        self.assert_(not self.dataReadySignal(), "Carousel should have sent nothing to its 'signal' outbox")
        self.assert_(not self.dataReadyRequestNext(), "Carousel should have sent nothing to its 'requestNext' outbox")
        self.assert_(not self.carousel._isStopped(), "Carousel should still be running")
        
    def test_canAskToMake1stRequest(self):
        """If the make1stRequest argument is set to True at initialisation, Carousel sends a "NEXT" message out of its "requestNext" outbox after it has started up."""
        self.setup_test(make1stRequest=True)

        self.runFor(cycles=5)

        self.assert_(self.children==[], "Carousel should create no children")
        self.assert_(not self.dataReadyOutbox(), "Carousel should have sent nothing to its 'outbox' outbox")
        self.assert_(not self.dataReadySignal(), "Carousel should have sent nothing to its 'signal' outbox")
        self.assert_(self.collectRequestNext()==["NEXT"], "Carousel should have sent a single 'NEXT' to its 'requestNext' outbox")
        self.assert_(not self.carousel._isStopped(), "Carousel should still be running")

    def test_shutsDownWhenToldToAndIdle(self):
        """When idle, with no child; a shutdownMicroprocess or producerFinished message will cause Carousel to terminate."""
        for IPC in (producerFinished, shutdownMicroprocess):
            self.setup_test()
    
            self.runFor(cycles=100)
            self.sendToControl(IPC())
            self.assert_(not self.carousel._isStopped(), "Carousel should still be running")
            self.runFor(cycles=100)
    
            got=self.collectSignal()
            self.assert_(len(got)==1 and isinstance(got[0],IPC), "Carousel should send a "+IPC.__class__.__name__+" message out its 'signal' outbox")
            self.assert_(self.carousel._isStopped(), "Carousel should have terminated")

    def test_messageToNextRunsFactoryFunction(self):
        """When a message is sent to the "next" inbox, the supplied factory function is run with that argument."""
        self.factoryRun=None
        def factory(arg):
            self.factoryRun=arg
            return Dummy()
        
        self.setup_test(componentFactory=factory)

        self.runFor(cycles=5)
        self.assert_(self.factoryRun==None)
        self.sendToNext("BLAH")
        self.runFor(cycles=5)
        self.assert_(self.factoryRun=="BLAH")
        
            
    def test_messageToNextSpawnsChild(self):
        """Messages sent to the "next" inbox trigger the factory function, leading to the creation and activation of a child component."""
        self.setup_test()
        self.runFor(cycles=5)
        self.sendToNext("BLAH")
        self.runFor(cycles=5)

        self.assert_(len(self.children)==1, "Carousel should have spawned a child in response to the 'next' request")
        self.assert_(self.children[-1].arg=="BLAH", "Carousel should have spawned child with the 'next' message as the argument")
        self.assert_(self.children[-1].wasActivated, "The child should have been activated")

    def test_childTerminationTriggersRequestNext(self):
        """When a child terminates; the Carousel sends a "NEXT" message out of its "requestNext" outbox."""
        self.setup_test()
        self.runFor(cycles=5)
        self.sendToNext("BLAH")
        self.runFor(cycles=5)

        self.children[-1].stopNow=True
        self.runFor(cycles=5)

        self.assert_(self.collectRequestNext()==["NEXT"], "Carousel should have sent a single 'NEXT' to its 'requestNext' outbox")
        
    def test_childShutdownSignalDoesntTriggerRequest(self):
        """If the child sends out a producerFinished or shutdownMicroprocess message out of its "signal" outbox; the Carousel does not send out a message from its "requestNext" outbox in response."""
        for IPC in (producerFinished,shutdownMicroprocess):
            self.setup_test()
            self.runFor(cycles=5)
            self.sendToNext("BLAH")
            self.runFor(cycles=5)
    
            self.children[-1].send(IPC(),"signal")
            self.runFor(cycles=50)
    
            self.assert_(self.collectRequestNext()==[], "Carousel should have not sent anything 'requestNext' outbox")
        
    def test_ChildReceivesShutdownSignal(self):
        """A shutdownMicroprocess or producerFinished message sent to the "control" inbox of the Carousel gets passed onto the "control" inbox of the child."""
        for IPC in (producerFinished,shutdownMicroprocess):
            self.setup_test()
            self.runFor(cycles=5)
            self.sendToNext("BLAH")
            self.runFor(cycles=5)
    
            self.sendToControl(IPC())
            self.runFor(cycles=50)
    
            self.assert_(self.children[-1].dataReady("control"), "Child should have received something on its 'control' inbox")
            msg=self.children[-1].recv("control")
            self.assert_(isinstance(msg,IPC), "Child should have received a "+IPC.__class__.__name__+" message out its 'control' inbox")
        
    def test_nextRequestStartsNewchildOnceCurrentHasTerminated(self):
        """A message sent to the "next" inbox starts a new child; but only once the current child has terminated."""
        self.setup_test()
        self.runFor(cycles=5)
        self.sendToNext("BLAH")
        self.runFor(cycles=5)

        for i in range(0,5):
            self.sendToNext("BLAH")
            self.runFor(cycles=50)
    
            self.assert_(len(self.children)==i+1, "The new child should not be created until the previous has terminated")
            self.children[-1].stopNow=True
            self.runFor(cycles=5)
            
            self.assert_(len(self.children)==i+2, "The 'next' message should have resulted in a new child")
            self.assert_(self.children[-2]._isStopped(), "The older child should by now be terminated")
            self.assert_(self.children[-1].wasActivated and not self.children[-1]._isStopped(), "The new child should be active and running")

    def test_dataReachesChildInbox(self):
        """Any messages sent to the "inbox" inbox of the Carousel gets sent on tot the "inbox" inbox of the child component."""
        self.setup_test()
        self.runFor(cycles=5)
        self.sendToNext("BLAH")
        self.runFor(cycles=1)

        for i in range(0,5):
            MSG = "HELLO"+str(i)
            self.sendToInbox(MSG)
            self.runFor(cycles=1)

            self.assert_(self.children[-1].dataReady("inbox"), "Something should have arrived at the inbox")
            self.assert_(self.children[-1].recv("inbox")==MSG, "The message sent to the Carousel's 'inbox' inbox should have reached the child's 'inbox' inbox")
        
            self.runFor(cycles=10)


    def test_dataReachesCarouselOutbox(self):
        """Any mesasges sent out of the "outbox" outbox of a child emerges from the "outbox" outbox of the Carousel."""
        self.setup_test()

        self.runFor(cycles=5)
        self.sendToNext("BLAH")
        self.runFor(cycles=2)

        for i in range(0,5):
            MSG = "HELLO"+str(i)
            self.children[-1].send(MSG,"outbox")
            self.runFor(cycles=1)

            self.assert_(self.collectOutbox()==[MSG], "The message sent to the child's 'outbox' outbox should have reached the Carousel's 'outbox' outbox")
        
            self.runFor(cycles=10)

    def test_childSignalIgnored(self):
        """Messages coming out of the child's "signal" outbox are ignored. They do not emerge from the "signal" outbox of the Carousel."""
        self.setup_test()

        self.runFor(cycles=5)
        self.sendToNext("BLAH")
        self.runFor(cycles=2)

        for MSG in (producerFinished,shutdownMicroprocess,"HELLO!"):
            self.children[-1].send(MSG,"signal")
            self.runFor(cycles=1)

            self.assert_(self.collectSignal()==[], "Any message sent to the child's 'signal' outbox should not have reached the Carousel's 'signal' outbox")
        
            self.runFor(cycles=10)

    def test_terminatingCarouselWithChildPassesSignalToChildToo(self):
        """If a producerFinshed or shutdownMicroprocess is sent to a Carousel's "control" inbox, it is passed onto the child's "control" inbox."""

        for IPC in (producerFinished,shutdownMicroprocess):
            self.setup_test()
            
            # create new child
            self.runFor(cycles=5)
            self.sendToNext("BLAH")
            self.runFor(cycles=50)

            # send shutdown to Carousel
            self.sendToControl(IPC())
            self.runFor(cycles=5)

            # did the child get it
            msg = self.children[-1].recv("control")
            self.assert_(isinstance(msg,IPC), "Child should also receive a "+IPC.__class__.__name__+" request")
            self.children[-1].stopNow=True
            self.runFor(cycles=5)
                
    def test_carouselDoesntTerminateUntilChildHas(self):
        """Carousel doesn't terminate (in response to producerFinished or shutdownMicroprocess) until the child has terminated."""

        for IPC in (producerFinished,shutdownMicroprocess):
            self.setup_test()
            
            # create new child
            self.runFor(cycles=5)
            self.sendToNext("BLAH")
            self.runFor(cycles=50)

            # send shutdown to Carousel
            self.sendToControl(IPC())
            self.runFor(cycles=50)

            # did the child get it
            msg = self.children[-1].recv("control")
            self.assert_(isinstance(msg,IPC), "Child should also receive a "+IPC.__class__.__name__+" request")

            # carousel and child should still be running
            self.assert_(not self.carousel._isStopped())
            self.assert_(not self.children[-1]._isStopped())
            
            self.children[-1].stopNow=True
            self.runFor(cycles=5)
            
            self.assert_(self.carousel._isStopped())
            self.assert_(self.children[-1]._isStopped())
                
    def test_queuedNextsFinishedIfProducerFinished(self):
        """If a producerFinished() is received, but there are still messages queued on the 'next' inbox, those messages are processed (and children created) first. *Then* the Carousel terminates."""
        
        self.setup_test()
        
        self.runFor(cycles=5)
        self.sendToNext("BLAH")
        self.runFor(cycles=50)
        
        self.sendToControl(producerFinished())
        for i in range(1,10):
            self.sendToNext("BLAH")
            
        self.runFor(cycles=1000)
        self.assert_(len(self.children)==1)
        self.assert_(not self.carousel._isStopped())
        
        for i in range(0,9):
            self.assert_(self.children[i].wasActivated)
            self.assert_(not self.children[i]._isStopped())
            msg=self.children[i].recv("control")
            self.assert_(isinstance(msg,(shutdownMicroprocess,producerFinished)))
            self.children[i].stopNow=True
            
            while len(self.children)<=i+1:
                self.runFor(cycles=1)
                
            while not self.children[-1].wasActivated:
                self.runFor(cycles=1)
                
    def test_queuedNextsAbortedIfShutdownMicroprocess(self):
        """If a shutdownMicroprocess() is received, any messages queued on the 'next' inbox are discarded; and Carousel shuts down as soon as any current child has terminated."""
            
        self.setup_test()
        
        self.runFor(cycles=5)
        self.sendToNext("BLAH")
        self.runFor(cycles=50)
        
        self.sendToControl(shutdownMicroprocess())
        for i in range(1,10):
            self.sendToNext("BLAH")
            
        self.runFor(cycles=50)
        self.assert_(len(self.children)==1, "Should only be the one child")
        self.assert_(not self.carousel._isStopped(), "Carousel shouldn't have stopped until the child has")
        msg=self.children[-1].recv("control")
        self.assert_(isinstance(msg,(shutdownMicroprocess,producerFinished)))

        self.children[-1].stopNow=True
        self.runFor(cycles=2)
        
        self.assert_(len(self.children)==1, "Should only be the one child")
        self.assert_(self.carousel._isStopped(), "Carousel should have terminated")
        self.assert_(self.children[0]._isStopped(), "Child should have terminated")
        
if __name__ == "__main__":
    unittest.main()
    