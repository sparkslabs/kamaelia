#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Aim: Full coverage testing of the selector class
#

# Test the module loads
import unittest
import sys ; sys.path.append("..")
from Kamaelia.Internet.Selector import selectorComponent
from Axon.Component import component
import Kamaelia.Internet.Selector
from Axon.AxonExceptions import ServiceAlreadyExists
import Axon.CoordinatingAssistantTracker

def preservedIncreasedItemCount(preList, postList):
   "Boolean that returns true if the number of items in each list has increased, and preserved the old items"
   return (len(preList)<len(postList)) and (reduce(bool.__and__, [ x in postList for x in preList ]))

def linkMatchesExpected(theLink, expected):
   "Compares a link with expected values"
   return expected[0] == theLink.sourcePair() and expected[1] == theLink.sinkPair()

class sampleComponent(component):
   Inboxes = selectorComponent.requiredInboxes
   Outboxes = selectorComponent.requiredOutboxes


class selector_Test(unittest.TestCase):
   def test__init__noArgs(self):
      "__init__ - Can be called without any arguments"
      mySelector = selectorComponent()
      self.assertNotEqual(None, mySelector, "Non-None selector created")
      self.assertNotEqual(None, mySelector.inboxes, "Component superconstructor was called")

   def setup_forWireInComponent(self):
      import socket
      theComponent = sampleComponent()
      theSocket = socket.socket()
      r = theComponent, theSocket
      mySelector = selectorComponent()
      return mySelector, r, theComponent

   def test_wireInComponent(self):
      "wireInComponent - Wiring in a socket/component pair means creating a new inbox/outbox pair to talk to it, linking those to the component, and storing a lookup of socket to inbox/outbox pair"
      mySelector, r, theComponent = self.setup_forWireInComponent()

      preInboxes, preOutboxes = list(mySelector.inboxes), list(mySelector.outboxes)
      mySelector.wireInComponent(r)

      # Check that the wiring in succeeded (Post conditions satisfied)
      postInboxes, postOutboxes = list(mySelector.inboxes), list(mySelector.outboxes)
      link1,link2 = mySelector.postoffice.linkages
      expectedLink1 = (theComponent,"signal"),(mySelector, "socketAdaptorFeedback")
      expectedLink2 = (mySelector,"socketAdaptorSignal"),(theComponent, "DataReady")

      self.assert_(preservedIncreasedItemCount(preInboxes, postInboxes),"Number of inboxes should have been added to, and be a superset of before" )
      self.assert_(preservedIncreasedItemCount(preOutboxes, postOutboxes),"Number of outboxes should have been added to, and be a superset of before" )
      self.assertEqual(2, len(mySelector.postoffice.linkages),  "Two linkages were added")
      self.assert_(linkMatchesExpected(link1, expectedLink1), "First link is from supplied component to the selector")
      #print; print "LINKAGE 2: ", link2
      #print "EXPECTED:", expectedLink2
      self.assert_(linkMatchesExpected(link2, expectedLink2), "Second link is from the selector  to the supplied component")

   def test_unwireComponent(self):
      mySelector, r, theComponent = self.setup_forWireInComponent()
      mySelector.wireInComponent(r)

      """
      SEL: Socket Error: Bad file descriptor
      SEL: We want to remove the socket from the set of things to check
      SEL:    Specifically:  <socket._socketobject object at 0x405b1b6c>
      SEL: We want to signal the component to shutdown
      SEL: We want to remove all references we have
      SEL:    Specifically:
                        socketAdaptorFeedback
                        socketAdaptorSignal
                        Component Kamaelia.Internet.ConnectedSocketAdapter.ConnectedSocketAdapter_17 [
                              inboxes : {'control': [], 'DataSend': [], 'Initialise': [], 'DataReady': [
                                            <Axon.Ipc.status object at 0x405919ec>, <Axon.Ipc.status object at 0x4059172c>]}
                              outboxes : {'FactoryFeedback': [], 'outbox': [], 'signal': []}
      SEL: We let the thing managing the socket close the socket
      SEL: Component that needs a shutdown message
               Component Kamaelia.Internet.ConnectedSocketAdapter.ConnectedSocketAdapter_17 [
                     inboxes : {'control': [], 'DataSend': [], 'Initialise': [], 'DataReady': [
                               <Axon.Ipc.status object at 0x405919ec>, <Axon.Ipc.status object at 0x4059172c>]}
                     outboxes : {'FactoryFeedback': [], 'outbox': [], 'signal': []}
      SEL: Contents out inboxes it has {'control': [], 'DataSend': [], 'Initialise': [], 'DataReady': [
                  <Axon.Ipc.status object at 0x405919ec>, <Axon.Ipc.status object at 0x4059172c>]}
      SEL: Contents of DataReady inbox ['write ready', 'write ready']
      """
   # This test is commented out, since the usage API changed, and this was decided against
   # The reason this was changed is due to the change to a service model rather than "just"
   # a usage model.
   def _test__init__minValidReaders(self):
      "__init__ - Should be called with iterables for reader,writer, and exceptional containing pairs of (socket, appropriate socket adaptor)"
      # This test uses dummy values.
      import socket
      r= [ (sampleComponent(),socket.socket()) for x in "hello" ]
      w= [ (sampleComponent(),socket.socket()) for x in "hello" ]
      x= [ (sampleComponent(),socket.socket()) for x in "hello" ]
      mySelector = selectorComponent(exceptionals=x, writers=w, readers=r)
      self.assertEqual(mySelector.readers, r, "Supplied readers were stored")
      self.assertEqual(mySelector.exceptionals, x, "Supplied exceptionals were stored")
      self.assertEqual(mySelector.writers, w, "Supplied writers were stored")

   def test__init__nonListArguments(self):
      "__init__ - Raises TypeError when called with random junk"
      self.assertRaises(TypeError, selectorComponent,None,
      {"exceptionals":1, "writers":"hello", "readers":None})

   def test__init__stringArguments(self):
      "__init__ - Raises TypeError when called with iterables containing junk"
      self.assertRaises(TypeError, selectorComponent,None,
            {"exceptionals":"world",
             "writers":"hello",
             "readers":"goodbye"})
             
   def test_setSelectorService_smoketest(self):
        "setSelectorService - Registers a selector with a Coordinating Assistant Tracker"
        try:
            Kamaelia.Internet.Selector.selectorComponent.setSelectorService()
            self.fail("Expected an exception to be thrown.  Selector argument required.")
        except TypeError,e:
            pass
        _selector = selectorComponent()
        Kamaelia.Internet.Selector.selectorComponent.setSelectorService(_selector)
        registeredservice,componentToActive = Kamaelia.Internet.Selector.selectorComponent.getSelectorService()
        _selectorreturned,serviceinbox = registeredservice
        self.failUnless(_selectorreturned is _selector)
        self.failUnless(serviceinbox == "notify")
        self.failUnless(componentToActive == None)
        _selector2 = selectorComponent()
        try:
            Kamaelia.Internet.Selector.selectorComponent.setSelectorService(_selector2)
            self.fail("Expected an exception")
        except ServiceAlreadyExists,e:
            # This is the expected success state. (Probably should use assertRaises :-)
            pass
            
   def test_setSelectorService_targettracker(self):
        "setSelectorService - Registers a selector with a Coordinating Assistant Tracker"
        cat = Axon.CoordinatingAssistantTracker.coordinatingassistanttracker()
        _selector = selectorComponent()
        Kamaelia.Internet.Selector.selectorComponent.setSelectorService(_selector,cat)
        myservice,componentToActive = Kamaelia.Internet.Selector.selectorComponent.getSelectorService(cat)
        _selectorreturned,serviceinbox = myservice
        self.failUnless(_selectorreturned is _selector)
        self.failUnless(serviceinbox == "notify")
        self.failUnless(componentToActive == None)

        globalservice,componentToActive = Kamaelia.Internet.Selector.selectorComponent.getSelectorService()
        _globalselector,_globalserviceinbox = globalservice
        self.failIf(_globalselector is _selector)
            
