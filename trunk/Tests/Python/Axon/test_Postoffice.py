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
# postoffice tests - testing for correct establishment and registering/
# deregistering of linkages by the postoffice
#
# also test creation of various chains of linkages checking data makes it
# through, irrespective of the ordering and sequence of events leading up to
# the creation of the chain


# Test the module loads
import unittest
from Axon.Component import component
from Axon.Scheduler import scheduler
from Axon.Postoffice import postoffice
from Axon.AxonExceptions import noSpaceInBox

class Dummybox(list):
    def __init__(self,*argl,**argd):
        super(Dummybox,self).__init__(*argl,**argd)
        self.sourcesadded = []
        self.sourcesremoved = []
    def addsource(self, source):
        self.sourcesadded.append(source)
    def removesource(self, source):
        self.sourcesremoved.append(source)

class DummyComponent(object):
    def __init__(self):
        super(DummyComponent,self).__init__()
        self.inboxes = {"inbox":Dummybox(), "control":Dummybox()}
        self.outboxes = {"outbox":Dummybox(), "signal":Dummybox()}

class postoffice_Test(unittest.TestCase):
    """Tests for postoffice object"""
    
    def test___init__SmokeTest_NoArguments(self):
        p = postoffice()
        self.assert_(p.debugname=="", "defaults to have no debugname")
        self.assert_(len(p.linkages)==0, "initializes with no linkages registered")

    def test___init__SmokeTest_DebugnameArgument(self):
        testname="[fwibble]"
        p = postoffice(debugname=testname)
        self.assert_(testname in p.debugname, "can specify a debugname")
        
    def strtest(self, postoffice):
        teststr = "{{ POSTOFFICE: " + postoffice.debugname + "links "+ str(postoffice.linkages) +" }}"
        return (teststr == str(postoffice))
    
    def test__str__checksStringFormatStrict(self):
        '__str__ - Checks the formatted string is of the correct format.'
        p = postoffice()
        self.failUnless(self.strtest(p))
        p2 = postoffice(debugname="flurble")
        self.failUnless(self.strtest(p2))

    def test_linkestablishes(self):
        p = postoffice()
        c1 = DummyComponent()
        c2 = DummyComponent()
        p.link( (c1,"outbox"), (c2,"inbox") )
        self.assert_(c2.inboxes['inbox'].sourcesadded == [c1.outboxes['outbox']])
        self.assert_(c2.inboxes['inbox'].sourcesremoved == [])
        self.assert_(c2.inboxes['control'].sourcesadded == [])
        self.assert_(c2.inboxes['control'].sourcesremoved == [])
        self.assert_(c2.outboxes['outbox'].sourcesadded == [])
        self.assert_(c2.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c2.outboxes['signal'].sourcesadded == [])
        self.assert_(c2.outboxes['signal'].sourcesremoved == [])
        
        self.assert_(c1.inboxes['inbox'].sourcesadded == [])
        self.assert_(c1.inboxes['inbox'].sourcesremoved == [])
        self.assert_(c1.inboxes['control'].sourcesadded == [])
        self.assert_(c1.inboxes['control'].sourcesremoved == [])
        self.assert_(c1.outboxes['outbox'].sourcesadded == [])
        self.assert_(c1.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c1.outboxes['signal'].sourcesadded == [])
        self.assert_(c1.outboxes['signal'].sourcesremoved == [])
        
    def test_linkestablishes_inboxinboxpassthrough(self):
        p = postoffice()
        c1 = DummyComponent()
        c2 = DummyComponent()
        p.link( (c1,"inbox"), (c2,"inbox"), passthrough=1 )
        self.assert_(c2.inboxes['inbox'].sourcesadded == [c1.inboxes['inbox']])
        self.assert_(c2.inboxes['inbox'].sourcesremoved == [])
        self.assert_(c2.inboxes['control'].sourcesadded == [])
        self.assert_(c2.inboxes['control'].sourcesremoved == [])
        self.assert_(c2.outboxes['outbox'].sourcesadded == [])
        self.assert_(c2.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c2.outboxes['signal'].sourcesadded == [])
        self.assert_(c2.outboxes['signal'].sourcesremoved == [])
        
        self.assert_(c1.inboxes['inbox'].sourcesadded == [])
        self.assert_(c1.inboxes['inbox'].sourcesremoved == [])
        self.assert_(c1.inboxes['control'].sourcesadded == [])
        self.assert_(c1.inboxes['control'].sourcesremoved == [])
        self.assert_(c1.outboxes['outbox'].sourcesadded == [])
        self.assert_(c1.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c1.outboxes['signal'].sourcesadded == [])
        self.assert_(c1.outboxes['signal'].sourcesremoved == [])

    def test_linkestablishes_outboxoutboxpassthrough(self):
        p = postoffice()
        c1 = DummyComponent()
        c2 = DummyComponent()
        p.link( (c1,"outbox"), (c2,"outbox"), passthrough=2 )
        self.assert_(c2.inboxes['inbox'].sourcesadded == [])
        self.assert_(c2.inboxes['inbox'].sourcesremoved == [])
        self.assert_(c2.inboxes['control'].sourcesadded == [])
        self.assert_(c2.inboxes['control'].sourcesremoved == [])
        self.assert_(c2.outboxes['outbox'].sourcesadded == [c1.outboxes['outbox']])
        self.assert_(c2.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c2.outboxes['signal'].sourcesadded == [])
        self.assert_(c2.outboxes['signal'].sourcesremoved == [])
        
        self.assert_(c1.inboxes['inbox'].sourcesadded == [])
        self.assert_(c1.inboxes['inbox'].sourcesremoved == [])
        self.assert_(c1.inboxes['control'].sourcesadded == [])
        self.assert_(c1.inboxes['control'].sourcesremoved == [])
        self.assert_(c1.outboxes['outbox'].sourcesadded == [])
        self.assert_(c1.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c1.outboxes['signal'].sourcesadded == [])
        self.assert_(c1.outboxes['signal'].sourcesremoved == [])

    def test_linkregistered(self):
        p = postoffice()
        c1 = DummyComponent()
        c2 = DummyComponent()
        l1 = p.link( (c1,"outbox"), (c2,"inbox") )
        self.assert_(l1 in p.linkages, "postoffice registers with itself any linkages you ask it to make")
        l2 = p.link( (c1,"signal"), (c2,"control") )
        self.assert_(l1 in p.linkages and l2 in p.linkages)

    def test_linkderegisters(self):
        p = postoffice()
        c1 = DummyComponent()
        c2 = DummyComponent()
        l1 = p.link( (c1,"outbox"), (c2,"inbox") )
        l2 = p.link( (c1,"signal"), (c2,"control") )
        p.unlink(thelinkage=l1)
        self.assert_(l1 not in p.linkages and l2 in p.linkages, "linkage deregisters when you unlink specifying a linkage")
        
    def test_componentlinksderegisters(self):
        p = postoffice()
        c1 = DummyComponent()
        c2 = DummyComponent()
        c3 = DummyComponent()
        l1 = p.link( (c1,"outbox"), (c2,"inbox") )
        l2 = p.link( (c1,"signal"), (c2,"control") )
        l3 = p.link( (c2,"outbox"), (c3,"inbox") )
        l4 = p.link( (c2,"signal"), (c3,"control") )
        p.unlink(thecomponent=c1)
        self.assert_(l1 not in p.linkages and 
                     l2 not in p.linkages and
                     l3 in p.linkages and
                     l4 in p.linkages,
                     "linkages deregister when you unlink specifying a component")
        
    def test_linkdisengages(self):
        p = postoffice()
        c1 = DummyComponent()
        c2 = DummyComponent()
        l1 = p.link( (c1,"outbox"), (c2,"inbox") )
        p.unlink(thelinkage=l1)
        self.assert_(c2.inboxes['inbox'].sourcesadded == [c1.outboxes['outbox']])
        self.assert_(c2.inboxes['inbox'].sourcesremoved == [c1.outboxes['outbox']])
        self.assert_(c2.inboxes['control'].sourcesadded == [])
        self.assert_(c2.inboxes['control'].sourcesremoved == [])
        self.assert_(c2.outboxes['outbox'].sourcesadded == [])
        self.assert_(c2.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c2.outboxes['signal'].sourcesadded == [])
        self.assert_(c2.outboxes['signal'].sourcesremoved == [])
        
        self.assert_(c1.inboxes['inbox'].sourcesadded == [])
        self.assert_(c1.inboxes['inbox'].sourcesremoved == [])
        self.assert_(c1.inboxes['control'].sourcesadded == [])
        self.assert_(c1.inboxes['control'].sourcesremoved == [])
        self.assert_(c1.outboxes['outbox'].sourcesadded == [])
        self.assert_(c1.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c1.outboxes['signal'].sourcesadded == [])
        self.assert_(c1.outboxes['signal'].sourcesremoved == [])
        
    def test_linkdisengages_inboxinboxpassthrough(self):
        p = postoffice()
        c1 = DummyComponent()
        c2 = DummyComponent()
        l1 = p.link( (c1,"inbox"), (c2,"inbox"), passthrough=1 )
        p.unlink(thelinkage=l1)
        self.assert_(c2.inboxes['inbox'].sourcesadded == [c1.inboxes['inbox']])
        self.assert_(c2.inboxes['inbox'].sourcesremoved == [c1.inboxes['inbox']])
        self.assert_(c2.inboxes['control'].sourcesadded == [])
        self.assert_(c2.inboxes['control'].sourcesremoved == [])
        self.assert_(c2.outboxes['outbox'].sourcesadded == [])
        self.assert_(c2.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c2.outboxes['signal'].sourcesadded == [])
        self.assert_(c2.outboxes['signal'].sourcesremoved == [])
        
        self.assert_(c1.inboxes['inbox'].sourcesadded == [])
        self.assert_(c1.inboxes['inbox'].sourcesremoved == [])
        self.assert_(c1.inboxes['control'].sourcesadded == [])
        self.assert_(c1.inboxes['control'].sourcesremoved == [])
        self.assert_(c1.outboxes['outbox'].sourcesadded == [])
        self.assert_(c1.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c1.outboxes['signal'].sourcesadded == [])
        self.assert_(c1.outboxes['signal'].sourcesremoved == [])
        
    def test_linkdisengages_outboxoutboxpassthrough(self):
        p = postoffice()
        c1 = DummyComponent()
        c2 = DummyComponent()
        l1 = p.link( (c1,"outbox"), (c2,"outbox"), passthrough=2 )
        p.unlink(thelinkage=l1)
        self.assert_(c2.inboxes['inbox'].sourcesadded == [])
        self.assert_(c2.inboxes['inbox'].sourcesremoved == [])
        self.assert_(c2.inboxes['control'].sourcesadded == [])
        self.assert_(c2.inboxes['control'].sourcesremoved == [])
        self.assert_(c2.outboxes['outbox'].sourcesadded == [c1.outboxes['outbox']])
        self.assert_(c2.outboxes['outbox'].sourcesremoved == [c1.outboxes['outbox']])
        self.assert_(c2.outboxes['signal'].sourcesadded == [])
        self.assert_(c2.outboxes['signal'].sourcesremoved == [])
        
        self.assert_(c1.inboxes['inbox'].sourcesadded == [])
        self.assert_(c1.inboxes['inbox'].sourcesremoved == [])
        self.assert_(c1.inboxes['control'].sourcesadded == [])
        self.assert_(c1.inboxes['control'].sourcesremoved == [])
        self.assert_(c1.outboxes['outbox'].sourcesadded == [])
        self.assert_(c1.outboxes['outbox'].sourcesremoved == [])
        self.assert_(c1.outboxes['signal'].sourcesadded == [])
        self.assert_(c1.outboxes['signal'].sourcesremoved == [])
        

