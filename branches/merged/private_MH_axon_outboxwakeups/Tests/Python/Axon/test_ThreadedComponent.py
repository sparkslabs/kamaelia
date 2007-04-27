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

from Axon.ThreadedComponent import threadedcomponent, threadedadaptivecommscomponent
import thread,Queue,threading
import time
from Axon.Component import component
from Axon.Scheduler import scheduler
from Axon.AxonExceptions import noSpaceInBox

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

class ThreadedSender(threadedcomponent):
    def __init__(self,*argl,**argd):
        if "slow" in argd:
            self.delay=argd["slow"]
            del argd["slow"]
        else:
            self.delay=None
        super(ThreadedSender,self).__init__(*argl,**argd)
        self.feedback = Queue.Queue()
        self.howManyToSend = Queue.Queue()
    def main(self):
        while 1:
            qty = self.howManyToSend.get()
            if qty<=0 or qty=="STOP":
                return
            else:
                try:
                    for i in xrange(qty):
                        self.send(i,"outbox")
                        if self.delay!=None:
                            self.pause(self.delay)
                    self.feedback.put("ALL SENT")
                except noSpaceInBox:
                    self.feedback.put(i)
                except:
                    raise

class DoesNothingThread(threadedcomponent):
    def main(self):
        while 1:
            self.pause()

class DoesNothingComponent(component):
    def main(self):
        while 1:
            self.pause()
            yield 1

