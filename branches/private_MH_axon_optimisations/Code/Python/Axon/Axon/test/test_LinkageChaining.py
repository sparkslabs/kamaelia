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
# linkage tests
#
# test creation of various chains of linkages checking data makes it through
# including rejigging of chains



# Test the module loads
import unittest
import sys ; sys.path.append(".") ; sys.path.append("..")
from Component import component
from Scheduler import scheduler

class BusyWaitComponent(component):
    def main(self):
        while 1:
            yield 1

class LinkageChainingTests(unittest.TestCase):
    """Data will be correctly delivered along chains of linkages"""
    
    def verifyChain(self, *chain):
        """Verify delivery along a chain"""
        target=chain[-1]
        execute = scheduler.run.main()
        
        for src in chain[:-1]:
            self.verifyDelivery(execute, src, target, len(chain))
        
        
    def verifyDelivery(self, execute, src, target, chainlength):
        waitcycles=1000
        
        (comp,boxname) = src
        if boxname in comp.inboxes:
            # skip if an inbox (can't send from an inbox!)
            pass
        
        elif boxname in comp.outboxes:
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
        
        else:
            self.fail("ERROR IN TEST - invalid boxname")


    def initComponents(self,qty):
        scheduler.run = scheduler()
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
        
        a.postoffice.deregisterlinkage(thelinkage=link)
        self.verifyChain((a,"outbox"), (b,"inbox"))
        

    
    
if __name__=='__main__':
   unittest.main()
