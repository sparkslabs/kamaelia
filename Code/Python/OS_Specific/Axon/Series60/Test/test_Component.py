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
# Aim: Full coverage testing of the Component class
#

# Test the module loads
import unittest
import re
#import sys ; sys.path.append(".") ; sys.path.append("..")
from Axon.Component import *
import Axon.Linkage
Linkage = Axon.Linkage
#from Scheduler 
class TComponent(component):
    def __init__(self):
        super(TComponent,self).__init__()
        self.tc1=component()
        self.tc2=component()
        #self.tc1.synchonisedBox()
        #self.tc2.synchonisedBox(boxtype="source",boxdirection="inbox",boxname="inbox")
        self.link(source=(self.tc1,"outbox"),sink=(self.tc2,"inbox"),synchronous=True)
        self.link(source=(self.tc1,"signal"),sink=(self.tc2,"control"),synchronous=True,pipewidth=3)

class TComponentAsync(component):
    def __init__(self):
        super(TComponentAsync,self).__init__()
        self.tc1=component()
        self.tc2=component()
        #self.tc1.synchonisedBox()
        #self.tc2.synchonisedBox(boxtype="source",boxdirection="inbox",boxname="inbox")
        self.link(source=(self.tc1,"outbox"),sink=(self.tc2,"inbox"))
        self.link(source=(self.tc2,"signal"),sink=(self.tc1,"control"))

class TestMainLoopComponent(component):
    def __init__(self):
        super(TestMainLoopComponent, self).__init__()
        self.count = 0
    def mainBody(self):
        self.count = self.count + 1
        if self.count < 1000:
            return self.count
        return None

class closeDownCompTestException(Exception):
    pass
        
class TestMainLoopComponentClosedown(TestMainLoopComponent):
    def closeDownComponent(self):
        raise closeDownCompTestException

class dummylinkage:
    dummylinkagelist = []
    def __init__(self, source, sink, sourcebox="outbox", sinkbox="inbox",
                postoffice=None, passthrough=0, pipewidth=0,
                synchronous=False):
        self.source=source
        self.sink=sink
        self.sourcebox=sourcebox
        self.sinkbox=sinkbox
        self.showtransit=0
        self.passthrough=passthrough
        self.pipewidth=pipewidth
        self.synchronous=synchronous
        dummylinkage.dummylinkagelist.append(self)
        
class testpostman:
    def __init__(self):
        self.registereditems = dict()
        self.calledcount = 0
        self.deregisteredComponents = []
    def register(self, cname, cobject):
        self.registereditems[cname]=cobject
        self.calledcount=self.calledcount+1
    def deregister(self, name=None, component=None):
        if component:
            self.deregisteredComponents.append(component)
        if name:
            self.deregisteredName.append(name)

class testpostman2(postman):
    def istestpostman2(self):
        return True

