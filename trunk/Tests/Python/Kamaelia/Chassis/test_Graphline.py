#!/usr/bin/env python
#
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# test suite for graphline

import unittest

from Kamaelia.Chassis.Graphline import Graphline

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


class Test_Graphline(unittest.TestCase):

    def setup_initialise(self,*listargs,**dictargs):
        self.children = {}
        for key in dictargs.keys():
            if key != "linkages":
                self.children[key] = dictargs[key]
        
        self.scheduler = scheduler()
        scheduler.run = self.scheduler

        self.graphline = Graphline(*listargs, **dictargs)
        
        self.inSrc = {}
        for box in ["inbox","control"]:
            c = Dummy()
            c.link((c,"outbox"), (self.graphline,box))
            self.inSrc[box]=c
        
        self.outDest = {}
        for box in ["outbox","signal"]:
            c = Dummy()
            c.link((self.graphline,box), (c,"inbox"))
            self.outDest[box]=c
        
        self.run = self.scheduler.main()

    def setup_activate(self):
        self.graphline.activate(Scheduler=self.scheduler)
        for c in self.inSrc.values():
            c.activate(Scheduler=self.scheduler)
        for c in self.outDest.values():
            c.activate(Scheduler=self.scheduler)
        
    def sendTo(self,data,boxname):
        self.ensureHandlerForInbox(boxname)
        self.inSrc[boxname].send(data,"outbox")
        
    def recvFrom(self,boxname):
        return self.outDest[boxname].recv("inbox")
    
    def dataReadyAt(self,boxname):
        return self.outDest[boxname].dataReady("inbox")
        
    def ensureHandlerForInbox(self,boxname):
        if not boxname in self.inSrc:
            try:
                c=Dummy()
                c.link((c,"outbox"), (self.graphline,boxname))
                c.activate(Scheduler=self.scheduler)
                self.inSrc[boxname]=c
            except KeyError:
                self.fail("Expected inbox '"+boxname+"' on graphline does not exist")

    def ensureHandlerForOutbox(self,boxname):
        if not boxname in self.outDest:
            try:
                c=Dummy()
                c.link((self.graphline,boxname), (c,"inbox"))
                c.activate(Scheduler=self.scheduler)
                self.outDest[boxname]=c
            except KeyError:
                self.fail("Expected inbox '"+boxname+"' on graphline does not exist")
    
    
    def runFor(self, cycles):
        numcycles=cycles*(len(self.inSrc)+len(self.outDest)+1+len(self.children))    # approx this many components in the system
        for i in range(0,numcycles): self.run.next()

    def checkDataFlows(self, source, *targets):
        (fromComponent, fromBox) = source
        
        DATA=object()
        
        for (toComponent,toBox) in targets:
            if toComponent==self.graphline:
                self.ensureHandlerForOutbox(toBox)

        if fromComponent==self.graphline:
            self.sendTo(DATA,fromBox)
        else:
            fromComponent.send(DATA,fromBox)        
          
        self.runFor(cycles=1)
        
        for (toComponent,toBox) in targets:
            if toComponent==self.graphline:
                self.assert_(self.dataReadyAt(toBox))
                self.assertEquals(DATA, self.recvFrom(toBox))
            else:
                self.assert_(toComponent.dataReady(toBox))
                self.assertEquals(DATA, toComponent.recv(toBox))
    
        for child in self.children.values():
            if child not in [toComponent for (toComponent,toBox) in targets]:
               self.assert_(not(child.anyReady()))



    def test_smokeTest(self):
        """Instantiating a graphline with no arguments results in a ValueError exception"""
        self.failUnlessRaises(ValueError, Graphline)
        
        
    def test_graphlineNoLinkagesArg(self):
        """Instantiating with components as named arguments, but specifying no linkages argument results in a ValueError exception"""
        self.failUnlessRaises(ValueError, Graphline, A=component(), B=component())


    def test_graphlineEmptyLinkagesArg(self):
        """Instantiating with components as named arguments, and specifying an empty linkages argument succeeds"""
        Graphline(A=component(), B=component(), linkages={})


    def test_graphlineNoComponentsEmptyLinkagesArg(self):
        """Instantiating with no components as named arguments, and specifying an empty linkages argument succeeds"""
        Graphline(linkages={})


    def test_graphlineHasChildren(self):
        """Instantiating a graphline, components specified as named arguments, eg. A=component() and B=component() become children of the graphline once activated and run."""
        self.setup_initialise(A=component(), B=component(), linkages={})
        self.setup_activate()
        
        self.runFor(cycles=1)
        
        gChildren = self.graphline.childComponents()
        for c in self.children.values():
            self.assert_(c in gChildren)
        
        
    def test_unactivatedGraphlineHasNoChildren(self):
        """Instantiating a graphline, components specified as named arguments, eg. A=component() and B=component() will not be children of the graphline before it is activated and run"""
        self.setup_initialise(A=component(), B=component(), linkages={})
        
        gChildren = self.graphline.childComponents()
        for c in self.children.values():
            self.assert_(not(c in gChildren))
        

    def test_activatesChildrenOnlyWhenActivatedNotLinked(self):
        """Children are activated as soon as the Graphline itself is activated, but no sooner. They get activated even if they have no linkages specified to them."""
        self.setup_initialise(A=MockChild(), B=MockChild(), C=MockChild(), linkages={})

        for child in self.children.values():
            self.assert_(not(child.wasActivated))

        self.setup_activate()
        self.runFor(cycles=1)
        self.runFor(cycles=3)
        
        for child in self.children.values():
            self.assert_(child.wasActivated)
        
        
    def test_activatesChildrenOnlyWhenActivatedLinked(self):
        """Children are activated as soon as the Graphline itself is activated, but no sooner. They get activated even if they have no linkages specified to them."""
        self.setup_initialise(A=MockChild(), B=MockChild(), C=MockChild(), linkages={
            ("A","outbox"):("B","inbox"),
            ("B","outbox"):("C","inbox"),
            ("C","outbox"):("A","inbox"),
            })

        for child in self.children.values():
            self.assert_(not(child.wasActivated))

        self.setup_activate()
        self.runFor(cycles=1)
        self.runFor(cycles=3)
        
        for child in self.children.values():
            self.assert_(child.wasActivated)
        
        
    def test_linkagesBetweenComponents(self):
        """A linkage from "outbox" to "inbox" between two named child components "A" and "B" can be specified by specifying a "linkages" argument containing a dictionary with an entry: ("A","outbox"):("B","inbox"). Data sent to A's "outbox"  will reach B's "inbox" and nowhere else."""
        A=MockChild()
        B=MockChild()
        self.setup_initialise(A=A, B=B, linkages={("A","outbox"):("B","inbox")})

        self.setup_activate()
        self.runFor(cycles=1)

        self.checkDataFlows((A,"outbox"),(B,"inbox"))
        
        
    def test_severalLinkagesBetweenComponents(self):
        """Several linkages can be specified between components. They will all be created, and messages will be able to flow along them once the graphline is activated and run. Data will only flow along the specified linkages and will not leak anywhere else!"""
        A=MockChild()
        B=MockChild()
        C=MockChild()
        D=MockChild()
        self.setup_initialise(
            A=A, B=B, C=C, D=D,
            linkages={
                ("A","outbox"):("B","inbox"),
                ("C","outbox"):("D","control"),
                ("C","signal"):("A","inbox"),
                ("B","signal"):("A","control"),
                }
            )

        self.setup_activate()
        self.runFor(cycles=1)

        self.checkDataFlows((A,"outbox"),(B,"inbox"))
        self.checkDataFlows((C,"outbox"),(D,"control"))
        self.checkDataFlows((C,"signal"),(A,"inbox"))
        self.checkDataFlows((B,"signal"),(A,"control"))
        
    def test_terminateWhenAllChildrenHaveTerminated(self):
        """Graphline will terminate when all of its children have terminated, but not before."""
        A=MockChild()
        B=MockChild()
        C=MockChild()
        self.setup_initialise(A=A, B=B, C=C, linkages={ ("A","outbox"):("B","inbox"), } )

        self.setup_activate()
        
        for i in range(0,2):
            self.runFor(cycles=100)
            self.assert_(self.graphline in self.scheduler.listAllThreads())
            
        for child in self.children.values():
            child.stopNow()
            
        self.runFor(cycles=2)
        self.assert_(not(self.graphline in self.scheduler.listAllThreads()))
        
        
    def test_specifyingPassthruInLinkage(self):
        """If a linkage is specified whose source is (X, "inbox") or (X, "control") where X is not the name given to one of the child components in the graphline, then the linkage created is a passthrough from that named inbox of the graphline to the specified destination child component in the graphline."""
        
        selectionOfUnusedNames = ["", "self", "flurble", "a", "component", "pig"]
        
        for name in selectionOfUnusedNames:
            
            A=MockChild()
            B=MockChild()
            C=MockChild()
        
            self.setup_initialise(
                A=A, B=B, C=C,
                linkages={
                    (name,"inbox"):("A","control"),
                    (name,"control"):("B","inbox"),
                    ("C","outbox"):("A","inbox"),
                })

        self.setup_activate()
        self.runFor(cycles=10)

        self.checkDataFlows((self.graphline,"inbox"),(A,"control"))
        self.checkDataFlows((self.graphline,"control"),(B,"inbox"))
    
    
    def test_specifyingPassthruInLinkageNewBox(self):
        """If a linkage is specified whose source is (X, Y) where X is not the name given to one of the child components in the graphline and Y is neither "inbox" nor "control", then an inbox with name Y is created and the linkage created is a passthrough from that named inbox of the graphline to the specified destination child component in the graphline."""

        selectionOfUnusedNames = ["", "self", "flurble", "a", "component", "pig"]
        
        for name in selectionOfUnusedNames:
            
            A=MockChild()
            B=MockChild()
            C=MockChild()
        
            self.setup_initialise(
                A=A, B=B, C=C,
                linkages={
                    (name,"novel-inbox"):("A","control"),
                    (name,"another-novel-inbox"):("B","inbox"),
                    ("C","outbox"):("A","inbox"),
                })

        self.setup_activate()
        self.runFor(cycles=10)

        self.checkDataFlows((self.graphline,"novel-inbox"),(A,"control"))
        self.checkDataFlows((self.graphline,"another-novel-inbox"),(B,"inbox"))


    def test_specifyingPassthruOutLinkage(self):
        """If a linkage is specified whose destination is (X, "outbox") or (X, "signal") where X is not the name given to one of the child components in the graphline, then the linkage created is a passthrough from the specified source child component in the graphline to that named outbox of the graphline."""
    
        selectionOfUnusedNames = ["", "self", "flurble", "a", "component", "pig"]
        
        for name in selectionOfUnusedNames:
            
            A=MockChild()
            B=MockChild()
            C=MockChild()
        
            self.setup_initialise(
                A=A, B=B, C=C,
                linkages={
                    ("A","outbox"):(name,"signal"),
                    ("B","signal"):(name,"outbox"),
                    ("C","outbox"):("A","inbox"),
                })

        self.setup_activate()
        self.runFor(cycles=10)

        self.checkDataFlows((A,"outbox"),(self.graphline,"signal"))
        self.checkDataFlows((B,"signal"),(self.graphline,"outbox"))
    
    
    def test_specifyingPassthruOutLinkageNewBox(self):
        """If a linkage is specified whose destination is (X, Y) where X is not the name given to one of the child components in the graphline and Y is neither "outbox" nor "signal", then  an outbox with name Y is created and the linkage created is a passthrough from the specified source child component in the graphline to that named outbox of the graphline."""
        
        selectionOfUnusedNames = ["", "self", "flurble", "a", "component", "pig"]
        
        for name in selectionOfUnusedNames:
            
            A=MockChild()
            B=MockChild()
            C=MockChild()
        
            self.setup_initialise(
                A=A, B=B, C=C,
                linkages={
                    ("A","outbox"):(name,"novel-boxname"),
                    ("B","signal"):(name,"another-novel-boxname"),
                    ("C","outbox"):("A","inbox"),
                })

        self.setup_activate()
        self.runFor(cycles=10)

        self.checkDataFlows((A,"outbox"),(self.graphline,"novel-boxname"))
        self.checkDataFlows((B,"signal"),(self.graphline,"another-novel-boxname"))
    
    
    def test_emissionOfShutdownSignal_1(self):
        """When all children have terminated. If no child is wired to the Graphline's "signal" outbox, the Graphline will send out its own message. The message sent will be a producerFinished message if a child is wired to the Graphline's "control" inbox, or if no shutdownMicroprocess message has been previously received on that inbox."""
        
        A=MockChild()
        B=MockChild()
        C=MockChild()
        self.setup_initialise(A=A, B=B, C=C, linkages={ ("A","outbox"):("B","inbox"), } )

        self.setup_activate()
        self.runFor(cycles=100)
        
        # check nothing has been emitted yet!
        self.assert_(not(self.dataReadyAt("signal")))
        
        for child in self.children.values():
            child.stopNow()
            
        self.runFor(cycles=2)
        self.assert_(self.dataReadyAt("signal"))
        self.assert_(isinstance(self.recvFrom("signal"), producerFinished))
        

