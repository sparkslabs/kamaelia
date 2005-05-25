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
# Aim: Full coverage testing of the Linkage module
#

# Test the module loads
import unittest
#import sys ; sys.path.append("..")
from Axon.Linkage import *
import Axon.Component
Component = Axon.Component
from Axon.Postman import postman
from Axon.AxonExceptions import ArgumentsClash, noSpaceInBox
#import gc as _gc
import re

class DummyPostman:
   def registerlinkage(self,linkage):
      self.linkage=linkage
      
class TestComponent(Component.component):
   def __init__(self):
      super(TestComponent, self).__init__()
      self.syncboxes=list()
   def _synchronisedBox(self , boxtype="sink",boxdirection="outbox",boxname="outbox", maxdepth=1):
      self.syncboxes.append((boxtype,boxdirection,boxname,maxdepth))

class linkage_Test(unittest.TestCase):
   def setUp(self):
      self.compA = Component.component()
      self.compB = Component.component()
   def test_SmokeTest_NoArguments(self):
      "__init__ - Called with no arguments fails - raises TypeError - must supply source & sink components..."
      self.failUnlessRaises(TypeError, linkage)
   def test_SmokeTest_MinArguments(self):
      "__init__ - Called with source & sink components forms a non-synchronous, non-passthrough linkage between the source component's outbox to the sink component's inbox not registered with any postman..."
      #Some lengths have to be gone to to check that the linkage hasn't found a postman to register with.
      #This line gets the number of postmen from the garbage collector before the linkage is created.
#      numberOfPostmen = len([ str(x) for x in _gc.get_objects() if isinstance(x, postman) ])
      link = linkage(self.compA,self.compB)
      #This line checks that the number of postmen hasn't changed and causes a failure if it has.
#      self.failUnless(numberOfPostmen == len([ str(x) for x in _gc.get_objects() if isinstance(x, postman) ]), "The act of creating a linkage seems to have created or destroyed at least one postman object.  This should not have happened.")
      #The final stage is to check that the linkage hasn't registered itself with either of the components passed to it's postman.
      self.failIf(self.compA.postoffice.islinkageregistered(link), "New linkage has been registered with the source component's postoffice!!!")
      self.failIf(self.compB.postoffice.islinkageregistered(link), "New linkage has been registered with the sink component's postoffice!!!")
      
      self.failUnless(link.source == self.compA, "Source component not correctly set.  Args by position.")
      self.failUnless(link.sink==self.compB,"Sink component not correctly set.  Args by position.")
      self.failUnless(link.sourcebox=="outbox", "Default outbox not used as source.")
      self.failUnless(link.sinkbox=="inbox", "Default inbox not used as inbox.")
      self.failUnless(link.synchronous==False, "Link has not defaulted to asynchronous.")
      self.failUnless(link.passthrough==0, "Link is not set to non-passthrough.")
      self.failUnless(link.showtransit==0, "showTransit is not zero.")

      link2 = linkage(sink=self.compB, source=self.compA)
      self.failUnless(link2.source == self.compA, "Source component not correctly set.  Args by name.")
      self.failUnless(link2.sink==self.compB,"Sink component not correctly set.  Args by name.")

   def test_SmokeTest_SpecificBoxesArguments(self):
      "__init__ - called with both source/sink in/outboxes in addition to min-args forms a linkage between the specified source/sink boxes."
      link=linkage(self.compA, self.compB, "signal", "control")
      self.failUnless(link.source == self.compA, "Source component not correctly set.  Args by position.")
      self.failUnless(link.sink==self.compB,"Sink component not correctly set.  Args by position.")
      self.failUnless(link.sourcebox=="signal", "Sourcebox not set correctly.  Args by position.")
      self.failUnless(link.sinkbox=="control", "Default outbox not used as source.")
      self.failUnless(link.synchronous==False, "Link has not defaulted to asynchronous.")
      self.failUnless(link.passthrough==0, "Link is not set to non-passthrough.")
      self.failUnless(link.showtransit==0, "showTransit is not zero.")
      
      link2=linkage(sink=self.compB, sinkbox="control", source=self.compA, sourcebox="signal")
      self.failUnless(link2.sourcebox=="signal", "sourcebox not set correctly by name.")
      self.failUnless(link2.sinkbox=="control", "sinkbox not set correctly by name.")

   def test_SmokeTest_defaultPassthrough(self):
      "__init__ - called with passthrough set to 0 results in a standard non-passthrough outbox to inbox linkage."
      link=linkage(self.compA, self.compB, "outbox", "inbox",passthrough=0)
      self.failUnless(link.passthrough==0, "Link is not set to non-passthrough.  Was set explicitly")
   def test_SmokeTest_inboxPassthrough(self):
      "__init__ - called with passthrough set to 1 means the source and sink boxes are both inboxes. This means the linkage is passthrough-inbound (normally from the inbox of a wrapper component to the inbox of a worker/sub-component)."
      link=linkage(self.compA, self.compB, "inbox", "inbox",passthrough=1)
      self.failUnless(link.passthrough==1, "Link is not set to inbox passthrough.  Was set explicitly by name.")
      link2=linkage(self.compA, self.compB, "inbox", "inbox",None,1)
      self.failUnless(link.passthrough==1, "Link is not set to inbox passthrough.  Was set explicitly by position.")
   def test_SmokeTest_outboxPassthrough(self):
      "__init__ - called with passthrough set to 2 means the source and sink boxes are both outboxes. This means the linkage is passthrough-outbound (normally from the outbox of a worker/sub-component to the outbox of a wrapper component ). ttbw"
      link=linkage(self.compA, self.compB, "outbox", "outbox",passthrough=2)
      self.failUnless(link.passthrough==2, "Link is not set to inbox passthrough.  Was set explicitly by name.")
   def test_SmokeTest_postofficeDefined(self):
      "__init__ - When created with a defined postoffice/postman, the linkage registers itself with that postman."
      dp=DummyPostman()
      link=linkage(self.compA, self.compB, "outbox","inbox",dp)
      self.failUnless(dp.linkage is link, "Linkage not registered with postman!!!  Postman set by position.")
      dp2=DummyPostman()
      link2=linkage(postoffice=dp2, sink=self.compB, source=self.compA)
      self.failUnless(dp2.linkage is link2, "Linkage not registered with postman!!!  Postman set by name.")
