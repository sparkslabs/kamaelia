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
from Kamaelia.Util.Splitter import Splitter, addsink, removesink
from Axon.Scheduler import scheduler
from Axon.Linkage import linkage
from Axon.Component import component
from Axon.Axon import AxonObject
import gc
#from test_Component import Component_Test

class TestComponent(component):
   Inboxes = ["inbox","control","test"]

class DummyPostman:
   def registerlinkage(self,linkage):
      self.linkage=linkage
   
def runrepeat(gen, count = 10):
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
   def test_createsink_defaultbox(self):
      """createsink - Checks that a new sink is created and linked on calling creatsink with default box argument"""
      self.split.createsink(self.dst)
      for i in xrange(0,10):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         self.failUnless(self.dst.dataReady())
         self.failUnless(self.dst.recv() == i)
         
   def test_simplepassthrough_createsink(self):
      """createsink - Checks that a new sink is created and linked on calling creatsink with arguments"""
      self.split.createsink(self.dst2,"test")
      for i in xrange(0,10):
         self.src.send(i)
         self.deliverhelper()
         runrepeat(self.runner)
         self.deliverhelper()
         self.failUnless(self.dst2.dataReady("test"))
         self.failUnless(self.dst2.recv("test") == i)      

   def test_addOutboxes_createsink(self):
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
            
if __name__=='__main__':
   unittest.main()