## FIXME: This test is definitely broken since an example 
## Doing this exists in Examples, and works :-)
    def test_emissionOfShutdownSignal_2(self):
        """When all children have terminated. If no child is wired to the Graphline's "signal" outbox, the Graphline will send out its own message. If no child is wired to the Graphline's "control" inbox and a shutdownMicroprocess message has been previously received on that inbox, then the message sent out will be that shutdownMicroprocess message."""
        
        A=MockChild()
        B=MockChild()
        C=MockChild()
        self.setup_initialise(A=A, B=B, C=C, linkages={ ("A","outbox"):("B","inbox"), } )

        self.setup_activate()
        self.runFor(cycles=100)
        
        # check nothing has been emitted yet!
        self.assert_(not(self.dataReadyAt("signal")))
        
        shutdownMsg = shutdownMicroprocess();
        self.sendTo(shutdownMsg,"control")
        
        self.runFor(cycles=1)
        
        for child in self.children.values():
            child.stopNow()
            
        self.runFor(cycles=3)
        
        self.assert_(self.dataReadyAt("signal"))
        recvd=self.recvFrom("signal")
        
        self.assert_(recvd == shutdownMsg)
        
        
    def test_receivesShutdownPassesThru(self):
        """If a graphline's "control" inbox is specified to be wired to a child component in the graphline, then any message (including shutdown messages) flow along that linkage only."""

        A=MockChild()
        B=MockChild()
        C=MockChild()
        self.setup_initialise(A=A, B=B, C=C, linkages={ ("","control"):("A","control"), } )

        self.setup_activate()
        self.runFor(cycles=100)
        
        self.checkDataFlows((self.graphline,"control"),(A,"control"))