##~    def test_SmokeTest_showTransitDefined(self):
##~       "__init__ - If a showTransit flag is provided, this gets stored to change behaviour during message movement. ttbw"
##~       #link=linkage(self.compA,self.compB,"outbox","inbox",None,
##~       pass
   def test_SmokeTest_pipewidthDefined(self):
      "__init__ - Providing a pipewidth automatically changes the source/sink boxes to being synchronised - with a maximum number of items in transit. (Clearly just stored by the object during initialisation). ttbw"
      link=linkage(self.compA, self.compB, "outbox", "inbox",pipewidth=2)
      self.failUnless(link.pipewidth==2, "Link is not set to pipewidth 2.  Was set explicitly by name.")
      self.failUnless(link.synchronous==True, "Setting pipewidth should set link to synchronous automatically.")
      
      link2=linkage(self.compA, self.compB, "outbox", "inbox",None,0,5)
      self.failUnless(link2.pipewidth==5, "Link is not set to pipewidth 5.  Was set explicitly by position.")
      self.failUnless(link2.synchronous==True, "Setting pipewidth should set link to synchronous automatically.")
   def test_SmokeTest_pipewidthDefinedNotSynchronous(self):
      "__init__ - Providing a pipewidth and synchronous flag set to false is an error. Raises an exception."
      self.failUnlessRaises(ArgumentsClash, linkage,self.compA,self.compB,pipewidth=5,synchronous=False)
   def test_SmokeTest_synchronousDefined(self):
      "__init__ - The synchronous flag is stored to note whether the linkage limits deliveries based on whether the recipient (sink) box has space to recieve data. Source & Sink boxes are changed to be synchronous if they were not originally defined to be so. ttbw"
      link=linkage(self.compA, self.compB, "outbox", "inbox",synchronous=True)
      self.failUnless(link.pipewidth==1, "Link is not set to pipewidth 1.  Should occur when set synchronised.")
      self.failUnless(link.synchronous==True, "Syncronuous set explictly to True failed.")
      
      link2=linkage(self.compA, self.compB, "outbox", "inbox",None,0,5,True)
      self.failUnless(link2.pipewidth==5, "Link is not set to pipewidth 5.  Was set explicitly by position.")
      self.failUnless(link2.synchronous==True, "synchronous set explicitly to True should suceed even when the pipewidth is explicit.")
      
   def test_setShowTransit(self):
      "setShowtransit - Provides a mechanism for adjusting the debuging options of the linkage so that traffic can be monitored."
      link=linkage(self.compA,self.compB)
      link.setShowTransit(5)
      self.failUnless(link.showtransit==5,"showtransit not set correctly.")
      link.setShowTransit(1)
      self.failUnless(link.showtransit==1,"showtransit not set correctly.")
      link.setShowTransit(0)
      self.failUnless(link.showtransit==0, "showtransit not set correctly.")
      
   def test_setSynchronous_noArg(self):
      "setSynchronous - Makes a linkage synchronous with its current pipewidth, will default to 1. Calls _synchronisedBox on each component so that the boxes are setup correctly."
      tc1=TestComponent()
      tc2=TestComponent()
      link=linkage(tc1,tc2)
      link.setSynchronous()
      self.failUnless(link.synchronous == True, "Has not set link as synchronous.")
      self.failUnless(link.pipewidth == 1, "Pipewidth has not defaulted to 1.")
      self.failUnless(tc1.syncboxes[0] == ("source","outbox","outbox",1))
      self.failUnless(tc2.syncboxes[0] == ("sink","inbox","inbox",1))
      
      link2=linkage(tc1,tc2,sourcebox="control",sinkbox="control",passthrough=1)
      link2.setSynchronous()
      self.failUnless(link2.synchronous == True, "Has not set link as synchronous.")
      self.failUnless(link2.pipewidth == 1, "Pipewidth has not defaulted to 1.")
      self.failUnless(tc1.syncboxes[1] == ("source","inbox","control",1))
      self.failUnless(tc2.syncboxes[1] == ("sink","inbox","control",1))
 
      link3=linkage(tc1,tc2,sourcebox="signal",sinkbox="signal",passthrough=2)
      link3.pipewidth=9 #Checks that the pipewidth gets used if set.
      link3.setSynchronous()
      self.failUnless(link3.synchronous == True, "Has not set link as synchronous.")
      self.failUnless(link3.pipewidth == 9, "Pipewidth has not defaulted to 1.")
      self.failUnless(tc1.syncboxes[2] == ("source","outbox","signal",9))
      self.failUnless(tc2.syncboxes[2] == ("sink","outbox","signal",9))

   def test_setSynchronous_withWidthArg(self):
      "setSynchronous - Makes a linkage synchronous with its the argument as the pipewidth."
      tc1=TestComponent()
      tc2=TestComponent()
      link=linkage(tc1,tc2)
      link.setSynchronous(5)
      self.failUnless(link.synchronous == True, "Has not set link as synchronous.")
      self.failUnless(link.pipewidth == 5, "Pipewidth has not defaulted to 1.")
      self.failUnless(tc1.syncboxes[0] == ("source","outbox","outbox",5))
      self.failUnless(tc2.syncboxes[0] == ("sink","inbox","inbox",5))
      
      link2=linkage(tc1,tc2,sourcebox="control",sinkbox="control",passthrough=1)
      link2.setSynchronous(2)
      self.failUnless(link2.synchronous == True, "Has not set link as synchronous.")
      self.failUnless(link2.pipewidth == 2, "Pipewidth has not defaulted to 1.")
      self.failUnless(tc1.syncboxes[1] == ("source","inbox","control",2))
      self.failUnless(tc2.syncboxes[1] == ("sink","inbox","control",2))

      link3=linkage(tc1,tc2,sourcebox="signal",sinkbox="signal",passthrough=2)
      link3.setSynchronous(6)
      self.failUnless(link3.synchronous == True, "Has not set link as synchronous.")
      self.failUnless(link3.pipewidth == 6, "Pipewidth has not defaulted to 1.")
      self.failUnless(tc1.syncboxes[2] == ("source","outbox","signal",6))
      self.failUnless(tc2.syncboxes[2] == ("sink","outbox","signal",6))

   def test_sourcePair(self):
      link = linkage(source=self.compA,sink=self.compB, sourcebox="outbox",sinkbox="inbox")
      self.failUnless(link.sourcePair()==(self.compA,"outbox"))
      link2 = linkage(source=self.compB,sink=self.compA, sourcebox="signal",sinkbox="control")
      self.failUnless(link2.sourcePair()==(self.compB,"signal"))

   def test_sourcePair(self):
      link = linkage(source=self.compA,sink=self.compB, sourcebox="outbox",sinkbox="inbox")
      self.failUnless(link.sinkPair()==(self.compB,"inbox"))
      link2 = linkage(source=self.compB,sink=self.compA, sourcebox="signal",sinkbox="control")
      self.failUnless(link2.sinkPair()==(self.compA,"control"))
   
   def test_setShowTransit(self):
      link=linkage(source=self.compA,sink=self.compB, sourcebox="outbox",sinkbox="inbox")
      self.failUnless(link.showtransit==0)
      link.setShowTransit(5)
      self.failUnless(link.showtransit==5)
      link.setShowTransit(0)
      self.failUnless(link.showtransit==0)

   def test___str__strict(self):
      "__str__ - Returns a string that indicates the link source and sink components and boxes.  Precise formatting is checked."
      link=linkage(self.compA, self.compB, "signal", "control",postoffice=self.compA.postoffice)
      stricttest = "Link\( source:\["+self.compA.name+",signal\], sink:\["+self.compB.name+",control\] \)"
      self.failUnless(re.match(stricttest,str(link)),"Strict match failed with expected string.  Any format change will have broken this.\nGot:\n"+str(link)+"\nExpected\n"+stricttest+"\n\n")
      
   def test_dataToMove_pass0(self):
      "dataToMove - Checks whether the source outbox has any data available on it.  This works on normal linkages."
      link=linkage(source=self.compA,sink=self.compB, sourcebox="signal",sinkbox="control")
      self.failIf(link.dataToMove())
      self.compA.send("blah","signal")
      self.failUnless(link.dataToMove())
      self.compA._collect("signal")
      self.failIf(link.dataToMove())
      
   def test_dataToMove_pass1(self):
      "dataToMove - Checks whether the source has any data available on it that needs moving to the sink.  Passthrough inbox->inbox test."
      link=linkage(source=self.compA,sink=self.compB, sourcebox="control",sinkbox="inbox",passthrough=1)
      self.failIf(link.dataToMove())
      self.compA._deliver("blah","control")
      self.failUnless(link.dataToMove())
      self.compA._collectInbox("control")
      self.failIf(link.dataToMove())
      
   def test_dataToMove_pass2(self):
      "dataToMove - Checks whether the source has any data available on it that needs moving to the sink."
      link=linkage(source=self.compA,sink=self.compB, sourcebox="signal",sinkbox="outbox",passthrough=2)
      self.failIf(link.dataToMove())
      self.compA.send("blah","signal")
      self.failUnless(link.dataToMove())
      self.compA._collect("signal")
      self.failIf(link.dataToMove())
      
   def test_moveData_pass0(self):
      "moveData - Moves data from source to sink.  One item is moved if there is room in the sink box.  IndexError is thrown if source box is empty so check with dataToMove before calling unless you know there is an item available."
      link=linkage(source=self.compA,sink=self.compB, sourcebox="signal",sinkbox="control")
      self.failUnlessRaises(IndexError, link.moveData)
      self.compA.send("ba","signal")
      self.compA.send("da","signal")
      link.moveData()
      self.failUnless(self.compB.recv("control")=="ba")
      self.failIf(self.compB.dataReady("control"))
      link.moveData()
      self.failUnless(self.compB.recv("control")=="da")
      self.failUnlessRaises(IndexError, link.moveData)
      
   def test_moveData_pass1(self):
      "moveData - Moves data from source to sink.  One item is moved if there is room in the sink box.  IndexError is thrown if source box is empty so check with dataToMove before calling unless you know there is an item available."
      link=linkage(source=self.compA,sink=self.compB, sourcebox="control",sinkbox="inbox",passthrough=1)
      self.failUnlessRaises(IndexError, link.moveData)
      self.compA._deliver("ba","control")
      self.compA._deliver("da","control")
      link.moveData()
      self.failUnless(self.compB.recv("inbox")=="ba")
      self.failIf(self.compB.dataReady("inbox"))
      link.moveData()
      self.failUnless(self.compB.recv("inbox")=="da")
      self.failUnlessRaises(IndexError, link.moveData)
      
   def test_moveData_pass2(self):
      "moveData - "
      link=linkage(source=self.compA,sink=self.compB, sourcebox="signal",sinkbox="outbox",passthrough=2)
      self.failUnlessRaises(IndexError, link.moveData)
      self.compA.send("ba","signal")
      self.compA.send("da","signal")
      link.moveData()
      self.failUnless(self.compB._collect("outbox")=="ba")
      link.moveData()
      self.failUnless(self.compB._collect("outbox")=="da")
      self.failUnlessRaises(IndexError, link.moveData)

