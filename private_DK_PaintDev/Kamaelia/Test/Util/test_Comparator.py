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

import unittest
from Axon.Component import component
from Kamaelia.Util.Comparator import Comparator
from Axon.util import testInterface
from Axon.Postman import postman
from Axon.Linkage import linkage
from Axon.Ipc import shutdownMicroprocess, producerFinished

class Comparator_test1(unittest.TestCase):
    def test_smoketest1(self):
        """__init__ - Basic creation test."""
        self.failUnless(Comparator())
        
    def test_smoketest2(self):
        """__init__ - Checks the created component has the correct inboxes and outboxes ("inA", "inB", "control", "outbox" and "signal")."""
        self.failUnless(testInterface(Comparator(),(["inA","inB","control"],["outbox", "signal"])))

class Comparator_test2(unittest.TestCase):
    def setUp(self):
        self.testerA = component()
        self.testerB = component()
        self.Comparator = Comparator()
        self.Comparator.activate()
        self.pm = postman()
        #pipewidth = 1 implies 2 items in the linkage.  One in outbox and one in sourcebox.  Need to change this code if these semantics change.
        self.pm.registerlinkage(linkage(source = self.testerA, sink = self.Comparator, sourcebox = "outbox", sinkbox = "inA"))
        self.pm.registerlinkage(linkage(source = self.testerB, sink = self.Comparator, sourcebox = "outbox", sinkbox = "inB"))
        self.pm.registerlinkage(linkage(source = self.testerA, sink = self.Comparator, sourcebox = "signal", sinkbox = "control"))
        self.pm.registerlinkage(linkage(source = self.Comparator, sink = self.testerA, sourcebox = "outbox", sinkbox = "inbox"))
        self.pm.registerlinkage(linkage(source = self.Comparator, sink = self.testerA, sourcebox = "signal", sinkbox = "control"))
    

    def runtestsystem(self):
        for i in xrange(5):
            self.Comparator.next()
            self.pm.domessagedelivery()
            
    def test_equality1(self):
        """mainBody - Checks equal inputs on inA and inB produce a true value on output."""
        self.testerA.send("blah")
        self.testerB.send("blah")
        self.runtestsystem()
        self.failUnless(self.testerA.recv())
        
    def test_equality2(self):
        """mainBody - Checks equal inputs on inA and inB produce a true value on output.  Repeated many times."""
        for i in xrange(100):
            self.testerA.send(i)
            self.testerB.send(i)
            self.runtestsystem()
            self.failUnless(self.testerA.recv())
            
    def test_equality3(self):
        """mainBody - Checks equal inputs on inA and inB produce a true value on output.  Repeated many times.  Also messages on one input arrive earlier than the other (but in the same order)."""
        for i in xrange(100):
            self.testerA.send(i)
            self.runtestsystem()
            self.failIf(self.testerA.dataReady())
        for i in xrange(100):
            self.testerB.send(i)
            self.runtestsystem()
            self.failUnless(self.testerA.recv())
        
    def test_inequality1(self):
        """mainBody - Checks different inputs on inA and inB produce a false value on output."""
        self.testerA.send("blah")
        self.testerB.send("bling")
        self.runtestsystem()
        self.failIf(self.testerA.recv()) # Checks that the answer is False
        
    def test_inequality2(self):
        """mainBody - Checks different inputs on inA and inB produce a false value on output.  Repeated many times."""
        for i in xrange(100):
            self.testerA.send(i)
            self.testerB.send(i+1)
            self.runtestsystem()
            self.failIf(self.testerA.recv()) # Checks that the answer is False

    def test_inequality3(self):
        """mainBody - Checks different inputs on inA and inB produce a false value on output.  Repeated many times.  Also messages on one input arrive earlier than the other."""
        for i in xrange(100):
            self.testerA.send(i)
            self.runtestsystem()
            self.failIf(self.testerA.dataReady())
        for i in xrange(100):
            self.testerB.send(i+1)
            self.runtestsystem()
            self.failIf(self.testerA.recv())
            
    def test_shutdownMicroprocess1(self):
        """mainBody - Checks that the Comparator shutsdown when sent a shutdownMicroprocess message on its control box"""
        self.testerA.send(shutdownMicroprocess(), "signal")
        self.failUnlessRaises(StopIteration, self.runtestsystem)
        
    def test_shutdownMicroprocess2(self):
        """mainBody - Checks that the Comparator sends a producerFinished when sent a shutdownMicroprocess message on its control box"""
        self.testerA.send(shutdownMicroprocess(), "signal")
        try:
            self.runtestsystem()
        except: # Bad form except for the fact that this is tested in test_shutdownMicroprocess1
            pass
        self.failUnless(isinstance(self.testerA.recv("control"), producerFinished))
        
    def test_producerFinished1(self):
        """mainBody - Checks that the Comparator shutsdown when sent a producerFinished message on its control box"""
        self.testerA.send(producerFinished(), "signal")
        self.failUnlessRaises(StopIteration, self.runtestsystem)
        
    def test_producerFinished2(self):
        """mainBody - Checks that the Comparator sends a producerFinished when sent a producerFinished message on its control box"""
        self.testerA.send(producerFinished(), "signal")
        try:
            self.runtestsystem()
        except: # Bad form except for the fact that this is tested in test_shutdownMicroprocess1
            pass
        self.failUnless(isinstance(self.testerA.recv("control"), producerFinished))
        
def suite():
   #This returns a TestSuite made from the tests in the linkage_Test class.  It is required for eric3's unittest tool.
   suite = unittest.TestSuite((Comparator_test1,Comparator_test2))
   #suite = unittest.makeSuite(Comparator_test2)
#   suite.addTest(Comparator_test1)
#   suite.addTest(Comparator_test2)
   return suite
      
if __name__=='__main__':
   suite()
   unittest.main()
