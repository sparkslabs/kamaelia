#!/usr/bin/env python
#
# Code migrated into mainline: --> Kamaelia.Util.test.test_Splitter.py
#
#

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

import unittest

import sys; sys.path.append("..")
from Splitter import PlugSplitter as Splitter
from Splitter import addsink, removesink, Plug

import Axon.Scheduler

class DummyComponent(Axon.Component.component):
    """Simple component that terminates on receiving suitable messages,
       but also logs all incoming messages"""
    def __init__(self):
        super(DummyComponent, self).__init__()
        self.inboxlog = []
        self.controllog = []
        
    def main(self):
        done=False
        while not done:
            yield 1
            if self.dataReady("inbox"):
                self.inboxlog.append(self.recv("inbox"))
            
            if self.dataReady("control"):
                msg = self.recv("control")
                self.controllog.append(msg)
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    done=True


class Splitter_Tests(unittest.TestCase):

    def test_InstantiateNoArgs(self):
        """Splitter instantiated with no args is just passthrough"""
        split = Splitter()
        split.activate()


    def test_PassThroughInboxOutbox(self):
        """Data sent to the inbox is sent on to the outbox"""
        split = Splitter()
        split.activate()

        for i in xrange(1,10):
            split._deliver( i, "inbox" )
        for _ in xrange(0,100):
            split.next()
        for i in xrange(1,10):
            self.assert_(len(split.outboxes["outbox"]))
            self.assert_(0==len(split.outboxes["signal"]))
            self.assert_( i == split._collect("outbox") )

        for i in xrange(1,10):
            split._deliver( i, "inbox" )
            split.next()
            split.next()
        for _ in xrange(0,10):
            split.next()
        for i in xrange(1,10):
            self.assert_(len(split.outboxes["outbox"]))
            self.assert_(0==len(split.outboxes["signal"]))
            self.assert_( i == split._collect("outbox") )

    
    def test_PassThroughControlSignal(self):
        """Data sent to the inbox is sent on to the outbox"""
        split = Splitter()
        split.activate()

        for i in xrange(1,10):
            split._deliver( i, "control" )
        for _ in xrange(0,100):
            split.next()
        for i in xrange(1,10):
            self.assert_(len(split.outboxes["signal"]))
            self.assert_(0==len(split.outboxes["outbox"]))
            self.assert_( i == split._collect("signal") )

        for i in xrange(1,10):
            split._deliver( i, "control" )
            split.next()
            split.next()
        for _ in xrange(0,10):
            split.next()
        for i in xrange(1,10):
            self.assert_(len(split.outboxes["signal"]))
            self.assert_(0==len(split.outboxes["outbox"]))
            self.assert_( i == split._collect("signal") )

    
    def test_SplitterShutdown(self):
        """If producerFinished or shutdownMicroprocess is received on the 'control' inbox they are passed on and the component shuts down"""
        for msg in [producerFinished(self), shutdownMicroprocess(self)]:
            split = Splitter()
            split.activate()
    
            for _ in xrange(0,10):
                split.next()
            self.assert_(0==len(split.outboxes["outbox"]))
            self.assert_(0==len(split.outboxes["signal"]))
    
            split._deliver( msg, "control" )
            try:
                for _ in xrange(0,10):
                    split.next()
                self.fail()
            except StopIteration:
                pass
            self.assert_(0==len(split.outboxes["outbox"]))
            self.assert_(1==len(split.outboxes["signal"]))
            received = split._collect("signal")
            self.assert_( msg == received )


            
    def test_SplitterAddLinkBoth(self):
        """Sending an addSink message to splitter links in an extra outbox and signal"""
        Axon.Scheduler.scheduler.run = Axon.Scheduler.scheduler()
        split = Splitter().activate()

        target1 = Axon.Component.component().activate()
        target2 = Axon.Component.component().activate()

        target1.link( (split,"outbox"), (target1, "inbox") )
        target1.link( (split,"signal"), (target1, "control") )
        
        addmsg = addsink(target2, "inbox", "control")
        split._deliver(addmsg, "configuration")

        execute = Axon.Scheduler.scheduler.run.main()
        
        for i in xrange(1,10):
            execute.next()

        for i in xrange(1,10):
            split._deliver(i, "inbox")
            split._deliver(10+i, "control")
            execute.next()
            
        for i in xrange(1,40):
            execute.next()

        # verify that the data has made it to the targets
        for i in xrange(1,10):
            self.assert_(target1.dataReady("inbox"))
            self.assert_(target1.dataReady("control"))
            self.assert_(i == target1.recv("inbox"))
            self.assert_(10+i == target1.recv("control"))
            
            self.assert_(target2.dataReady("inbox"))
            self.assert_(target2.dataReady("control"))
            self.assert_(i == target2.recv("inbox"))
            self.assert_(10+i == target2.recv("control"))

        # verify there is nothing left
        self.assert_(not target1.dataReady("inbox"))
        self.assert_(not target1.dataReady("control"))
        
        self.assert_(not target2.dataReady("inbox"))
        self.assert_(not target2.dataReady("control"))


        
    def test_SplitterAddLinkOutboxOnly(self):
        """Sending an addSink message to splitter links in an extra outbox"""
        Axon.Scheduler.scheduler.run = Axon.Scheduler.scheduler()
        split = Splitter().activate()

        target1 = Axon.Component.component().activate()
        target2 = Axon.Component.component().activate()

        target1.link( (split,"outbox"), (target1, "inbox") )
        target1.link( (split,"signal"), (target1, "control") )
        
        addmsg = addsink(target2, "inbox")
        split._deliver(addmsg, "configuration")

        execute = Axon.Scheduler.scheduler.run.main()
        
        for i in xrange(1,10):
            execute.next()

        for i in xrange(1,10):
            split._deliver(i, "inbox")
            split._deliver(10+i, "control")
            execute.next()
            
        for i in xrange(1,40):
            execute.next()

        # verify that the data has made it to the targets
        for i in xrange(1,10):
            self.assert_(target1.dataReady("inbox"))
            self.assert_(target1.dataReady("control"))
            self.assert_(i == target1.recv("inbox"))
            self.assert_(10+i == target1.recv("control"))
            
            self.assert_(target2.dataReady("inbox"))
            self.assert_(not target2.dataReady("control"))
            self.assert_(i == target2.recv("inbox"))

        # verify there is nothing left
        self.assert_(not target1.dataReady("inbox"))
        self.assert_(not target1.dataReady("control"))

        self.assert_(not target2.dataReady("inbox"))
        self.assert_(not target2.dataReady("control"))


        
    def test_SplitterAddLinkSignalOnly(self):
        """Sending an addSink message to splitter links in an extra signal"""
        Axon.Scheduler.scheduler.run = Axon.Scheduler.scheduler()
        split = Splitter().activate()

        target1 = Axon.Component.component().activate()
        target2 = Axon.Component.component().activate()

        target1.link( (split,"outbox"), (target1, "inbox") )
        target1.link( (split,"signal"), (target1, "control") )
        
        addmsg = addsink(target2, None, "control")
        split._deliver(addmsg, "configuration")

        execute = Axon.Scheduler.scheduler.run.main()
        
        for i in xrange(1,10):
            execute.next()

        for i in xrange(1,10):
            split._deliver(i, "inbox")
            split._deliver(10+i, "control")
            for j in xrange(1,10):
                execute.next()
            
        # verify that the data has made it to the targets
        for i in xrange(1,10):
            self.assert_(target1.dataReady("inbox"))
            self.assert_(target1.dataReady("control"))
            self.assert_(i == target1.recv("inbox"))
            self.assert_(10+i == target1.recv("control"))
            
            self.assert_(not target2.dataReady("inbox"))
            self.assert_(target2.dataReady("control"))
            self.assert_(10+i == target2.recv("control"))

        # verify there is nothing left
        self.assert_(not target1.dataReady("inbox"))
        self.assert_(not target1.dataReady("control"))

        self.assert_(not target2.dataReady("inbox"))
        self.assert_(not target2.dataReady("control"))


        
    def test_SplitterDelLinkBoth(self):
        """Sending an delSink message to splitter unlinks in the extra outbox and signal"""
        Axon.Scheduler.scheduler.run = Axon.Scheduler.scheduler()
        split = Splitter().activate()

        target1 = Axon.Component.component().activate()
        target2 = Axon.Component.component().activate()

        target1.link( (split,"outbox"), (target1, "inbox") )
        target1.link( (split,"signal"), (target1, "control") )
        
        addmsg = addsink(target2, "inbox", "control")
        split._deliver(addmsg, "configuration")

        execute = Axon.Scheduler.scheduler.run.main()
        
        for i in xrange(1,10):
            execute.next()

        for i in xrange(1,10):
            if i == 5:
                delmsg = removesink(target2, "inbox", "control")
                split._deliver(delmsg, "configuration")
            
            split._deliver(i, "inbox")
            split._deliver(10+i, "control")

            for j in xrange(1,10):
                execute.next()
            
        for i in xrange(1,40):
            execute.next()

        # verify that the data has made it to the targets
        for i in xrange(1,5):
            self.assert_(target1.dataReady("inbox"))
            self.assert_(target1.dataReady("control"))
            self.assert_(i == target1.recv("inbox"))
            self.assert_(10+i == target1.recv("control"))
            
            self.assert_(target2.dataReady("inbox"))
            self.assert_(target2.dataReady("control"))
            self.assert_(i == target2.recv("inbox"))
            self.assert_(10+i == target2.recv("control"))

        for i in xrange(5,10):
            self.assert_(target1.dataReady("inbox"))
            self.assert_(target1.dataReady("control"))
            self.assert_(i == target1.recv("inbox"))
            self.assert_(10+i == target1.recv("control"))
            
            self.assert_(not target2.dataReady("inbox"))
            self.assert_(not target2.dataReady("control"))
        
        # verify there is nothing left
        self.assert_(not target1.dataReady("inbox"))
        self.assert_(not target1.dataReady("control"))
        
        self.assert_(not target2.dataReady("inbox"))
        self.assert_(not target2.dataReady("control"))


