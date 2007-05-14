#!/usr/bin/env python

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
        self.setup_test()

        self.runFor(cycles=1000)

        self.assert_(self.children==[], "Carousel should create no children")
        self.assert_(not self.dataReadyOutbox(), "Carousel should have sent nothing to its 'outbox' outbox")
        self.assert_(not self.dataReadySignal(), "Carousel should have sent nothing to its 'signal' outbox")
        self.assert_(not self.dataReadyRequestNext(), "Carousel should have sent nothing to its 'requestNext' outbox")
        self.assert_(not self.carousel._isStopped(), "Carousel should still be running")
        
    def test_canAskToMake1stRequest(self):
        self.setup_test(make1stRequest=True)

        self.runFor(cycles=1000)

        self.assert_(self.children==[], "Carousel should create no children")
        self.assert_(not self.dataReadyOutbox(), "Carousel should have sent nothing to its 'outbox' outbox")
        self.assert_(not self.dataReadySignal(), "Carousel should have sent nothing to its 'signal' outbox")
        self.assert_(self.collectRequestNext()==["NEXT"], "Carousel should have sent a single 'NEXT' to its 'requestNext' outbox")
        self.assert_(not self.carousel._isStopped(), "Carousel should still be running")

    def test_shutsDownWhenToldToAndIdle(self):
        for IPC in (producerFinished, shutdownMicroprocess):
            self.setup_test()
    
            self.runFor(cycles=1000)
            self.sendToControl(IPC())
            self.assert_(not self.carousel._isStopped(), "Carousel should still be running")
            self.runFor(cycles=1000)
    
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
        self.setup_test()
        self.runFor(cycles=5)
        self.sendToNext("BLAH")
        self.runFor(cycles=5)

        self.assert_(len(self.children)==1, "Carousel should have spawned a child in response to the 'next' request")
        self.assert_(self.children[-1].arg=="BLAH", "Carousel should have spawned child with the 'next' message as the argument")
        self.assert_(self.children[-1].wasActivated, "The child should have been activated")

    def test_childTerminationTriggersRequestNext(self):
        self.setup_test()
        self.runFor(cycles=5)
        self.sendToNext("BLAH")
        self.runFor(cycles=5)

        self.children[-1].stopNow=True
        self.runFor(cycles=5)

        self.assert_(self.collectRequestNext()==["NEXT"], "Carousel should have sent a single 'NEXT' to its 'requestNext' outbox")
        
    def test_childShutdownSignalDoesntTriggerRequest(self):
        for IPC in (producerFinished,shutdownMicroprocess):
            self.setup_test()
            self.runFor(cycles=5)
            self.sendToNext("BLAH")
            self.runFor(cycles=5)
    
            self.children[-1].send(IPC(),"signal")
            self.runFor(cycles=50)
    
            self.assert_(self.collectRequestNext()==[], "Carousel should have not sent anything 'requestNext' outbox")
        
    def test_ChildReceivesShutdownSignal(self):
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

        for IPC in (producerFinished,):
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
                
        
if __name__ == "__main__":
    unittest.main()
    