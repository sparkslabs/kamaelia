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
#
# Aim: Full coverage testing of the Component class
#

# Test the module loads
import unittest
import re
import sys ; sys.path.append(".") ; sys.path.append("..")
from Component import *
import Linkage
#from Scheduler 
class TComponent(component):
    def __init__(self):
        self.__super.__init__()
        self.tc1=component()
        self.tc2=component()
        self.link(source=(self.tc1,"outbox"),sink=(self.tc2,"inbox"))
        self.link(source=(self.tc1,"signal"),sink=(self.tc2,"control"))

TComponentAsync = TComponent

class TestMainLoopComponent(component):
    def __init__(self):
        self.__super.__init__()
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
        
        
class testpostoffice:
    def __init__(self):
        self.linksmade = []
        self.linksremoved = []
    def link(self, source, sink, passthrough=0):
        linkage = (source, sink, passthrough)
        self.linksmade.append(linkage)
        return linkage
    def unlink(self, thecomponent=None, thelinkage=None):
        self.linksremoved.append( (thecomponent,thelinkage) )

        
        

class testpostoffice2(postoffice):
    def istestpostoffice2(self):
        return True

class Component_Test(unittest.TestCase):
   def test_SmokeTest_NoArguments(self):
      "__init__ - Class constructor is expected to be called without arguments."
      testcomponent = component()
      self.failUnless(isinstance(testcomponent,microprocess), "Component should be a Microprocess")
      self.failUnless(testcomponent.Usescomponents==[],"Basic component should not depend on other components")
      self.failUnless(testcomponent.Inboxes.keys().count("inbox")==1,"There should be one 'inbox' in the Inboxes structure.")
      self.failUnless(testcomponent.Inboxes.keys().count("control")==1,"There should be one 'control' in the Inboxes structure.")
      self.failUnless(testcomponent.Outboxes.keys().count("outbox")==1,"There should be one 'outbox' in the Outboxes structure.")
      self.failUnless(testcomponent.Outboxes.keys().count("signal")==1,"There should be one 'signal' in the Outboxes structure.")
      for x in testcomponent.Inboxes:
        self.failUnless(len(testcomponent.inboxes[x])==0,"Unexpected inbox data structure for "+x+".")
      for x in testcomponent.Outboxes:
        self.failUnless(len(testcomponent.outboxes[x])==0,"Unexpected outbox data structure for "+x+".")
      self.failUnless(testcomponent.children==[], "The children component should be an empty list.")

   def test___str__strict(self):
      "__str__ - Returns a string representation of the component- consisting of Component,representation of inboxes, representation of outboxes."
      #First test against an expected string.  Strict test, may have to change.
      t = TComponent()
#      t.send("fish")
#      t.send("chips","signal")
      stricttest = "Component (\S*\.)+TComponent_\d+ \[ inboxes : \{'control'\: <[^>]+>, 'inbox': <[^>]+>\} outboxes : \{'outbox': <[^>]+>, 'signal': <[^>]+>\}"
      self.failUnless(re.match(stricttest,str(t)),"Strict match failed with expected string.  Any format change will have broken this.\n\n"+str(t)+"\n\n")
   
   def test___str__relaxed(self):
      "__str__ - Returns a string that contains the fact that it is a component object and the name of it."
      #Test for vital details.  Not strict shouldn't be broken
      t = TComponent()