class BusyWaitComponent(component):
    def main(self):
        while 1:
            yield 1

class linkagechaining_Test(unittest.TestCase):
    """\
    Data will be correctly delivered along chains of linkages irrespective of
    the order in which the chain is constructed.
    """
    
    def verifyChain(self, *chain):
        """Verify delivery along a chain"""
        target=chain[-1]
        execute = self.schedthread
        
        for src in chain[:-1]:
            self.verifyDelivery(execute, src, target, len(chain))
        
        
    def verifyDelivery(self, execute, src, target, chainlength):
        waitcycles=10
        visited = []
        
        (comp,boxname) = src
        if boxname in comp.inboxes:
            # skip if an inbox (can't send from an inbox!)
            boxtype="inbox"
        
        elif boxname in comp.outboxes:
            boxtype="outbox"
            data = object()
            comp.send(data, boxname)
            
            try:
                for _ in range(0,waitcycles):
                    execute.next()
            except StopIteration:
                self.fail("Scheduler terminated unexpectedly")
            
            (tcomp,tboxname) = target
            self.failUnless( tboxname in tcomp.inboxes, "ERROR IN TEST - destination box not an inbox" )
            self.assert_( tcomp.dataReady(tboxname), "something delivered from "+comp.name+" '"+boxname+"' outbox to  "+tcomp.name+" '"+tboxname+"' inbox" )
            self.assert_( data == tcomp.recv(tboxname), "correct data delivered from "+comp.name+" '"+boxname+"' outbox to  "+tcomp.name+" '"+tboxname+"' inbox" )
        
            self.failIf( (comp,boxname,boxtype) in visited, "Loop detected in linkage chain!")
            visited.append((comp,boxname,boxtype))
        else:
            self.fail("ERROR IN TEST - invalid boxname")


    def initComponents(self,qty):
        scheduler.run = scheduler()
        self.schedthread = scheduler.run.main()
        return self.makeComponents(qty)
    
    def makeComponents(self, qty):
        return [BusyWaitComponent().activate() for _ in range(0,qty)]
    
    
    def test_Simple(self):
        """Simple outbox to inbox link"""
        a,b = self.initComponents(2)
        a.link( (a,"outbox"), (b,"inbox") )
        self.verifyChain((a,"outbox"),(b,"inbox"))
        
        
    def test_SimpleThenInboxPassthrough(self):
        """Simple outox to inbox link, followed by an inbox to inbox passthrough"""
        a,b,c = self.initComponents(3)
        a.link( (a,"outbox"), (b,"inbox") )
        a.link( (b,"inbox"),  (c,"inbox"), passthrough=1 )
        self.verifyChain((a,"outbox"), (b,"inbox"), (c,"inbox"))
        

    def test_InboxPassthroughThenNormal(self):
        """Simple outox to inbox link, followed by an inbox to inbox passthrough, created in the opposite order"""
        a,b,c = self.initComponents(3)
        a.link( (b,"inbox"),  (c,"inbox"), passthrough=1 )
        a.link( (a,"outbox"), (b,"inbox") )
        self.verifyChain((a,"outbox"), (b,"inbox"), (c,"inbox"))
        
        
    def test_SimpleThenOutboxPassthrough(self):
        """Simple outbox to inbox link, preceeded later by an outbox to outbox passthough"""
        a,b,c = self.initComponents(3)
        a.link( (b,"outbox"), (c,"inbox") )
        a.link( (a,"outbox"),  (b,"outbox"), passthrough=2 )
        self.verifyChain((a,"outbox"), (b,"outbox"), (c,"inbox"))

    def test_OutboxPassthroughThenNormal(self):
        """Simple outbox to inbox link, preceeded earlier by an outbox to outbox passthough"""
        a,b,c = self.initComponents(3)
        a.link( (a,"outbox"),  (b,"outbox"), passthrough=2 )
        a.link( (b,"outbox"), (c,"inbox") )
        self.verifyChain((a,"outbox"), (b,"outbox"), (c,"inbox"))

    def test_InboxPassthrougthDeletion(self):
        """Outbox->Inbox->Inbox chain, then 2nd link (passthrough) is deleted"""
        a,b,c = self.initComponents(3)
        a.link( (a,"outbox"),  (b,"inbox") )
        link = a.link( (b,"inbox"), (c,"inbox"), passthrough=1 )
        self.verifyChain((a,"outbox"), (b,"inbox"), (c,"inbox"))
        
        a.postoffice.unlink(thelinkage=link)
        self.verifyChain((a,"outbox"), (b,"inbox"))
        