def get(list,index,default):
    try:
        return list[index]
    except IndexError:
        return default



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
        """__init__ - can accept no arguments"""
        self.assert_(threadedcomponent())
        
    def test_smoketest_oneargs(self):
        """__init__ - accepts one argument"""
        self.assert_(threadedcomponent(10))
        
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
        """link() unlink() -  thread safe when called. The postoffice link() and unlink() methods are not expected to be capable of re-entrant use."""
        class ThreadedLinker(threadedcomponent):
            def main(self):
                for i in range(10):
                    linkage = self.link( (self,"outbox"),(self,"inbox") )
                    self.unlink(linkage)
        
        sched=scheduler()
        t=ThreadedLinker().activate(Scheduler=sched)
        oldlink   = t.postoffice.link
        oldunlink = t.postoffice.unlink
        
        safetycheck = threading.RLock()          # re-entrancy permitting mutex
        failures = Queue.Queue()
        
        def link_mock(*argL,**argD):      # wrapper for postoffice.link() method
            if not safetycheck.acquire(False):  # returns False if should block (meaning its not thread safe!)
                failures.put(".link()")
                return False
            else:
                result = oldlink(*argL,**argD)
                time.sleep(0.05)
                safetycheck.release()
                return result
            
        def unlink_mock(*argL,**argD):
            if not safetycheck.acquire(False):  # returns False if should block (meaning its not thread safe!)
                failures.put(".unlink()")
                return False
            else:
                result = oldunlink(*argL,**argD)
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
            failed = {}
            while failures.qsize():
                failed[failures.get()] = 1
                conj=""
                errmsg="threadedcomponent,postoffice"
                for method in failed.keys():
                    errmsg=errmsg+conj+method
                    conj=" and "
                errmsg=errmsg+" should not be entered by more than one thread at once."
                self.fail(errmsg)


    def test_ThereIsADefaultOutgoingQueueSize(self):
        """There is a default limit on the number of messages that can queue up waiting to be sent out by the main thread."""
        
        sched=scheduler()
        t=ThreadedSender().activate(Scheduler=sched)
        
        try:
            s=sched.main()
            for _ in range(0,10):
                s.next()
                
            t.howManyToSend.put(99999)
        
            while t.feedback.qsize() == 0:
                time.sleep(0.1)
            
            result = t.feedback.get()
            self.assert_(result != "ALL SENT")
            self.assert_(result > 0)
        except:
            t.howManyToSend.put("STOP")
            raise
        
    def test_CanSetOutgoingQueueSize(self):
        """Setting the queue size in the initializer limits the number of messages that can queue up waiting to be sent out by the main thread."""
       
        QSIZE=20
        sched=scheduler()
        t=ThreadedSender(QSIZE).activate(Scheduler=sched)
        
        try:
            s=sched.main()
            for _ in range(0,10):
                s.next()
                
            t.howManyToSend.put(99999)
        
            while t.feedback.qsize() == 0:
                time.sleep(0.1)
            
            result = t.feedback.get()
            self.assert_(result != "ALL SENT")
            self.assert_(result==QSIZE)
        except:
            t.howManyToSend.put("STOP")
            raise
        
    def test_RestrictedInboxSize(self):
        """Setting the inbox size means at most inbox_size+internal_queue_size messages can queue up before the sender receives a noSpaceInBox exception"""
        
        QSIZE=20
        BSIZE=10
        sched=scheduler()
        t=DoesNothingThread(QSIZE).activate(Scheduler=sched)
        t.inboxes['inbox'].setSize(BSIZE)
        d=DoesNothingComponent().activate(Scheduler=sched)
        d.link((d,"outbox"),(t,"inbox"))
        
        s=sched.main()
        for _ in range(0,10):
            s.next()
        for _ in range(QSIZE+BSIZE):
            d.send(object(),"outbox")
            for __ in range(0,10):
                s.next()
        self.failUnlessRaises(noSpaceInBox, d.send, object(), "outbox")
    
    def test_NoSpaceInBoxExceptionsReachThread(self):
        """If a threadedcomponent outbox is linked to a size restricted inbox, then the thread can send at most inbox_size+internal_queue_size messages before it receives a noSpaceInBox exception."""
        
        QSIZE=20
        BSIZE=10
        sched=scheduler()
        t=ThreadedSender(QSIZE,slow=0.05)
        d=DoesNothingComponent().activate(Scheduler=sched)
        d.inboxes['inbox'].setSize(BSIZE)
        d.link((t,"outbox"),(d,"inbox"))

        s=sched.main()
        for _ in range(0,10):
            s.next()
        
        t.activate(Scheduler=sched)
        
        try:
            t.howManyToSend.put(QSIZE+BSIZE+10)
        
            while t.feedback.qsize() == 0:
                s.next()
            
            result = t.feedback.get()
            self.assert_(result != "ALL SENT")
            self.assert_(result == QSIZE+BSIZE)
        except:
            t.howManyToSend.put("STOP")
            raise

    def test_TakingFromDestinationAllowsMoreToBeDelivered(self):
        """"""
        QSIZE=20
        BSIZE=10
        self.assert_(QSIZE > BSIZE)
        sched=scheduler()
        t=ThreadedSender(QSIZE)
        d=DoesNothingComponent().activate(Scheduler=sched)
        d.inboxes['inbox'].setSize(BSIZE)
        d.link((t,"outbox"),(d,"inbox"))
        
        s=sched.main()
        for _ in range(10):
            s.next()
        
        t.activate(Scheduler=sched)
        
        try:
            for _ in range(10):
                s.next()
            
            t.howManyToSend.put(QSIZE+BSIZE+10)
            
            # wait for a response, verify it filled its in queue
            result = t.feedback.get()
            self.assert_(result != "ALL SENT")
            self.assert_(result == QSIZE)
            
            # flush them through to the inbox queue of the destination
            for _ in range(BSIZE*5):
                s.next()
            
            # let the thread fill the newly free slots
            t.howManyToSend.put(QSIZE+BSIZE+10)
            result = t.feedback.get()
            self.assert_(result != "ALL SENT")
            self.assert_(result == BSIZE)
            
            
            # collect messages
            NUM_COLLECT = 0
            while NUM_COLLECT < BSIZE/2:
                while not d.dataReady("inbox"):
                    s.next()
                if d.dataReady("inbox"):
                    d.recv("inbox")
                    NUM_COLLECT += 1
                
            # let the main thread flush some message through from the thread
            for _ in range(50):
                s.next()
                
            t.howManyToSend.put(QSIZE+BSIZE+10)
            
            while t.feedback.qsize() == 0:
                s.next()
            
            result = t.feedback.get()
            self.assert_(result != "ALL SENT")
            self.assert_(result == NUM_COLLECT)
        except:
            t.howManyToSend.put("STOP")
            raise

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
        """__init__ - can accept no arguments"""
        self.assert_(threadedadaptivecommscomponent())
        
    def test_smoketest_oneargs(self):
        """__init__ - accepts one argument"""
        self.assert_(threadedadaptivecommscomponent(10))
        
    
    def test_addInbox(self):
        """addInbox - adds a new inbox with the specified name. Component can then receive from that inbox."""
        class T(threadedadaptivecommscomponent):
            def __init__(self):
                super(T,self).__init__()
                self.toTestCase = Queue.Queue()
                self.fromTestCase = Queue.Queue()
            def main(self):
                try:
                    boxname=self.addInbox("newbox")
                    self.toTestCase.put( (False,boxname) )
                    self.fromTestCase.get()
                    if not self.dataReady(boxname):
                        self.toTestCase.put( (True,"Data should have been ready at the new inbox") )
                        return
                    self.toTestCase.put( (False,self.recv(boxname)) )
                except Exception, e:
                    self.toTestCase.put( (True, str(e.__clas__.__name__) + str(e.args)) )
                    return
        sched=scheduler()
        t=T().activate(Scheduler=sched)
        
        timeout=10
        t.next()
        while t.toTestCase.empty():
            t.next()
            timeout=timeout-1
            time.sleep(0.05)
            self.assert_(timeout,"timed out")
        (err,msg) = t.toTestCase.get()
        self.assert_(not err, "Error in thread:"+str(msg))
        
        boxname=msg
        t._deliver("hello",boxname)
        try: 
            t.next()
            t.next()
        except StopIteration: pass
        t.fromTestCase.put(1)
        
        (err,msg) = t.toTestCase.get()
        self.assert_(not err, "Error in thread:"+str(msg))
        self.assert_(msg=="hello", "Data send through inbox corrupted, received:"+str(msg))
    
    def test_addOutbox(self):
        """addOutbox - adds a new outbox with the specified name. Component can then send to that inbox."""
        class T(threadedadaptivecommscomponent):
            def __init__(self,dst):
                super(T,self).__init__()
                self.toTestCase = Queue.Queue()
                self.fromTestCase = Queue.Queue()
                self.dst = dst
            def main(self):
                try:
                    boxname=self.addOutbox("newbox")
                    self.link( (self,boxname), self.dst )
                    msg = self.fromTestCase.get()
                    
                    self.send(msg,boxname)
                    self.toTestCase.put( (False, msg) )
                except Exception, e:
                    self.toTestCase.put( (True, str(e.__clas__.__name__) + str(e.args)) )
                    return
                
        class Recv(component):
           def __init__(self):
               super(Recv,self).__init__()
               self.rec = []
           def main(self):
               while 1:
                   yield 1
                   if self.dataReady("inbox"):
                       self.rec.append(self.recv("inbox"))
        
        sched=scheduler()
        r=Recv().activate(Scheduler=sched)
        t=T( (r,"inbox") ).activate(Scheduler=sched)
        
        t.fromTestCase.put("hello")
        while not t.toTestCase.qsize():
            t.next()
        t.next()
        (err,msg) = t.toTestCase.get()
        self.assert_(not err, "Error in thread:"+str(msg))
        
        try: 
            t.next()
        except StopIteration: pass
        try: 
            r.next()
            r.next()
        except StopIteration: pass
        self.assert_(r.rec == ["hello"], "Data send through outbox corrupted; r.rec = "+str(r.rec))
    
if __name__ == "__main__":
    unittest.main()