#      t.send("fish")
#      t.send("chips","signal")
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
      This involves adding them to the list childred"""
      parent=component()
      child1=component()
      child2=component()
      parent.addChildren(child1,child2)
      self.failUnless(parent.children.count(child1)==1,"Component not added to children list.")
      self.failUnless(parent.children.count(child2)==1,"Component not added to children list.")
      countitems = 0
      for x in parent.children:
        countitems = 1+countitems
      self.failUnless(countitems==2,"Children list has unexpected contents.")
      
   def test_removeChild(self):
      "removeChild - Removes the specified component from the set of child components and deregisters it from the postoffice."
      parent=component()
      parent.postoffice=testpostoffice()
      child=component()
      parent.addChildren(child)
      parent.removeChild(child)
      self.failUnless(parent.children.count(child)==0,"Child not removed from children list.")
      self.failUnless(parent.postoffice.linksremoved == [(child,None)],"Postoffice not informed of child's removal.")
      
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
      self.failUnless(t.tc2.dataReady(),"Should be data ready after a send.")
      t.tc2.recv()
      self.failIf(t.tc2.dataReady(),"There shouldn't be any data ready after this recv.")
      t.tc1.send("b")
      t.tc1.send("c")
      self.failUnless(t.tc2.dataReady(),"Should be data ready after a send.")
      t.tc2.recv()
      self.failUnless(t.tc2.dataReady(),"Should still be data ready after a double send.")
      t.tc2.recv()
      self.failIf(t.tc2.dataReady(),"There shouldn't be any data ready after these recv calls.")
      
      #Test Explicit arguments
      self.failIf(t.tc2.dataReady("control"),"There shouldn't be any data ready before any is sent.")
      t.tc1.send("a","signal")
      self.failUnless(t.tc2.dataReady("control"),"Should be data ready after a send.")
      t.tc2.recv("control")
      self.failIf(t.tc2.dataReady("control"),"There shouldn't be any data ready after this recv.")
      t.tc1.send("b","signal")
      t.tc1.send("c","signal")
      self.failUnless(t.tc2.dataReady("control"),"Should be data ready after a send.")
      t.tc2.recv("control")
      self.failUnless(t.tc2.dataReady("control"),"Should still be data ready after a double send.")
      t.tc2.recv("control")
      self.failIf(t.tc2.dataReady("control"),"There shouldn't be any data ready after these recv calls.")
      
   def test_link(self):
      """link - Creates a link, handled by the component's postoffice, that links a source component to it's sink, honouring passthrough, pipewidth and synchronous attributes.
      Test is delicate to internal structure of component and linkage, extra default linkages may break test."""
      parent = component()
      ac = component()
      bc = component()
      parent.addChildren(ac,bc)
      parent.postoffice=testpostoffice2()

      parent.link((ac,"outbox"),(bc,"inbox"))
      d = parent.postoffice.linkages[0]#dummylinkage.dummylinkagelist[0]
      self.failUnless(d.source == ac
        and d.sourcebox == "outbox"
        and d.sink == bc
        and d.sinkbox == "inbox"
        and d.passthrough==0, "Problem with link called with mostly default arguments.")
      parent.link((bc,"outbox"),(parent,"outbox"),passthrough=2)
      d = parent.postoffice.linkages[1]
      self.failUnless(d.source == bc
        and d.sourcebox == "outbox"
        and d.sink == parent
        and d.sinkbox == "outbox"
        and d.passthrough==2, "Problem with link called with passthrough arguments.")

      parent.link((parent,"inbox"),(ac,"inbox"),1)
      d = parent.postoffice.linkages[2]
      self.failUnless(d.source == parent
        and d.sourcebox == "inbox"
        and d.sink == ac
        and d.sinkbox == "inbox"
        and d.passthrough==1, "Problem with link called with all arguments set by position not name.")

   def test_recv(self):
      "recv - Takes the first item available off the specified inbox, and returns it."
      tcomp = TComponentAsync()
      self.failUnlessRaises(IndexError, tcomp.tc2.recv)#, "Exception should be thrown calling recv on empty box")
      m1 = "inbox1"
      m2 = "inbox2"
      m3 = "control1"
      m4 = "control2"
      tcomp.tc1.send(m1)
      tcomp.tc1.send(m2)
      self.failUnless(tcomp.tc2.recv()==m1,"Message 1 not received properly")
      self.failUnless(tcomp.tc2.recv()==m2,"Second message not received properly.")
      self.failUnlessRaises(IndexError, tcomp.tc2.recv)#, "Exception should be thrown calling recv on empty box")
      
      self.failUnlessRaises(IndexError, tcomp.tc2.recv,"inbox")#, "Exception should be thrown calling recv on empty box")
      tcomp.tc1.send(m3,"signal")
      tcomp.tc1.send(m4,"signal")
      self.failUnless(tcomp.tc2.recv("control")==m3,"Message 1 not received properly with inbox arguments.")
      self.failUnless(tcomp.tc2.recv("control")==m4,"Second message not received properly with inbox arguments.")
      self.failUnlessRaises(IndexError, tcomp.tc2.recv,"control")#, "Exception should be thrown calling recv on empty box")
       
   def test_send(self):
      "send - Takes the message and places it into the specified outbox."
      tcomp=TComponentAsync()
      tcomp.tc1.send("ba")
      self.failUnless(tcomp.tc1.outboxes["outbox"].pop(0)=="ba", "Sent item not put in outbox.")
      tcomp.tc1.send("bing","signal")
      tcomp.tc1.send("boom","signal")
      signalbox = tcomp.tc1.outboxes["signal"]
      self.failUnless(signalbox.pop(0)=="bing", "Items arrived out of order")
      self.failUnless(signalbox.pop(0)=="boom", "Items arrived out of order")
      
      for x in xrange(0,1000):
          tcomp.tc1.send(x)
          self.failUnless(tcomp.tc1.outboxes["outbox"].pop(0)==x, "Failed while sending lots without clearing box.")

#   def test_passthrough_       
      
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
      self.failUnless(c._closeDownMicroprocess()==None, "_closeDownComponent should return None.")

   def test__closeDownMicroprocess_None(self):
      "_closeDownMicroprocess - Checks the message returned is None (no knockons)."
      c=component()
      sm=c._closeDownMicroprocess()
      self.failUnless(sm == None)

def suite():
   return unittest.makeSuite(Component_Test)
      
if __name__=='__main__':
   unittest.main()