class UnpauseDetectionComponent(component):
    def __init__(self):
        super(UnpauseDetectionComponent,self).__init__()
        self.unpaused=0
    def main(self):
        while 1:
            self.pause()
            yield 1
            self.unpaused += 1

class MessageDeliveryNotifications_Test(unittest.TestCase):
    """\
    Tests to check notification callbacks are correctly established and used for
    message deliveries and collections.
    """
    
    def initComponents(self,qty):
        scheduler.run = scheduler()
        self.schedthread = scheduler.run.main()
        return self.makeComponents(qty)
    
    def makeComponents(self, qty):
        return [UnpauseDetectionComponent().activate() for _ in range(0,qty)]
    
    def runForAWhile(self, cycles=100):
        for _ in range(0,cycles):
            self.schedthread.next()
    
    def test_NothingHappensIfNothingHappens(self):
        """A paused component stays paused if nothing happens"""
        a,b = self.initComponents(2)
        a.link( (a,"outbox"), (b,"inbox") )
        b.link( (b,"outbox"), (a,"inbox") )
        self.assert_(a.unpaused==0 and b.unpaused==0)
        self.runForAWhile()
        self.assert_(a.unpaused==0 and b.unpaused==0)
            
    def test_ConsumerWokenByDelivery(self):
        """A paused component is unpaused when a message is delivered to its inbox."""
        a,b = self.initComponents(2)
        a.link( (a,"outbox"), (b,"inbox") )
        
        self.runForAWhile()
        a.send(object(),"outbox")
        self.runForAWhile()
        self.assert_(b.unpaused==1)
    
    def test_ProducerNotWokenByDelivery(self):
        """A paused component is not unpaused when it sends a message."""
        a,b = self.initComponents(2)
        a.link( (a,"outbox"), (b,"inbox") )
        
        self.runForAWhile()
        a.send(object(),"outbox")
        self.runForAWhile()
        self.assert_(a.unpaused==0)
    
    def test_ProducerNotWokenByDelivery(self):
        """A paused component is unpaused when a consumer picks up a message it has sent."""
        a,b = self.initComponents(2)
        a.link( (a,"outbox"), (b,"inbox") )
        
        self.runForAWhile()
        a.send(object(),"outbox")
        self.runForAWhile()
        b.recv("inbox")
        self.runForAWhile()
        self.assert_(a.unpaused==1)
    
    def test_ChainOnlyFinalDestinationNotified(self):
        """In a chain of linkages with more than one inbox, only the final destination is woken when a message is sent."""
        a,b,c,d = self.initComponents(4)
        a.link( (a,"outbox"), (b,"inbox") )
        b.link( (b,"inbox"),  (c,"inbox"), passthrough=1 )
        c.link( (c,"inbox"),  (d,"inbox"), passthrough=1 )
        
        self.runForAWhile()
        a.unpaused = 0
        b.unpaused = 0
        c.unpaused = 0
        d.unpaused = 0
        a.send(object(),"outbox")
        self.runForAWhile()
        
        self.assert_(a.unpaused==0)
        self.assert_(b.unpaused==0)
        self.assert_(c.unpaused==0)
        self.assert_(d.unpaused==1)
        
    def test_ChainOnlyOutboxHoldersNotified(self):
        """In a chain of linkages, only the owners of outboxes are notified when a message is picked up."""
        a,b,c,d = self.initComponents(4)
        a.link( (a,"outbox"), (b,"inbox") )
        b.link( (b,"inbox"),  (c,"inbox"), passthrough=1 )
        c.link( (c,"inbox"),  (d,"inbox"), passthrough=1 )
        
        self.runForAWhile()
        a.send(object(),"outbox")
        self.runForAWhile()
        a.unpaused = 0
        b.unpaused = 0
        c.unpaused = 0
        d.unpaused = 0
        d.recv("inbox")
        self.runForAWhile()
        
        self.assert_(a.unpaused==1)
        self.assert_(b.unpaused==0)
        self.assert_(c.unpaused==0)
        self.assert_(d.unpaused==0)
        
    def test_AllOutboxOwnersNotified(self):
        """In a chain of linkages, all owners of outboxes are notified when a message is picked up."""
        a,b,c,d,e = self.initComponents(5)
        a.link( (a,"outbox"), (b,"outbox"), passthrough=2 )
        b.link( (b,"outbox"), (c,"outbox"), passthrough=2 )
        c.link( (c,"outbox"), (d,"inbox"),                )
        d.link( (d,"inbox"),  (e,"inbox"),  passthrough=1 )
       
        self.runForAWhile()
        a.send(object(),"outbox")
        self.runForAWhile()
        a.unpaused = 0
        b.unpaused = 0
        c.unpaused = 0
        d.unpaused = 0
        e.unpaused = 0
        d.recv("inbox")
        self.runForAWhile()
        self.assert_(a.unpaused==1)
        self.assert_(b.unpaused==1)
        self.assert_(c.unpaused==1)
        self.assert_(d.unpaused==0)
        self.assert_(e.unpaused==0)
        
    def test_LinkBrokenNoNotify(self):
        """If the linkage chain breaks before a message is collected, the owners of outboxes that are no longer in the chain are not notified."""
        a,b,c,d,e = self.initComponents(5)
        L1 = a.link( (a,"outbox"), (b,"outbox"), passthrough=2 )
        L2 = b.link( (b,"outbox"), (c,"outbox"), passthrough=2 )
        L3 = c.link( (c,"outbox"), (d,"inbox"),                )
        L4 = d.link( (d,"inbox"),  (e,"inbox"),  passthrough=1 )
       
        self.runForAWhile()
        a.send(object(),"outbox")
        self.runForAWhile()
        b.unlink(thelinkage=L2)
        self.runForAWhile()
        a.unpaused = 0
        b.unpaused = 0
        c.unpaused = 0
        d.unpaused = 0
        e.unpaused = 0
        d.recv("inbox")
        self.runForAWhile()
        self.assert_(a.unpaused==0)
        self.assert_(b.unpaused==0)
        self.assert_(c.unpaused==1)
        self.assert_(d.unpaused==0)
        self.assert_(e.unpaused==0)
       
    def test_LinkReestablishedNotify(self):
        """If the linkage chain breaks and is then re-established before a message is collected, the owners of outboxes that are no longer in the chain are not notified, but ones that are will be."""
        a,b,c,d,e = self.initComponents(5)
        L1 = a.link( (a,"outbox"), (b,"outbox"), passthrough=2 )
        L2 = b.link( (b,"outbox"), (c,"outbox"), passthrough=2 )
        L3 = c.link( (c,"outbox"), (d,"inbox"),                )
        L4 = d.link( (d,"inbox"),  (e,"inbox"),  passthrough=1 )
       
        self.runForAWhile()
        a.send(object(),"outbox")
        self.runForAWhile()
        b.unlink(thelinkage=L2)
        self.runForAWhile()
        b.link( (b,"outbox"), (c,"outbox"), passthrough=2 )   # re-establish
        self.runForAWhile()
        a.unpaused = 0
        b.unpaused = 0
        c.unpaused = 0
        d.unpaused = 0
        e.unpaused = 0
        d.recv("inbox")
        self.runForAWhile()
        self.assert_(a.unpaused==1)  # reestablished
        self.assert_(b.unpaused==1)  # reestablished
        self.assert_(c.unpaused==1)  # stil linked
        self.assert_(d.unpaused==0)
        self.assert_(e.unpaused==0)
       
    def test_LinkNewlyEestablishedNotify(self):
        """If a message is sent, then a new linkage added before a message is collected, the owner of the newly linked in outbox will notified too."""
        a,b,c,d,e,f = self.initComponents(6)
        L1 = a.link( (a,"outbox"), (b,"outbox"), passthrough=2 )
        L2 = b.link( (b,"outbox"), (c,"outbox"), passthrough=2 )
        L3 = c.link( (c,"outbox"), (d,"inbox"),                )
        L4 = d.link( (d,"inbox"),  (e,"inbox"),  passthrough=1 )
       
        self.runForAWhile()
        a.send(object(),"outbox")
        self.runForAWhile()
        self.runForAWhile()
        f.link( (f,"outbox"),(c,"outbox"), passthrough=2 )
        self.runForAWhile()
        a.unpaused = 0
        b.unpaused = 0
        c.unpaused = 0
        d.unpaused = 0
        e.unpaused = 0
        f.unpaused = 0
        d.recv("inbox")
        self.runForAWhile()
        self.assert_(a.unpaused==1)
        self.assert_(b.unpaused==1)
        self.assert_(c.unpaused==1)
        self.assert_(d.unpaused==0)
        self.assert_(e.unpaused==0)
        self.assert_(f.unpaused==1)  # new one linked in, also gets notified
       

