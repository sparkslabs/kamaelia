#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
#
# Aim: Full coverage testing of the Linkage module
#

# Test the module loads
import unittest
from Axon.Linkage import *
import Axon.Component as Component
#from Postman import postman
from Axon.AxonExceptions import ArgumentsClash, noSpaceInBox
import gc as _gc
import re

class DummyPostman:
   def registerlinkage(self,linkage):
      self.linkage=linkage
      
class TestComponent(Component.component):
   def __init__(self):
      self.__super.__init__()
      self.syncboxes=list()

class linkage_Test(unittest.TestCase):
   def setUp(self):
      self.compA = Component.component()
      self.compB = Component.component()
   def test_SmokeTest_NoArguments(self):
      "__init__ - Called with no arguments fails - raises TypeError - must supply source & sink components..."
      self.failUnlessRaises(TypeError, linkage)
   def test_SmokeTest_MinArguments(self):
      "__init__ - Called with source & sink components forms a non-synchronous, non-passthrough linkage between the source component's outbox to the sink component's inbox"
      link = linkage(self.compA,self.compB)
      
      self.failUnless(link.source == self.compA, "Source component not correctly set.  Args by position.")
      self.failUnless(link.sink==self.compB,"Sink component not correctly set.  Args by position.")
      self.failUnless(link.sourcebox=="outbox", "Default outbox not used as source.")
      self.failUnless(link.sinkbox=="inbox", "Default inbox not used as inbox.")
      self.failUnless(link.passthrough==0, "Link is not set to non-passthrough.")

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
      self.failUnless(link.passthrough==0, "Link is not set to non-passthrough.")
      
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
      link2=linkage(self.compA, self.compB, "inbox", "inbox",1)
      self.failUnless(link.passthrough==1, "Link is not set to inbox passthrough.  Was set explicitly by position.")
   def test_SmokeTest_outboxPassthrough(self):
      "__init__ - called with passthrough set to 2 means the source and sink boxes are both outboxes. This means the linkage is passthrough-outbound (normally from the outbox of a worker/sub-component to the outbox of a wrapper component ). ttbw"
      link=linkage(self.compA, self.compB, "outbox", "outbox",passthrough=2)
      self.failUnless(link.passthrough==2, "Link is not set to inbox passthrough.  Was set explicitly by name.")
   
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
   
   def test___str__strict(self):
      "__str__ - Returns a string that indicates the link source and sink components and boxes.  Precise formatting is checked."
      link=linkage(self.compA, self.compB, "signal", "control")
      stricttest = "Link\( source:\["+self.compA.name+",signal\], sink:\["+self.compB.name+",control\] \)"
      self.failUnless(re.match(stricttest,str(link)),"Strict match failed with expected string.  Any format change will have broken this.\nGot:\n"+str(link)+"\nExpected\n"+stricttest+"\n\n")
      
      
def suite():
   #This returns a TestSuite made from the tests in the linkage_Test class.  It is required for eric3's unittest tool.
   return unittest.makeSuite(linkage_Test)
      
if __name__=='__main__':
   suite()
   unittest.main()
