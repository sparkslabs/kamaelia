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
# Full coverage testing of the NullPayloadRTP module. -- INCOMPLETE - work in progress
#
# INCOMPLETE - work in progress
# Test the module loads
import unittest
import Kamaelia.NullPayloadRTP 
import Kamaelia.Util.Comparator
from Kamaelia.Util.TestResultComponent import testResultComponent, StopSystemException
import Kamaelia.Util.Chargen
import Kamaelia.Util.Splitter
import Axon.Component
from Axon.util import testInterface
from Axon.Scheduler import scheduler

from Kamaelia.NullPayloadRTPDecode import nullPayloadRTPDecode
# INCOMPLETE - work in progress
class NullPayloadRTPDecodeTest1(unittest.TestCase):
    def test_smoketest1(self):
        """__init__ - Basic creation test."""
        self.failUnless(nullPayloadRTPDecode())
        
    def test_smoketest2(self):
        """__init__ - Checks the created component has the correct inboxes and outboxes ("inA", "inB", "control", "outbox" and "signal")."""
        self.failUnless(testInterface(nullPayloadRTPDecode(),(["inbox","control"],["outbox", "signal"])))

class TestFrame(Axon.Component.component):
    def __init__(self):
        super(TestFrame,self).__init__()
        self.src = Kamaelia.Util.Chargen.Chargen()
        self.src.activate()
        self.split = Kamaelia.Util.Splitter.Splitter()
        self.comp= Kamaelia.Util.Comparator.comparator()
        self.comp.activate()
        self.testres = testResultComponent()
        self.pack = Kamaelia.NullPayloadRTP.NullPayloadPreFramer("TestSource")
        self.pack.activate()
        self.depack = Kamaelia.NullPayloadRTPDecode.nullPayloadRTPDecode()
        self.depack.activate()
        self.split.createsink(self.pack,"recvsrc")
        self.split.createsink(self.comp, "inB")
        self.link((self.src,"outbox"),(self.split, "inbox"))
        self.link((self.pack,"output"), (self.depack,"inbox"))
        self.link((self.depack,"outbox"), (self.comp, "inA"))
        self.link((self.comp, "outbox"), (self.testres, "inbox"))

class NullPayloadRTPDecodeTest2(unittest.TestCase):
    def setUp(self):
        self.tf = TestFrame()
        self.tf.activate()
        
    def test__selfcheck(self):
        "This test checks that the setUp method of this testcase hasn't failed.  Make this work first."
        pass
        
    def test__runtest(self):
        self.failUnlessRaises(StopSystemException, scheduler.run.runThreads)
        
        
def suite():
   #This returns a TestSuite made from the tests in the linkage_Test class.  It is required for eric3's unittest tool.
   suite = unittest.TestSuite((NullPayloadRTPDecodeTest1,))
   #suite = unittest.makeSuite(Comparator_test2)
#   suite.addTest(Comparator_test1)
#   suite.addTest(Comparator_test2)
   return suite
      
if __name__=='__main__':
   suite()
   unittest.main()