class SizeLimitedBoxes_Test(unittest.TestCase):
    """\
    Tests ability to limit the size of inboxes.
    """
    def initComponents(self,qty):
        scheduler.run = scheduler()
        self.schedthread = scheduler.run.main()
        return self.makeComponents(qty)
    
    def makeComponents(self, qty):
        return [UnpauseDetectionComponent().activate() for _ in range(0,qty)]
    
    def runForAWhile(self, cycles=100):
        for _ in range(0,cycles):
            self.schedthread.next()
    
    def test_smoketest(self):
        """You can call mycomponent.inboxes[boxname].setSize(n) to set the box size."""
        a, = self.initComponents(1)
        a.inboxes['inbox'].setSize(5)
        
    def test_BoxSizeGetsLimited(self):
        """Restrict the size of an inbox to 5 and you can send 5 messages to it without error."""
        a,b = self.initComponents(2)
        b.inboxes['inbox'].setSize(5)
        
        a.link((a,"outbox"),(b,"inbox"))
        self.runForAWhile()
        for _ in range(5):
            a.send(object(), "outbox")
        self.runForAWhile()
        
    def test_ExceedBoxSizeAndGetException(self):
        """Send a 6th message to an inbox of size 5 and a noSpaceInBox exception will be thrown."""
        a,b = self.initComponents(2)
        b.inboxes['inbox'].setSize(5)
        
        a.link((a,"outbox"),(b,"inbox"))
        self.runForAWhile()
        for _ in range(5):
            a.send(object(), "outbox")
        self.runForAWhile()
        self.failUnlessRaises(noSpaceInBox, a.send, object(), "outbox")
        
    def test_removingFromInboxAllowsYouToPutMoreIn(self):
        """Collecting 3 items from a full inbox and you can put 3 more in before a noSpaceInBox exception is thrown."""
        a,b = self.initComponents(2)
        b.inboxes['inbox'].setSize(5)
        
        a.link((a,"outbox"),(b,"inbox"))
        self.runForAWhile()
        for _ in range(5):
            a.send(object(), "outbox")
        self.runForAWhile()
        for _ in range(3):
            b.recv("inbox")
        self.runForAWhile()
        for _ in range(3):
            a.send(object(), "outbox")
        self.failUnlessRaises(noSpaceInBox, a.send, object(), "outbox")
        
    def test_SizeLimitMidLinkageChainHasNoEffect(self):
        """A size limited inbox that isn't the final destination in a linkage chain will not cause noSpaceInBox exceptions to be thrown."""
        a,b,c = self.initComponents(3)
        b.inboxes['inbox'].setSize(5)
        
        a.link((a,"outbox"), (b,"inbox"))
        b.link((b,"inbox"), (c,"inbox"), passthrough=1)
        self.runForAWhile()
        for _ in range(10):
            a.send(object(), "outbox")
        self.runForAWhile()
        
    def test_SizeLimitMidLinkageChainComesIntoEffectIfChainBroken(self):
        """A size limited inbox that becomes the final destination in a linkage chain (because a link is broken) causes noSpaceInBox exceptions to be thrown as if it had always been the final destination."""
        a,b,c = self.initComponents(3)
        b.inboxes['inbox'].setSize(5)
        
        L1=a.link((a,"outbox"), (b,"inbox"))
        L2=b.link((b,"inbox"), (c,"inbox"), passthrough=1)
        self.runForAWhile()
        for _ in range(10):
            a.send(object(), "outbox")
        self.runForAWhile()
        b.unlink(thelinkage=L2)
        self.runForAWhile()
        for _ in range(5):
            a.send(object(), "outbox")
        self.failUnlessRaises(noSpaceInBox, a.send, object(), "outbox")
        
    def test_SettingSizeLimitToNoneSetsToUnlimited(self):
        """Setting a size limit of None mean the inbox size is unrestricted."""
        a,b = self.initComponents(2)
        b.inboxes['inbox'].setSize(None)
        
        a.link((a,"outbox"),(b,"inbox"))
        self.runForAWhile()
        for _ in range(9999):
            a.send(object(), "outbox")
        self.runForAWhile(9999)
        
    def test_TurningOffSizeLimit(self):
        """Setting a size limit then later changing it to None turns off  inbox size restrictions."""
        a,b = self.initComponents(2)
        b.inboxes['inbox'].setSize(5)
        L1=a.link((a,"outbox"), (b,"inbox"))
        self.runForAWhile()
        for _ in range(5):
            a.send(object(), "outbox")
        self.runForAWhile()
        b.inboxes['inbox'].setSize(None)
        self.runForAWhile()
        for _ in range(500):
            a.send(object(), "outbox")
        self.runForAWhile()
        
    def test_AllProducersExperienceSameSizeLimit(self):
        """All outboxes in a linkage chain sharing the same destination inbox will experience noSpaceInBox exceptions when and only when the destination inbox becomes full and any of them tries to send to it."""
        a,b,c,d,e = self.initComponents(5)
        e.inboxes['inbox'].setSize(4*4)
        a.link((a,"outbox"),(e,"inbox"))
        b.link((b,"outbox"),(e,"inbox"))
        c.link((c,"outbox"),(b,"outbox"),passthrough=2)
        d.link((d,"outbox"),(b,"outbox"),passthrough=2)
        
        self.runForAWhile()
        i=0
        while i < 100:
            for X in [a,b,c,d]:
                i+=1
                if i <= e.inboxes['inbox'].getSize():
                    X.send(object(),"outbox")
                else:
                    self.failUnlessRaises(noSpaceInBox, X.send, object(), "outbox")
                self.runForAWhile()



if __name__=='__main__':
   unittest.main()