## FIXME: This test is definitely broken since an example 
## Doing this exists in Examples, and works :-)
    def test_receivesShutdownDisseminated(self):
        """If a graphline's "control" inbox is not specified to be wired to a child component in the graphline, then any message (including shutdown messages) flows to the "control" inbox of all children without linkages going to their "control" inbox only."""

        A=MockChild()
        B=MockChild()
        C=MockChild()
        self.setup_initialise(
            A=A, B=B, C=C,
            linkages={ ("A","outbox"):("B","control"), # should block msg getting to B
            })

        self.setup_activate()
        self.runFor(cycles=100)
        
        msg=shutdownMicroprocess()
        self.sendTo(msg,"control")
        self.runFor(cycles=2)
        
        self.assert_(A.dataReady("control"))
        self.assertEquals(msg, A.recv("control"))
        
        self.assert_(not(B.dataReady("control")))
        
        self.assert_(C.dataReady("control"))
        self.assertEquals(msg, C.recv("control"))

    def test_receivesShutdownAndPropagates(self):
        """If a graphline's "control" inbox and "signal" outbox are not specified to be wired to a child component in the graphline then, if a shutdownMicroprocess message is sent to the "control" inbox, it will be sent on out of the "signal" outbox once all children have terminated."""

        A=MockChild()
        B=MockChild()
        C=MockChild()
        self.setup_initialise(
            A=A, B=B, C=C,
            linkages={ ("A","outbox"):("B","control"), 
            })

        self.setup_activate()
        self.runFor(cycles=100)
        
        msg=shutdownMicroprocess()
        self.sendTo(msg,"control")
        
        self.runFor(cycles=100)
        self.assert_(self.graphline in self.scheduler.listAllThreads())
        
        for child in self.children.values():
            child.stopNow()

        self.runFor(cycles=10)
        self.assert_(self.graphline not in self.scheduler.listAllThreads())
        
        self.assert_(self.dataReadyAt("signal"))
        self.assertEquals(msg, self.recvFrom("signal"))


    def test_receivesShutdownAndPropagates2(self):
        """If a graphline's "control" inbox and "signal" outbox are not specified to be wired to a child component in the graphline then, if a any non shutdownMicroprocess message is sent to the "control" inbox, a producerFinished message will be sent on out of the "signal" outbox once all children have terminated."""

        A=MockChild()
        B=MockChild()
        C=MockChild()
        self.setup_initialise(
            A=A, B=B, C=C,
            linkages={ ("A","outbox"):("B","control"), 
            })

        self.setup_activate()
        self.runFor(cycles=100)
        
        msg=producerFinished()
        self.sendTo(msg,"control")
        
        self.runFor(cycles=100)
        self.assert_(self.graphline in self.scheduler.listAllThreads())
        
        for child in self.children.values():
            child.stopNow()

        self.runFor(cycles=10)
        self.assert_(self.graphline not in self.scheduler.listAllThreads())
        
        self.assert_(self.dataReadyAt("signal"))
        recvd=self.recvFrom("signal")
        self.assert_(recvd != msg)
        self.assert_(isinstance(recvd,producerFinished))


    def test_receivesShutdownAndPropagates23(self):
        """If a graphline's "control" inbox is specified to be wired to a child component, but its "signal" outbox is not then, irrespective of what message (eg. shutdownMicroprocess) is sent to the "control" inbox, a producerFinished message will be sent on out of the "signal" outbox once all children have terminated."""

        possibleMessages = [ producerFinished(), shutdownMicroprocess(), "flurble" ]
        
        for msg in possibleMessages:
            A=MockChild()
            B=MockChild()
            C=MockChild()
            self.setup_initialise(
                A=A, B=B, C=C,
                linkages={
                    ("","control"):("A","control"),
                    ("A","outbox"):("B","control"), 
                })

            self.setup_activate()
            self.runFor(cycles=100)
            
            self.sendTo(msg,"control")
            
            self.runFor(cycles=100)
            self.assert_(self.graphline in self.scheduler.listAllThreads())
            
            for child in self.children.values():
                child.stopNow()

            self.runFor(cycles=10)
            self.assert_(self.graphline not in self.scheduler.listAllThreads())
            
            self.assert_(self.dataReadyAt("signal"))
            recvd=self.recvFrom("signal")
            self.assert_(recvd != msg)
            self.assert_(isinstance(recvd,producerFinished))


    def test_doesNotPropagateShutdownMsg(self):
        """If a graphline's "signal" outbox is specified to be wired to a child component, the graphline will send any messages itself out of its "signal" outbox, before or after all children have terminated, even if a shutdownMicroprocess or producerFinished message was sent to its "control" inbox."""
        
        A=MockChild()
        B=MockChild()
        C=MockChild()
        self.setup_initialise(
            A=A, B=B, C=C,
            linkages={ 
                ("A","signal"):("","signal"),
                ("A","outbox"):("B","control"), 
            })

        self.setup_activate()
        self.runFor(cycles=100)
        
        self.sendTo(producerFinished(), "control")
        self.sendTo(shutdownMicroprocess(), "control")
        
        self.runFor(cycles=100)
        self.assert_(self.graphline in self.scheduler.listAllThreads())
        
        self.assert_(not(self.dataReadyAt("signal")))
        
        for child in self.children.values():
            child.stopNow()

        self.runFor(cycles=100)
        
        self.assert_(not(self.dataReadyAt("signal")))


    def test_manuallyImplementedShutdownOverrides(self):
        """If a graphline's "control" inbox and "signal" outbox are both specified to be wired to child components in the graphline, then graphline will not emit its own messages out of its "signal" outbox when it terminates (or at any other time)"""
        A=MockChild()
        B=MockChild()
        C=MockChild()
        self.setup_initialise(
            A=A, B=B, C=C,
            linkages={ 
                ("","control"):("A","control"),
                ("A","signal"):("","signal"), 
                ("B","outbox"):("C","inbox"),
            })

        self.setup_activate()
        self.runFor(cycles=100)
        
        self.assert_(not(self.dataReadyAt("outbox")))
        self.assert_(not(self.dataReadyAt("signal")))

        self.checkDataFlows((self.graphline,"control"),(A,"control"))
        self.checkDataFlows((A,"signal"),(self.graphline,"signal"))
        self.checkDataFlows((B,"outbox"),(C,"inbox"))
        
        self.runFor(cycles=100)

        self.assert_(not(self.dataReadyAt("outbox")))
        self.assert_(not(self.dataReadyAt("signal")))
        
        for child in self.children.values():
            child.stopNow()
        
        self.runFor(cycles=100)

        self.assert_(self.graphline not in self.scheduler.listAllThreads())
        
        self.assert_(not(self.dataReadyAt("outbox")))
        self.assert_(not(self.dataReadyAt("signal")))


    # hack to make this work in python 2.3
    # where assertTrue and assertFalse are not defined
    try:
        unittest.TestCase.assertTrue
    except AttributeError:
        def assertTrue(self,X):
            return self.assert_(X)

    try:
        unittest.TestCase.assertFalse
    except AttributeError:
        def assertFalse(self,X):
            return self.assert_(not X)



if __name__ == "__main__":
    unittest.main()
    