#synchronous
   def test_moveData_pass0sync(self):
      "moveData - Moves data from source to sink.  One item is moved if there is room in the sink box.  noSpaceInBox is thrown if source box is full."
      link=linkage(source=self.compA,sink=self.compB, sourcebox="signal",sinkbox="control",pipewidth=1)
      self.compA.send("ba","signal")
      self.failUnlessRaises(noSpaceInBox, self.compA.send,"da","signal")
      link.moveData()
      self.compA.send("da","signal")
      link.moveData() # Should do nothing as sink is full
      self.failUnless(self.compB.recv("control")=="ba")
      self.failIf(self.compB.dataReady())
      self.failUnlessRaises(noSpaceInBox, self.compA.send,"bing","signal")
      link.moveData()
      self.failUnless(self.compB.recv("control")=="da")
      
   def test_moveData_pass1sync(self):
      "moveData - Moves data from source to sink.  One item is moved if there is room in the sink box.  noSpaceInBox is thrown if _deliver is called and source box is full."
      link=linkage(source=self.compA,sink=self.compB, sourcebox="control",sinkbox="inbox",passthrough=1,pipewidth=1)
      self.compA._deliver("ba","control")
      self.failUnlessRaises(noSpaceInBox, self.compA._deliver, "da", "control")
      link.moveData()
      self.compA._deliver("da", "control")
      link.moveData() # Should do nothing as sink is full
      self.failUnless(self.compB.recv("inbox")=="ba")
      self.failIf(self.compB.dataReady("inbox"))
      link.moveData()
      self.failUnless(self.compB.recv("inbox")=="da")
      
   def test_moveData_pass2sync(self):
      "moveData - "
      link=linkage(source=self.compA,sink=self.compB, sourcebox="signal",sinkbox="outbox",passthrough=2,pipewidth=1)
      self.compA.send("ba","signal")
      self.failUnlessRaises(noSpaceInBox, self.compA.send, "da","signal")
      link.moveData()
      self.compA.send("da","signal")
      link.moveData() # Should do nothing as sink is full
      self.failUnless(self.compB._collect("outbox")=="ba")
      self.failIf(len(self.compB.outboxes["outbox"])) # Check outbox is empty
      link.moveData()
      self.failUnless(self.compB._collect("outbox")=="da")

      # Also need a force version.
   def test_moveData_pass0syncforce(self):
      "moveData - Moves data from source to sink.  Forces move despite pipewidth."
      link=linkage(source=self.compA,sink=self.compB, sourcebox="signal",sinkbox="control",pipewidth=1)
      self.compA.send("ba","signal")
      self.failUnlessRaises(noSpaceInBox, self.compA.send,"da","signal")
      link.moveData()
      self.compA.send("da","signal")
      link.moveData(True) 
      self.failUnless(self.compB.recv("control")=="ba")
      self.failUnless(self.compB.recv("control")=="da")
      
   def test_moveData_pass1syncforce(self):
      "moveData - Moves data from source to sink.  Forces despite full pipe."
      link=linkage(source=self.compA,sink=self.compB, sourcebox="control",sinkbox="inbox",passthrough=1,pipewidth=1)
      self.compA._deliver("ba","control")
      self.failUnlessRaises(noSpaceInBox, self.compA._deliver, "da", "control")
      link.moveData()
      self.compA._deliver("da", "control")
      link.moveData(True) 
      self.failUnless(self.compB.recv("inbox")=="ba")
      self.failUnless(self.compB.recv("inbox")=="da")
      
   def test_moveData_pass2syncforce(self):
      "moveData - "
      link=linkage(source=self.compA,sink=self.compB, sourcebox="signal",sinkbox="outbox",passthrough=2,pipewidth=1)
      self.compA.send("ba","signal")
      self.failUnlessRaises(noSpaceInBox, self.compA.send, "da","signal")
      link.moveData()
      self.compA.send("da","signal")
      link.moveData(True)
      self.failUnless(self.compB._collect("outbox")=="ba")
      self.failUnless(self.compB._collect("outbox")=="da")
      
def suite():
   #This returns a TestSuite made from the tests in the linkage_Test class.  It is required for eric3's unittest tool.
   return unittest.makeSuite(linkage_Test)
      
if __name__=='__main__':
   suite()
   try:
     unittest.main()
   except:
     print "Done"