if __name__=="__main__":
   unittest.main()


   if 0:
      class foo(object):
         def __init__(self,arg):
            self.arg=arg
         def __str__(self):
            return str(self.arg)
         __repr__=__str__
         def __lshift__(self,thing):
            print self, " << ", thing
            return self
         def __rshift__(self,thing):
            print self, " >> ", thing
            return self
         def __or__(self,thing):
            print self, " | ", thing
            return self
         def __and__(self,thing):
            print self, " & ", thing
            return self
         def __xor__(self,thing):
            print self, " ^ ", thing
            return self
      class message(foo):
         pass
      class box(foo):
         pass
      class recieve(foo):
         def __init__(self):
            super(recieve, self).__init__(-1)

      source=foo(0)
      sink=foo(1)
      sink2=foo(2)
      sink3=foo(2)
      source >> { "outbox1" : (sink, "inbox"),
                  "outbox2" : (sink2, "log")
               }
      source <<  { "outbox1" : [(sink, "inbox"),(sink2, "trace")],
                  "outbox2" : (sink3, "log")
               }
      foo(1) >> foo(2) << foo(3) | foo(4)  & foo(5) ^ foo(6)
      foo(1) << ("inbox",5)

      message("hello") >> box("outbox")
      recieve() << box("inbox")






