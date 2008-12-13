#!/usr/bin/env python2.3
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

import unittest
from Kamaelia.Util.Splitter import PlugSplitter as Splitter
from Kamaelia.Util.Splitter import addsink, removesink
from Kamaelia.Util.Splitter import Plug
from Axon.Ipc import producerFinished, shutdownMicroprocess
import Axon.Scheduler
from Axon.Scheduler import scheduler
from Axon.Linkage import linkage
from Axon.Component import component
from Axon.Axon import AxonObject
import gc
#from test_Component import Component_Test


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

class TestComponent(component):
   Inboxes = ["inbox","control","test"]

class DummyPostman:
   def registerlinkage(self,linkage):
      self.linkage=linkage
   
def runrepeat(gen, count = 100):
   """This just runs the specified generator the specified number of times.  This
   is used to try to make sure expected behaviour has sufficient timeslots to
   succeed without taking too long."""
   for i in xrange(count):
      gen.next()
   
class Splitter_Test(unittest.TestCase):
   def setUp(self):
      self.src = component()
      self.dst = component()
      self.dst2 = TestComponent()
      self.controller = component()
      self.split = Splitter()
      self.runner = self.split.main()
      self.linkin = linkage(self.src,self.split)
      self.linkcont = linkage(self.controller, self.split, sinkbox="configuration")
      self.links = [self.linkin, self.linkcont]