class Component_Test(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "__init__ - Class constructor is expected to be called without arguments."
      testcomponent = component()
      self.failUnless(isinstance(testcomponent,microprocess), "Component should be a Microprocess")
      self.failUnless(testcomponent.Usescomponents==[],"Basic component should not depend on other components")
      self.failUnless(testcomponent.Inboxes.count("inbox")==1,"There should be one 'inbox' in the Inboxes structure.")
      self.failUnless(testcomponent.Inboxes.count("control")==1,"There should be one 'control' in the Inboxes structure.")
      self.failUnless(testcomponent.Outboxes.count("outbox")==1,"There should be one 'outbox' in the Outboxes structure.")
      self.failUnless(testcomponent.Outboxes.count("signal")==1,"There should be one 'signal' in the Outboxes structure.")
      for x in testcomponent.Inboxes:
        self.failUnless(testcomponent.inboxes[x]==[],"Unexpected inbox data structure for "+x+".")
      for x in testcomponent.Outboxes:
        self.failUnless(testcomponent.outboxes[x]==[],"Unexpected outbox data structure for "+x+".")
      self.failUnless(testcomponent.children==[], "The children component should be an empty list.")
      self.failUnless(testcomponent.synchronised.items()==[],"Synchronised box list is empty.")
      self.failUnless(testcomponent.postoffice.next()=="initialised","Post office not properly inialised.")

   def test__synchronisedBox(self):
      """synchronisedBox - Called with no arguments sets the outbox 'outbox' to being a synchronised box, with a maximum depth of 1.
      It is also called with arguments to set the signal inbox to be synchronised with a depth of 5.  The set variables are checked and 
      the synchronised structure is checked that nothing has defaulted to synchronised."""
      tc=component()
      tc._synchronisedBox()
      self.failUnless(tc.synchronised["outbox"]["outbox"]==("sink",1) ,"Synchronised outbox not properly set up.")
      tc._synchronisedBox(boxtype="source",boxdirection="inbox",boxname="control",maxdepth=5)
      self.failUnless(tc.synchronised["inbox"]["control"]==("source",5),"Synchronised inbox not properly set up.")
      self.failUnless(len(tc.synchronised)==2,"More synchronised types than expected.")
      self.failUnless(len(tc.synchronised["inbox"])==1,"More inboxes than expected!")
      self.failUnless(len(tc.synchronised["outbox"])==1,"More outboxes than expected!")
      
   def test_synchronisedSend(self):
      "synchronisedSend - Takes a list of things to send, and returns a generator that when repeatedly called tries to send data over a synchronised outbox."
      tcomp=TComponent()
      sender = tcomp.tc1.synchronisedSend([1,2,3,4])
#      tcomp.postoffice.domessagedelivery()
      self.failIf(tcomp.tc2.dataReady(),"Data should not arrive unless the synchronisedSend generator has been called")
      self.failUnless(sender.next()==1,"Buffer length of one should allow first item into buffer")
      self.failUnless(sender.next()==-1,"Buffer length of one should hold on second attempt.")
      tcomp.postoffice.domessagedelivery()
      self.failUnless(sender.next()==2,"Extra buffer room should be available after message delivery.")
      tcomp.postoffice.domessagedelivery()
      self.failUnless(sender.next()==-1,"Delivery should fail so this should fail as the outbox buffer is occupied.")
      self.failUnless(tcomp.tc2.recv()==1,"First message should be delivered.")
      tcomp.postoffice.domessagedelivery()
      self.failUnless(sender.next()==3,"Third item should be accepted.")
      self.failUnless(sender.next()==-1,"Out buffer should be full again. -1 yielded for failure.")
      self.failUnless(tcomp.tc2.recv()==2,"Second item receive failed.")
      tcomp.postoffice.domessagedelivery()
      self.failUnless(tcomp.tc2.recv()==3,"Third item delivery failed.")
      self.failUnlessRaises(StopIteration, sender.next),# "Generator did not complete as expected")
      sender = tcomp.tc1.synchronisedSend([1,2,3,4,5,6,7,8],"signal")
      self.failUnless(sender.next()==1,"Initial synchronised send should work.")
      self.failUnless(sender.next()==2,"Pipewidth 3 should allow second item in outbox.")
      self.failUnless(sender.next()==3,"Pipewidth 3 should allow third item in outbox.")
      self.failUnless(sender.next()==-1,"Pipe should be full!")
      tcomp.postoffice.domessagedelivery()
      tcomp.postoffice.domessagedelivery()
      tcomp.postoffice.domessagedelivery()
      self.failUnless(sender.next()==4,"Should be out buffer space after deliveries.")
      self.failUnless(sender.next()==5,"Should be out buffer space after deliveries.")
      self.failUnless(sender.next()==6,"Should be out buffer space after deliveries.")
      self.failUnless(sender.next()==-1,"Both buffers should be full.")
      self.failUnless(tcomp.tc2.recv("control")==1,"Should receive first message at this point.")
      self.failUnless(sender.next()==-1,"Room in inbox but message delivery has not occured yet.")
      tcomp.postoffice.domessagedelivery()
      self.failUnless(sender.next()==7,"This message should fit in the buffer.")
      self.failUnless(sender.next()==-1,"Buffers should be full.")
      self.failUnless(tcomp.tc2.recv("control")==2, "Second message is collected.")
      tcomp.postoffice.domessagedelivery()
      self.failUnlessRaises(StopIteration, sender.next)
      for x in xrange(3,9):
        self.failUnless(tcomp.tc2.recv("control")==x,"Message reception error")
        tcomp.postoffice.domessagedelivery()
      self.failIf(tcomp.tc2.dataReady("control"), "All messages should have been received already.")
      
   def test___str__strict(self):
      "__str__ - Returns a string representation of the component- consisting of Component,representation of inboxes, representation of outboxes."
      #First test against an expected string.  Strict test, may have to change.
      t = TComponent()
      t.send("fish")
      t.send("chips","signal")
      stricttest = "Component (\S*\.)+TComponent_\d+ \[ inboxes : \{'control'\: \[\], 'inbox': \[\]\} outboxes : \{'outbox': \['fish'\], 'signal': \['chips'\]\}"
      self.failUnless(re.match(stricttest,str(t)),"Strict match failed with expected string.  Any format change will have broken this.\n\n"+str(t)+"\n\n")
   def test___str__relaxed(self):
      "__str__ - Returns a string that contains the fact that it is a component object and the name of it."
      #Test for vital details.  Not strict shouldn't be broken
      t = TComponent()
      t.send("fish")
      t.send("chips","signal")
      relaxedtest = "(C|c)(omponent|OMPONENT).*" + t.name
      self.failUnless(re.search(relaxedtest,str(t)), "Relaxed match failed.  Vital information missing (That it is a component and its name).")
       
   def test__activityCreator(self):
      "_activityCreator - Always returns true.  Components are microprocesses instantiated by users typically - thus they are creators of activity, not slaves to it. Internal function."
      t=component()
      self.failUnless(t._activityCreator()==True,"_activityCreator should always be True.")
      t=TComponent()
      self.failUnless(t._activityCreator()==True,"_activityCreator should always be True")
      
   def test___addChild(self):
      "__addChild - Registers the component as a child of the component. Internal function. ttbw"
      pass
      
   def test_addChildren(self):
      """addChildren - All arguments are added as child components of the component. 
      This involves registering them with the postoffice (of class postman) and adding them to the list childred"""
      parent=component()
      parent.postoffice = testpostman()
      child1=component()
      child2=component()
      parent.addChildren(child1,child2)
      self.failUnless(parent.postoffice.calledcount == 2,"Wrong number of components registered with postoffice.")
      self.failUnless(parent.postoffice.registereditems[child1.name]==child1,"Component improperly registered.")
      self.failUnless(parent.postoffice.registereditems[child2.name]==child2,"Component improperly registered.")
      self.failUnless(parent.children.count(child1)==1,"Component not added to children list.")
      self.failUnless(parent.children.count(child2)==1,"Component not added to children list.")
      countitems = 0
      for x in parent.children:
        countitems = 1+countitems
      self.failUnless(countitems==2,"Children list has unexpected contents.")
      
   def test_removeChild(self):
      "removeChild - Removes the specified component from the set of child components and deregisters it from the postoffice."
      parent=component()
      parent.postoffice=testpostman()
      child=component()
      parent.addChildren(child)
      parent.removeChild(child)
      self.failUnless(parent.children.count(child)==0,"Child not removed from children list.")
      if parent.postoffice.deregisteredComponents.count(child)!=1 and parent.postoffice.deregisteredName.count(child.name)!=1:
          self.fail("Child not properply deregistered from postoffice.")
      
   def test_childComponents(self):
      "childComponents - Returns the list of children components of this component."
      parent=component()
      child1=component()
      child2=component()
      child3=component()
      parent.addChildren(child1,child2,child3)
      childlist=parent.childComponents()
      self.failUnless(childlist.count(child1)==1,"Child list corrupted.")
      self.failUnless(childlist.count(child2)==1,"Child list corrupted.")
      self.failUnless(childlist.count(child3)==1,"Child list corrupted.")
      self.failUnless(len(childlist)==3,"Unexpected child list size.")
      
   def test_dataReady(self):
      "dataReady - Returns true if the supplied inbox has data ready for processing."
      t=TComponentAsync()
      #Test default arguments
      self.failIf(t.tc2.dataReady(),"There shouldn't be any data ready before any is sent.")
      t.tc1.send("a")
      t.postoffice.domessagedelivery()
      self.failUnless(t.tc2.dataReady(),"Should be data ready after a send and delivery.")
      t.tc2.recv()
      self.failIf(t.tc2.dataReady(),"There shouldn't be any data ready after this recv.")
      t.tc1.send("b")
      t.tc1.send("c")
      t.postoffice.domessagedelivery()
      t.postoffice.domessagedelivery()
      self.failUnless(t.tc2.dataReady(),"Should be data ready after a send and delivery.")
      t.tc2.recv()
      self.failUnless(t.tc2.dataReady(),"Should still be data ready after a double send and delivery.")
      t.tc2.recv()
      self.failIf(t.tc2.dataReady(),"There shouldn't be any data ready after these recv calls.")
      
      #Test Explicit arguments
      self.failIf(t.tc1.dataReady("control"),"There shouldn't be any data ready before any is sent.")
      t.tc2.send("a","signal")
      t.postoffice.domessagedelivery()
      self.failUnless(t.tc1.dataReady("control"),"Should be data ready after a send and delivery.")
      t.tc1.recv("control")
      self.failIf(t.tc1.dataReady("control"),"There shouldn't be any data ready after this recv.")
      t.tc2.send("b","signal")
      t.tc2.send("c","signal")
      t.postoffice.domessagedelivery()
      t.postoffice.domessagedelivery()
      self.failUnless(t.tc1.dataReady("control"),"Should be data ready after a send and delivery.")
      t.tc1.recv("control")
      self.failUnless(t.tc1.dataReady("control"),"Should still be data ready after a double send and delivery.")
      t.tc1.recv("control")
      self.failIf(t.tc1.dataReady("control"),"There shouldn't be any data ready after these recv calls.")
      
   def test_link(self):
      """link - Creates a link, handled by the component's postman, that links a source component to it's sink, honouring passthrough, pipewidth and synchronous attributes.
      Test is delicate to internal structure of component and linkage, extra default linkages may break test."""
#      properlinkageclass = Linkage.linkage
#      linkage = dummylinkage
      parent = component()
      ac = component()
      bc = component()
      parent.addChildren(ac,bc)
      parent.postoffice=testpostman2()

      parent.link((ac,"outbox"),(bc,"inbox"))
      d = parent.postoffice.linkages[0]#dummylinkage.dummylinkagelist[0]
      self.failUnless(d.source == ac
        and d.sourcebox == "outbox"
        and d.sink == bc
        and d.sinkbox == "inbox"
        and d.showtransit==0
        and d.passthrough==0
        and not d.pipewidth
        and d.synchronous==False, "Problem with link called with mostly default arguments.")
      parent.link((bc,"outbox"),(parent,"outbox"),passthrough=2)
      d = parent.postoffice.linkages[1]
      self.failUnless(d.source == bc
        and d.sourcebox == "outbox"
        and d.sink == parent
        and d.sinkbox == "outbox"
        and d.showtransit==0
        and d.passthrough==2
        and not d.pipewidth
        and d.synchronous==False, "Problem with link called with passthrough arguments.")
      parent.link((ac,"signal"),(bc,"control"),synchronous=True)
      d = parent.postoffice.linkages[2]
      self.failUnless(d.source == ac
        and d.sourcebox == "signal"
        and d.sink == bc
        and d.sinkbox == "control"
        and d.showtransit==0
        and d.passthrough==0
        and d.pipewidth==1
        and d.synchronous==True, "Problem with link called with synchronous True argument.")
      parent.link((bc,"signal"),(ac,"control"),pipewidth=5)
      d = parent.postoffice.linkages[3]
      self.failUnless(d.source == bc
        and d.sourcebox == "signal"
        and d.sink == ac
        and d.sinkbox == "control"
        and d.showtransit==0
        and d.passthrough==0
        and d.pipewidth==5
        and d.synchronous==True, "Problem with link called with pipewidth 5.")

      parent.link((parent,"inbox"),(ac,"inbox"),1,6,True)
      d = parent.postoffice.linkages[4]
      self.failUnless(d.source == parent
        and d.sourcebox == "inbox"
        and d.sink == ac
        and d.sinkbox == "inbox"
        and d.showtransit==0
        and d.passthrough==1
        and d.pipewidth==6
        and d.synchronous==True, "Problem with link called with all arguments set by position not name.")

  #    Linkage.linkage=properlinkageclass

   def test_recv(self):
      "recv - Takes the first item available off the specified inbox, and returns it."
      tcomp = TComponentAsync()
      self.failUnlessRaises(IndexError, tcomp.tc2.recv)#, "Exception should be thrown calling recv on empty box")
      m1 = "inbox1"
      m2 = "inbox2"
      m3 = "control1"
      m4 = "control2"
      tcomp.tc1.send(m1)
      tcomp.postoffice.domessagedelivery()
      tcomp.tc1.send(m2)
      tcomp.postoffice.domessagedelivery()
      self.failUnless(tcomp.tc2.recv()==m1,"Message 1 not received properly")
      self.failUnless(tcomp.tc2.recv()==m2,"Second message not received properly.")
      self.failUnlessRaises(IndexError, tcomp.tc2.recv)#, "Exception should be thrown calling recv on empty box")
      
      self.failUnlessRaises(IndexError, tcomp.tc1.recv,"control")#, "Exception should be thrown calling recv on empty box")
      tcomp.tc2.send(m3,"signal")
      tcomp.postoffice.domessagedelivery()
      tcomp.tc2.send(m4,"signal")
      tcomp.postoffice.domessagedelivery()
      self.failUnless(tcomp.tc1.recv("control")==m3,"Message 1 not received properly with inbox arguments.")
      self.failUnless(tcomp.tc1.recv("control")==m4,"Second message not received properly with inbox arguments.")
      self.failUnlessRaises(IndexError, tcomp.tc1.recv,"control")#, "Exception should be thrown calling recv on empty box")
       
   def test_send(self):
      "send - Takes the message and places it into the specified outbox, throws an exception if there is no space in a  synchronous outbox."
      tcomp=TComponent()
      tcomp.tc1.send("ba")
      self.failUnless(tcomp.tc1.outboxes["outbox"][0]=="ba", "Sent item not put in outbox.")
      self.failUnlessRaises(noSpaceInBox,tcomp.tc1.send,"da")
      tcomp.tc1.send("bing","signal")
      tcomp.tc1.send("boom","signal")
      signalbox = tcomp.tc1.outboxes["signal"]
      self.failUnless(signalbox[0]=="bing" and signalbox[1]=="boom", "Item queue unexpected at send.")
      
      tcomp=TComponentAsync()
      for x in xrange(0,1000):
          tcomp.tc1.send(x)
          self.failUnless(tcomp.tc1.outboxes["outbox"][x]==x, "Failed while sending lots without clearing box.")

   def test_sendforce(self):
      "send - Takes the message and places it into the specified outbox, throws an exception if there is no space in a  synchronous outbox."
      tcomp=TComponent()
      tcomp.tc1.send("ba")
      self.failUnless(tcomp.tc1.outboxes["outbox"][0]=="ba", "Sent item not put in outbox.")
      tcomp.tc1.send("da",force=True)
      tcomp.tc1.send("bing","signal",force=True)
      tcomp.tc1.send("boom","signal",force=True)
      signalbox = tcomp.tc1.outboxes["signal"]
      self.failUnless(signalbox[0]=="bing" and signalbox[1]=="boom", "Item queue unexpected at send.")
      
      tcomp=TComponentAsync()
      for x in xrange(0,1000):
          tcomp.tc1.send(x,force=True)
          self.failUnless(tcomp.tc1.outboxes["outbox"][x]==x, "Failed while sending lots without clearing box.")
          
   def test__collect(self):
      "_collect - Takes the first piece of data in an outbox and returns it. Raises IndexError if empty. Internal function."
      t=component()
      self.failUnlessRaises(IndexError, t._collect)
      t.send("ba")
      t.send("da")
      self.failUnless(t._collect()=="ba")
      self.failUnless(t._collect()=="da")
      self.failUnlessRaises(IndexError, t._collect)
      self.failUnlessRaises(IndexError, t._collect, "signal")
      t.send("ba","signal")
      t.send("da","signal")
      self.failUnless(t._collect("signal")=="ba")
      self.failUnless(t._collect("signal")=="da")
      self.failUnlessRaises(IndexError, t._collect,"signal")
      
   def test__safeCollect(self):
      "_safeCollect - Wrapper around _collect - returns None where an IndexError would normally be thrown. Internall Function."
      t=component()
      self.failUnless(t._safeCollect()==None)
      t.send("ba")
      t.send("da")
      self.failUnless(t._safeCollect()=="ba")
      self.failUnless(t._safeCollect()=="da")
      self.failUnless(t._safeCollect()==None)
      self.failUnless(t._safeCollect("signal")==None)
      t.send("ba","signal")
      t.send("da","signal")
      self.failUnless(t._safeCollect("signal")=="ba")
      self.failUnless(t._safeCollect("signal")=="da")
      self.failUnless(t._safeCollect("signal")==None)
      
   def test__collectInbox_withoutArgsEmptyBox(self):
      """_collectInbox - Tests with default args. Should raise IndexError as the box should be empty in this test. Internal Function."""
      c = component()
      self.failUnlessRaises(IndexError, c._collectInbox)
      c._deliver("ba","inbox")
      c._collectInbox()
      self.failUnlessRaises(IndexError, c._collectInbox)
   
   def test__collectInbox_withArgsEmptyBox(self):
      """_collectInbox - Tests with inbox arg. Should raise IndexError as the box should be empty in this test. Internal Function."""
      c = component()
      self.failUnlessRaises(IndexError, c._collectInbox,"control")
      c._deliver("ba","control")
      c._collectInbox("control")
      self.failUnlessRaises(IndexError, c._collectInbox,"control")
         
   def test__collectInbox_withoutArgs(self):
      """_collectInbox - Tests with default args. All these deliveries should suceed. Internal Function."""
      c = component()
      mes1="ba"
      mes2="da"
      mes3="bing"
      c._deliver(mes1,"inbox")
      c._deliver(mes2,"inbox")
      self.failUnless(c._collectInbox()==mes1, "First not delivered correctly.")
      self.failUnless(c._collectInbox()==mes2, "Second message not delivered correctly.")
      c._deliver(mes3,"inbox")
      self.failUnless(c._collectInbox()==mes3, "Failed to deliver the message after emptying the box and then sending something.")
         
   def test__collectInbox_withArgs(self):
      """_collectInbox - Tests with inbox arg. Tests collection. Internal Function."""
      c = component()
      mes1="ba"
      mes2="da"
      mes3="bing"
      c._deliver(mes1,"control")
      c._deliver(mes2,"control")
      self.failUnless(c._collectInbox("control")==mes1, "First not delivered correctly.")
      self.failUnless(c._collectInbox("control")==mes2, "Second message not delivered correctly.")
      c._deliver(mes3,"control")
      self.failUnless(c._collectInbox("control")==mes3, "Failed to deliver the message after emptying the box and then sending something.")
       
   def test__deliver_smoketest(self):
      "_deliver - Appends the given message to the given inbox. Internal Function."
      c=component()
      try:
          c._deliver("A message.")
          c._deliver("Another message","control",True)
      except:
          self.fail()
      
   def test__deliver_syncronisedBox(self):
       "_deliver - Checks delivery to a synchronised inbox fails when it is full."
       t = TComponent()
       try:
           t.tc2._deliver("ba")
       except:
           self.fail()
       self.failUnlessRaises(noSpaceInBox, t.tc2._deliver, "da","inbox")
       self.failUnlessRaises(noSpaceInBox, t.tc2._deliver, "da")
       self.failUnless(t.tc2._collectInbox("inbox")=="ba", "Different item received from that delivered.  Problem somewhere.")
       try:
           t.tc2._deliver("da")
       except:
           self.fail("Delivery failed unexpectedly.")
       
       try:
           t.tc2._deliver("ba","control")
           t.tc2._deliver("da","control")
           t.tc2._deliver("bing","control")
       except:
           self.fail("Delivery failed unexpectedly to pipewidth 3 inbox.")
       self.failUnlessRaises(noSpaceInBox, t.tc2._deliver, "!","control")
       #Check items were properly inserted into inbox by extracting them.
       self.failUnless(t.tc2.recv("control")=="ba")
       self.failUnless(t.tc2.recv("control")=="da")
       self.failUnless(t.tc2.recv("control")=="bing")
       self.failIf(t.tc2.dataReady("control"), "Confirm that when exception was thrown item was not added.")
       
   def test__deliver_syncronisedBoxforce(self):
       "_deliver - Checks delivery to a synchronised inbox fails when it is full using the force method."
       t = TComponent()
       try:
           t.tc2._deliver("ba")
       except:
           self.fail()
       t.tc2._deliver("da","inbox",True)
       t.tc2._deliver( "bing",force=True)
       self.failUnless(t.tc2._collectInbox("inbox")=="ba", "Different item received from that delivered.  Problem somewhere.")
       self.failUnless(t.tc2._collectInbox("inbox")=="da", "Different item received from that delivered.  Problem somewhere.")
       self.failUnless(t.tc2._collectInbox("inbox")=="bing", "Different item received from that delivered.  Problem somewhere.")
       try:
           t.tc2._deliver("ba","control")
           t.tc2._deliver("da","control")
           t.tc2._deliver("bing","control")
       except:
           self.fail("Delivery failed unexpectedly to pipewidth 3 inbox.")
       t.tc2._deliver("!","control",True)
       #Check items were properly inserted into inbox by extracting them.
       self.failUnless(t.tc2.recv("control")=="ba")
       self.failUnless(t.tc2.recv("control")=="da")
       self.failUnless(t.tc2.recv("control")=="bing")
       self.failUnless(t.tc2.recv("control")=="!")
       
   def test__passThroughDeliverOut_smoketest(self):
      "_passThroughDeliverOut - Appends the given message to the given outbox. Internal Function."
      c=component()
      try:
          c._passThroughDeliverOut("ba")
      except Exception, e:
          self.fail("Exception trying delivery."+str(e))
      self.failUnless(c._collect() == "ba")
      
   def test__passThroughDeliverOut_Sync_DefaultArgs(self):
        "_passThroughDeliverOut_Sync - Appends messages to given outbox.  Should throw noSpaceInBox when full."
        t=TComponent()
        try:
            t.tc1._passThroughDeliverOut("ba")
        except Exception, e:
            self.fail("_passThroughDeliverOut should work to empty outbox")
        self.failUnlessRaises(noSpaceInBox, t.tc1._passThroughDeliverOut, "da")
        self.failUnless(t.tc1._collect("outbox")=="ba", "Default argument passthrough out delivery failed.")
       
   def test__passThroughDeliverOut_Sync(self):
    "_passThroughDeliverOut - Checks delivery is limited to the pipewidth."
    t=TComponent()
    try:
        t.tc1._passThroughDeliverOut("ba","signal")
        t.tc1._passThroughDeliverOut("da","signal")
        t.tc1._passThroughDeliverOut("bing","signal")
    except Exception, e:
        self.fail("Should be room for three items in signal outbox. Exception: " + str(e))
    self.failUnlessRaises(noSpaceInBox, t.tc1._passThroughDeliverOut, "!!!", "signal")
    self.failUnless(t.tc1._collect("signal")=="ba")
    self.failUnless(t.tc1._collect("signal")=="da")
    self.failUnless(t.tc1._collect("signal")=="bing")
    self.failUnlessRaises(IndexError, t.tc1._collect, "signal")

   def test__passThroughDeliverOut_Syncforce(self):
    "_passThroughDeliverOut - Checks delivery is limited to the pipewidth."
    t=TComponent()
    try:
        t.tc1._passThroughDeliverOut("ba","signal")
        t.tc1._passThroughDeliverOut("da","signal")
        t.tc1._passThroughDeliverOut("bing","signal")
    except Exception, e:
        self.fail("Should be room for three items in signal outbox. Exception: " + str(e))
    t.tc1._passThroughDeliverOut("!!!", "signal",True)
    self.failUnless(t.tc1._collect("signal")=="ba")
    self.failUnless(t.tc1._collect("signal")=="da")
    self.failUnless(t.tc1._collect("signal")=="bing")
    self.failUnless(t.tc1._collect("signal")=="!!!")
    
    
   def test__passThroughDeliverIn_smoketest(self):
      "_passThroughDeliverIn - Appends the given message to the given inbox. Internal Function."
      c=component()
      try:
          c._passThroughDeliverIn("ba")
          c._passThroughDeliverIn("da", "inbox")
          c._passThroughDeliverIn("bing","control")
      except Exception, e:
          self.fail()
      self.failUnless(c.recv("inbox")=="ba")
      self.failUnless(c.recv("inbox")=="da")
      self.failUnless(c.recv("control")=="bing")
      
   def test__passThroughDeliverIn_sync(self):
      "_passThroughDeliverIn - Should throw noSpaceInBox if a synchronised box is full."
      t=TComponent()
      try:
          t.tc2._passThroughDeliverIn("ba")
          t.tc2._passThroughDeliverIn("ba","control")
          t.tc2._passThroughDeliverIn("da","control")
          t.tc2._passThroughDeliverIn("bing","control")
      except Exception, e:
          self.fail("Deliveries within pipewidth should suceed.  Exception: " + str(e))
      self.failUnlessRaises(noSpaceInBox, t.tc2._passThroughDeliverIn,"da", "inbox")
      self.failUnlessRaises(noSpaceInBox, t.tc2._passThroughDeliverIn,"!", "control")
      self.failUnless(t.tc2.recv("inbox")=="ba")
      self.failUnless(t.tc2.recv("control")=="ba")
      self.failUnless(t.tc2.recv("control")=="da")
      self.failUnless(t.tc2.recv("control")=="bing")
      self.failIf(t.tc2.dataReady("inbox"))
      self.failIf(t.tc2.dataReady("control"))

   def test__passThroughDeliverIn_syncforce(self):
      "_passThroughDeliverIn - When force is passed as true the box can be overfilled.."
      t=TComponent()
      try:
          t.tc2._passThroughDeliverIn("ba")
          t.tc2._passThroughDeliverIn("ba","control")
          t.tc2._passThroughDeliverIn("da","control")
          t.tc2._passThroughDeliverIn("bing","control")
      except Exception, e:
          self.fail("Deliveries within pipewidth should suceed.  Exception: " + str(e))
      t.tc2._passThroughDeliverIn("da", "inbox",True)
      t.tc2._passThroughDeliverIn("!", "control",True)
      self.failUnless(t.tc2.recv("inbox")=="ba")
      self.failUnless(t.tc2.recv("control")=="ba")
      self.failUnless(t.tc2.recv("control")=="da")
      self.failUnless(t.tc2.recv("control")=="bing")
      self.failUnless(t.tc2.recv("inbox")=="da")
      self.failUnless(t.tc2.recv("control")=="!")
      
   def test_main_smokeTest(self):
      """main - Returns a generator that implements the documented behaviour of a highly simplistic approach component statemachine.
      First value returned is always 1 then the return values are those from the component's main method unitil it returns a False value."""
      t=TestMainLoopComponent()
      m=t.main()
      self.failUnless(m.next()==1)
      for x in xrange(1,1000):
          self.failUnless(m.next()==x, "Failed when x = " + str(x))
      self.failUnless(m.next()==1,"After the main method returns a false value the result of closeDownComponent is returned.  Stub of 1 assumed.")
      self.failUnlessRaises(StopIteration, m.next)#, "Checks the generator has finished.")

   def test_main_closedowntest(self):
      """main - This ensures that the closeDownComponent method is called at the end of the loop.  It also repeats the above test."""
      t=TestMainLoopComponentClosedown()
      m=t.main()
      self.failUnless(m.next()==1)
      for x in xrange(1,1000):
          self.failUnless(m.next()==x, "Failed when x = " + str(x))
      self.failUnlessRaises(closeDownCompTestException , m.next)#Ensures that the closeDownComponent method has been called.
      self.failUnlessRaises(StopIteration, m.next)#, "Checks the generator has finished.")
            
   def test_initialiseComponent(self):
      "initialiseComponent - Stub method, returns 1, expected to be overridden by clients."
      self.failUnless(component().initialiseComponent()==1,"Expected a stub returning 1!")
   def test_mainBody(self):
      "mainBody - stub method, returns None, expected to be overridden by clients as the main loop."
      self.failUnless(component().mainBody()==None, "Stub method.  Expected return value None.")
   def test_closeDownComponent(self):
      "closeDownComponent - stub method, returns 1, expected to be overridden by clients."
      self.failUnless(component().closeDownComponent()==1, "Should be a stub returning 1!")
   def test__closeDownMicroprocess_smoketest(self):
      "_closeDownMicroprocess - Returns a shutdownMicroprocess. Internal Function."
      c = component()
      self.failUnless(isinstance(c._closeDownMicroprocess(),shutdownMicroprocess), "_closeDownComponent should return a shutdownMicroprocess object.")

   def test__closeDownMicroprocess_POcheck(self):
      "_closeDownMicroprocess - Checks the shutdownMicroprocess message for the scheduler contains a reference to the postoffice associated with the component."
      c=component()
      sm=c._closeDownMicroprocess()
      self.failUnless(sm.microprocesses()==(c.postoffice,))

def suite():
   return unittest.makeSuite(Component_Test)
      
if __name__=='__main__':
   try:
     unittest.main()
   except:
     print "Done"
