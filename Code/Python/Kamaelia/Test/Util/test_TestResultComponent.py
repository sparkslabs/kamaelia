#!/usr/bin/env python2.3
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

import unittest
from Kamaelia.Util.TestResult import TestResult, StopSystem, StopSystemException
from Axon.Component import component
from Axon.Linkage import linkage
from Axon.Postman import postman
from Axon.util import testInterface
from Axon.Scheduler import scheduler

class TestResult_test1(unittest.TestCase):
    def test_smoketest1(self):
        "__init__ - Object creation no arguments."
        self.failUnless(TestResult())
    
    def test_smoketest2(self):
        """__init__ - Checks the created component has the correct inboxes and outboxes ("inbox", "control", "outbox")."""
        self.failUnless(testInterface(TestResult(),(["inbox","control"],[])))
    
class TestResult_test2(unittest.TestCase):
    def setUp(self):
        self.tester = component()
        self.trcomp = TestResult()
        self.trcomp.activate()
        self.pm = postman()
        self.pm.activate()
        self.tester.activate()
        #pipewidth = 1 implies 2 items in the linkage.  One in outbox and one in sourcebox.  Need to change this code if these semantics change.
        self.pm.registerlinkage(linkage(source = self.tester, sink = self.trcomp, sourcebox = "outbox", sinkbox = "inbox"))
        self.pm.registerlinkage(linkage(source = self.tester, sink = self.trcomp, sourcebox = "signal", sinkbox = "control"))

    def runtestsystem(self):
        for i in range(5):
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
        for i in range(1,100):
            self.tester.send(i)
            self.runtestsystem()

    def test_falseInput2(self):
        "mainBody - Checks that an AssertionError is raised when false value messages are sent to the inbox after a series of true ones. Repeated test."
        for i in range(1,100):
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
   suite = unittest.makeSuite(TestResult_test1)
   suite.addTest(TestResult_test2)
   return suite
      
if __name__=='__main__':
   suite()
   unittest.main()