#      self.linkout1 = linkage(self.split,self.dst)
#      self.linkout2 = linkage(self.split,self.dst2, sourcebox="out2")
   
   def deliverhelper(self):
      for i in self.links:
         while i.dataToMove():
            i.moveData()
      self.split.postoffice.domessagedelivery()
   
   def test_isacomponent(self):
      "__init__ - Splitter is a component."
      self.failUnless(isinstance(self.split,component))
   
   def test_simplepassthrough_defaultbox(self):
      """mainBody - This test sets up a sink and checks it receives sent messages using the default box."""
      self.controller.send(addsink(self.dst))
      self.deliverhelper()
      runrepeat(self.runner)
      for i in xrange(0,10):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         self.failUnless(self.dst.dataReady())
         self.failUnless(self.dst.recv() == i)
         
   def test_simplepassthrough(self):
      """mainBody - addsink -> configuration - An addsink object is sent to the
      configuration box and it creates a new sink.  A new outbox is created and
      linked to the sink."""
      self.controller.send(addsink(self.dst2,"test"))
      self.deliverhelper()
      runrepeat(self.runner)
      for i in xrange(0,10):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         self.failUnless(self.dst2.dataReady("test"))
         self.failUnless(self.dst2.recv("test") == i)
   
   def test_addOutboxes(self):
      """mainBody - addsink->configurations - Adds a whole set of sinks and checks
      they all receive expected messages."""
      boxes = 10
      boxlist = []
      for x in xrange(boxes):
         c=component()
         boxlist.append(c)
         self.controller.send(addsink(c))
         self.deliverhelper()
         runrepeat(self.runner)
      for i in xrange(20):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         for comp in boxlist:
            self.failUnless(comp.dataReady())
            self.failUnless(comp.recv() == i)

   def test_addSinkInboxes_passthrough(self):
      """mainBody - addsink->configurations - Adds a whole set of sinks and checks
      they all receive expected messages.  Complicated by setting the sink to
      passthrough and to be to an inbox."""
      boxes = 10
      boxlist = []
      for x in xrange(boxes):
         c=component()
         boxlist.append(c)
         self.links.append(linkage(source=c, sourcebox="outbox", sink=c, sinkbox="control"))
         self.controller.send(addsink(c,"outbox",2))
         self.deliverhelper()
         runrepeat(self.runner)
      for i in xrange(20):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         self.deliverhelper()
         for comp in boxlist:
            self.failUnless(comp.dataReady("control"))
            self.failUnless(comp.recv("control") == i)
            
   def test_removeOutboxes_default(self):
      """mainBody - addsink|removesink->configuration - Tests addition and removal
      of sinks using the default box arguments.  Adds a array of sinks, removes
      the odd items and then checks that messages are delivered to the even
      sinks and not the odd ones."""
      boxes = 10
      boxlist = {}
      for x in xrange(boxes):
         c=component()
         boxlist[x] = c
         self.controller.send(addsink(c,"inbox"))
         self.deliverhelper()
         runrepeat(self.runner)
      for x in xrange(1,boxes,2):
         self.controller.send(removesink(boxlist[x]))
         self.deliverhelper()
         runrepeat(self.runner)
      for i in xrange(20):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         for j in xrange(0,boxes,2):
            self.failUnless(boxlist[j].dataReady("inbox"))
            self.failUnless(boxlist[j].recv("inbox") == i)   
         for j in xrange(1,boxes,2):
            self.failIf(boxlist[j].dataReady("inbox"))
   
   def test_removeOutboxes(self):
      """mainBody - addsink|removesink->configuration inbox - Tests addition and
      removal of sinks.  Adds a array of sinks, removes the odd items and then
      checks that messages are delivered to the even sinks and not the odd ones."""
      boxes = 10
      boxlist = {}
      for x in xrange(boxes):
         c=TestComponent()
         boxlist[x] = c
         self.controller.send(addsink(c,"test"))
         self.deliverhelper()
         runrepeat(self.runner)
      for x in xrange(1,boxes,2):
         self.controller.send(removesink(boxlist[x],"test"))
         self.deliverhelper()
         runrepeat(self.runner)
      for i in xrange(20):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         for j in xrange(0,boxes,2):
            self.failUnless(boxlist[j].dataReady("test"))
            self.failUnless(boxlist[j].recv("test") == i)   
         for j in xrange(1,boxes,2):
            self.failIf(boxlist[j].dataReady("test"))
   
   def test_cleanup(self):
      """mainBody - addsink|removesink->configuration - Checks that there are no
      object leakages by adding and then removing a sink and checking the
      garbage collecter for its count of AxonObjects and lists."""
      self.controller.send(addsink(self.dst))
      before = 0
      for x in gc.get_objects():
         if isinstance(x, AxonObject) or isinstance(x,list):
            before = before + 1
      self.controller.send(addsink(self.dst))
      self.controller.send(removesink(self.dst))
      after = 0
      for x in gc.get_objects():
         if isinstance(x, AxonObject) or isinstance(x,list):
            after = after + 1
      self.failUnless(before == after)
      
   def drd(self):
      "Deliver Run Deliver"
      self.deliverhelper()
      runrepeat(self.runner)
      self.deliverhelper()
      
   def test_multipleboxessinglecomponent(self):
      """mainBody - addsink|removesink->configuration - Checks that multiple sink
      inboxes on a single component can be added and removed independently."""
      self.controller.send(addsink(self.dst2,"test"))
      self.drd()
      self.src.send("ba")
      self.drd()
      self.failUnless(self.dst2.dataReady("test"))
      self.failIf(self.dst2.dataReady("inbox"))
      self.failIf(self.dst2.dataReady("control"))
      self.failUnless(self.dst2.recv("test") == "ba")
      self.controller.send(addsink(self.dst2))
      self.drd()
      self.src.send("da")
      self.drd()
      self.failUnless(self.dst2.dataReady("test"))
      self.failUnless(self.dst2.dataReady("inbox"))
      self.failIf(self.dst2.dataReady("control"))
      self.failUnless(self.dst2.recv("test") == "da")
      self.failUnless(self.dst2.recv("inbox") == "da")
      self.controller.send(addsink(self.dst2,"control"))
      self.drd()
      self.src.send("bing")
      self.drd()
      self.failUnless(self.dst2.dataReady("test"))
      self.failUnless(self.dst2.dataReady("inbox"))
      self.failUnless(self.dst2.dataReady("control"))
      self.failUnless(self.dst2.recv("test") == "bing")
      self.failUnless(self.dst2.recv("inbox") == "bing")
      self.failUnless(self.dst2.recv("control") == "bing")
      self.controller.send(removesink(self.dst2,"inbox"))
      self.drd()
      self.src.send('a')
      self.drd()
      self.failUnless(self.dst2.dataReady("test"))
      self.failIf(self.dst2.dataReady("inbox"))
      self.failUnless(self.dst2.dataReady("control"))
      self.failUnless(self.dst2.recv("test") == 'a')
      self.failUnless(self.dst2.recv("control") == 'a')
      self.controller.send(removesink(self.dst2,"control"))
      self.drd()
      self.src.send('b')
      self.drd()
      self.failUnless(self.dst2.dataReady("test"))
      self.failIf(self.dst2.dataReady("inbox"))
      self.failIf(self.dst2.dataReady("control"))
      self.failUnless(self.dst2.recv("test") == 'b')
      self.controller.send(removesink(self.dst2,"test"))
      self.drd()
      self.src.send('c')
      self.drd()
      self.failIf(self.dst2.dataReady("test"))
      self.failIf(self.dst2.dataReady("inbox"))
      self.failIf(self.dst2.dataReady("control"))

#-----------------
   def __test_createsink_defaultbox(self):  # SMELL - internal diagnostic
      """createsink - Checks that a new sink is created and linked on calling creatsink with default box argument"""
      self.split.createsink(self.dst)
      for i in xrange(0,10):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         self.failUnless(self.dst.dataReady())
         self.failUnless(self.dst.recv() == i)
         
   def __test_simplepassthrough_createsink(self): # SMELL - internal diagnostic
      """createsink - Checks that a new sink is created and linked on calling creatsink with arguments"""
      self.split.createsink(self.dst2,"test")
      for i in xrange(0,10):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         self.failUnless(self.dst2.dataReady("test"))
         self.failUnless(self.dst2.recv("test") == i)      

   def __test_addOutboxes_createsink(self):  # SMELL - internal diagnostic
      """createsink - Called repeatedly.  Adds a whole set of sinks and checks
      they all receive expected messages."""
      boxes = 10
      boxlist = []
      for x in xrange(boxes):
         c=component()
         boxlist.append(c)
         self.split.createsink(c)
      for i in xrange(20):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         for comp in boxlist:
            self.failUnless(comp.dataReady())
            self.failUnless(comp.recv() == i)
            
class PlugSplitter_Tests(unittest.TestCase):

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
