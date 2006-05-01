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

# Test the module loads
import unittest
import sys ; sys.path.append(".") ; sys.path.append("..")

from ThreadedComponent import threadedcomponent, threadedadaptivecommscomponent
import thread,Queue,threading
import time
from Component import component
from Scheduler import scheduler

class OneShotTo(component):
    def __init__(self,dst,msg):
        super(OneShotTo,self).__init__()
        self.link( (self,"outbox"), dst)
        self.msg=msg
    def main(self):
        self.send(self.msg)
        yield 1
        
class RecvFrom(component):
    def __init__(self,src):
        super(RecvFrom,self).__init__()
        self.link( src, (self,"inbox") )
        self.rec = []
    def main(self):
        while 1:
            yield 1
            if self.dataReady("inbox"):
                self.rec.append(self.recv("inbox"))

class threadedcomponent_Test(unittest.TestCase):
    
    def test_smoketest_init(self):
        """__init__ - class constructor is called with no arguments."""
        c = threadedcomponent()
        
        self.assert_(len(c.inboxes.keys()) == 2, "by default, has 2 inboxes")
        self.assert_("inbox" in c.inboxes.keys(), "by default, has 'inbox' inbox")
        self.assert_("control" in c.inboxes.keys(), "by default, has 'control' inbox")
        
        self.assert_(len(c.outboxes.keys()) == 2, "by default, has 2 outboxes")
        self.assert_("outbox" in c.outboxes.keys(), "by default, has 'outbox' outbox")
        self.assert_("signal" in c.outboxes.keys(), "by default, has 'signal' outbox")
    
    def test_smoketest_args(self):
        """__init__ - accepts no arguments, raises TypeError is any supplied."""
        self.failUnlessRaises(TypeError, threadedcomponent, 5)
        
    def test_localprocessterminates(self):
        """_localmain() microprocess also terminates when the thread terminates"""
        class Test(threadedcomponent):
            def main(self):
                pass
                
        sched=scheduler()
        t=Test().activate(Scheduler=sched)
        n=10
        for s in sched.main():
            time.sleep(0.05)
            n=n-1
            self.assert_(n>0, "Thread (and scheduler) should have stopped by now")
    
    def test_threadisseparate(self):
        """main() -runs in a separate thread of execution"""
        class Test(threadedcomponent):
            def __init__(self):
                super(Test,self).__init__()
                self.threadid = Queue.Queue()
            def main(self):
                self.threadid.put( thread.get_ident() )
                
        sched=scheduler()
        t=Test().activate(Scheduler=sched)
        t.next()            # get the thread started
        self.assert_(t.threadid.get() != thread.get_ident(), "main() returns a different value for thread.get_ident()")
    
    def test_flow_in(self):
        """main() - can receive data sent to the component's inbox(es) using the standard dataReady() and recv() methods."""
        class ThreadedReceiver(threadedcomponent):
            def __init__(self):
                super(ThreadedReceiver,self).__init__()
                self.rec = []
            def main(self):
                while 1:
                    if self.dataReady("inbox"):
                        self.rec.append(self.recv("inbox"))
                        
        sched=scheduler()
        r = ThreadedReceiver().activate(Scheduler=sched)
        msg = "hello!"
        o=OneShotTo( (r,"inbox"), msg).activate(Scheduler=sched)
        r.next()
        o.next()
        r.next()
        time.sleep(0.1)
        r.next()
        self.assert_(r.rec==[msg])
        
    def test_flow_out(self):
        """main() - can send data to the component's outbox(es) using the standard send() method."""
        class ThreadedSender(threadedcomponent):
            def __init__(self,msg):
                super(ThreadedSender,self).__init__()
                self.msg=msg
            def main(self):
                self.send(self.msg)
                
        msg="hello there!"
        sched = scheduler()
        t = ThreadedSender(msg).activate(Scheduler=sched)
        r = RecvFrom( (t,"outbox") ).activate(Scheduler=sched)
        for i in range(10):
            time.sleep(0.1)
            try:
                t.next()
            except StopIteration:
                pass
            try:
                r.next()
            except StopIteration:
                pass
        self.assert_(r.rec == [msg])
        
    def test_linksafe(self):
        class ThreadedLinker(threadedcomponent):
            def main(self):
                for i in range(10):
                    linkage = self.link( (self,"outbox"),(self,"inbox") )
                    self.unlink(linkage)
        
        sched=scheduler()
        t=ThreadedLinker().activate(Scheduler=sched)
        oldlink = t.postoffice.link
        
        safetycheck = threading.RLock()          # re-entrancy permitting mutex
        failures = Queue.Queue()
        
        def link_mock(*argL,**argD):      # wrapper for postoffice.link() method
            if not safetycheck.acquire(False):  # returns False if should block (meaning its not thread safe!)
                failures.put(1)
                return False
            else:
                result = oldlink(*argL,**argD)
                time.sleep(0.05)
                safetycheck.release()
                return result
            
        t.postoffice.link = link_mock
        
        done=False
        for i in range(10):
            try:
                t.next()
            except StopIteration:
                done=True
            linkage = t.link( (t,"signal"),(t,"control") )
            t.unlink(linkage)
        
        while not done:
            try:
                t.next()
            except StopIteration:
                done=True
            
        if failures.qsize():
            self.fail("threadedcomponent,postoffice.link() should not be entered by more than one thread at once.")

class threadedadaptivecommscomponent_Test(unittest.TestCase):
    
    def test_smoketest_init(self):
        """__init__ - class constructor is called with no arguments."""
        c = threadedadaptivecommscomponent()
        
        self.assert_(len(c.inboxes.keys()) == 2, "by default, has 2 inboxes")
        self.assert_("inbox" in c.inboxes.keys(), "by default, has 'inbox' inbox")
        self.assert_("control" in c.inboxes.keys(), "by default, has 'control' inbox")
        
        self.assert_(len(c.outboxes.keys()) == 2, "by default, has 2 outboxes")
        self.assert_("outbox" in c.outboxes.keys(), "by default, has 'outbox' outbox")
        self.assert_("signal" in c.outboxes.keys(), "by default, has 'signal' outbox")
    
    def test_smoketest_args(self):
        """__init__ - accepts no arguments, raises TypeError is any supplied."""
        self.failUnlessRaises(TypeError, threadedcomponent, 5)
    
if __name__ == "__main__":
    unittest.main()