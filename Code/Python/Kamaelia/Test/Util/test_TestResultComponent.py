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
from Kamaelia.Util.TestResultComponent import testResultComponent, StopSystem, StopSystemException
from Axon.Component import component
from Axon.Linkage import linkage
from Axon.Postman import postman
from Axon.util import testInterface
from Axon.Scheduler import scheduler

class testResultComponent_test1(unittest.TestCase):
    def test_smoketest1(self):
        "__init__ - Object creation no arguments."
        self.failUnless(testResultComponent())
    
    def test_smoketest2(self):
        """__init__ - Checks the created component has the correct inboxes and outboxes ("inbox", "control", "outbox")."""
        self.failUnless(testInterface(testResultComponent(),(["inbox","control"],[])))
    
class testResultComponent_test2(unittest.TestCase):
    def setUp(self):
        self.tester = component()
        self.trcomp = testResultComponent()
        self.trcomp.activate()
        self.pm = postman()
        self.pm.activate()
        self.tester.activate()
        #pipewidth = 1 implies 2 items in the linkage.  One in outbox and one in sourcebox.  Need to change this code if these semantics change.
        self.pm.registerlinkage(linkage(source = self.tester, sink = self.trcomp, sourcebox = "outbox", sinkbox = "inbox"))
        self.pm.registerlinkage(linkage(source = self.tester, sink = self.trcomp, sourcebox = "signal", sinkbox = "control"))

    def runtestsystem(self):
        for i in xrange(5):
            self.trcomp.next()
            self.pm.domessagedelivery()
        
    def test_trueInput1(self):
        "mainBody - Checks that system keeps running when true value messages are sent to the inbox"
        self.tester.send(1)
        self.runtestsystem()
        
    def test_falseInput1(self):
        "mainBody - Checks that an AssertionError is raised when a false value message is sent to the inbox."
        self.tester.send(0)
        self.failUnlessRaises(AssertionError, self.runtestsystem)
        
    def test_trueInput2(self):
        "mainBody - Checks that system keeps running when true value messages are sent to the inbox. Repeated test."
        for i in xrange(1,100):
            self.tester.send(i)
            self.runtestsystem()

    def test_falseInput2(self):
        "mainBody - Checks that an AssertionError is raised when false value messages are sent to the inbox after a series of true ones. Repeated test."
        for i in xrange(1,100):
            self.tester.send(i)
            self.runtestsystem()
        self.tester.send(False)
        self.failUnlessRaises(AssertionError, self.runtestsystem)
        
    def test_stopSystem1(self):
        "mainBody - Checks that a StopSystem message sent to the control causes StopSystemException."
        self.tester.send(StopSystem(), "signal")
        self.failUnlessRaises(StopSystemException, self.runtestsystem)
    
    def test_stopSystem2(self):
        "mainBody - Checks that a StopSystem message sent to the control causes StopSystemException and that this stops the scheduler."
        self.tester.send(StopSystem(), "signal")
        self.failUnlessRaises(StopSystemException, scheduler.run.runThreads)
    
def suite():
   #This returns a TestSuite made from the tests in the linkage_Test class.  It is required for eric3's unittest tool.
   suite = unittest.makeSuite(testResultComponent_test1)
   suite.addTest(testResultComponent_test2)
   return suite
      
if __name__=='__main__':
   suite()
   unittest.main()