class Plug_Tests(unittest.TestCase):

    def test_PluggingInAndTxfer(self):
        """Plug instantiated with splitter and component and passes data through to component."""
        Axon.Scheduler.scheduler.run = Axon.Scheduler.scheduler()

        splitter = Splitter()
        splitter.activate()

        target = DummyComponent()
        plug = Plug(splitter, target).activate()

        execute = Axon.Scheduler.scheduler.run.main()
        
        for i in xrange(1,1000):
            execute.next()

        #pass some data in
        for i in xrange(1,10):
            splitter._deliver(i, "inbox")
            splitter._deliver(10+i, "control")
            for i in xrange(1,100):
                execute.next()

        # verify it reached the target
        self.assert_(target.inboxlog == range(1,10))
        self.assert_(target.controllog == range(11,20))

        

    def test_Unplugging(self):
        """Plug will unplug and shutdown when child component dies."""
        Axon.Scheduler.scheduler.run = Axon.Scheduler.scheduler()

        splitter = Splitter()
        splitter.activate()

        target = DummyComponent()
        plug = Plug(splitter, target).activate()

        execute = Axon.Scheduler.scheduler.run.main()
        
        for i in xrange(1,100):
            execute.next()

        #send shutdown msg
        msg = producerFinished()
        target._deliver(msg, "control")

        for i in xrange(1,100):
            execute.next()

        # verify it reached the target
        self.assert_(target.controllog == [msg])

        # verify the plug has shutdown
        self.assert_(plug._isStopped())

        # verify the plug has no linkages
        self.assert_(not plug.postoffice.linkages)

        # verify that splitter only has outboxes "outbox" and "signal" now
        self.assert_( len(splitter.outboxes) == 2)
        self.assert_( "outbox" in splitter.outboxes)
        self.assert_( "signal" in splitter.outboxes)
        
                
if __name__=='__main__':
   unittest.main()
