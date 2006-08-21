#!/usr/bin/env python
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
from Axon.Component import component
import Kamaelia.Util.LossyConnector
from Axon.util import testInterface
from Axon.Postman import postman
from Axon.Linkage import linkage
from Axon.AxonExceptions import noSpaceInBox
from Axon.Ipc import producerFinished, shutdownMicroprocess

testedclass = Kamaelia.Util.LossyConnector.lossyConnector

class lossyConnector_test1(unittest.TestCase):
    def test_smoketest1(self):
        "__init__ - Object creation no arguments."
        self.failUnless(testedclass())
    
    def test_smoketest2(self):
        """__init__ - Checks the created component has the correct inboxes and outboxes ("inbox", "control", "outbox","signal")."""
        self.failUnless(testInterface(testedclass(),(["inbox","control"],["outbox","signal"])))
    
class lossyConnector_test2(unittest.TestCase):
    def deliver(self):
        self.pm.domessagedelivery()
    def runtestedcomponent(self):
        for i in xrange(5):
            self.connector.next()
    def setUp(self):
        self.tester = component()
        self.connector = testedclass()
        self.connector.activate()
        self.pm = postman()
        #pipewidth = 1 implies 2 items in the linkage.  One in outbox and one in sourcebox.  Need to change this code if these semantics change.
        self.pm.registerlinkage(linkage(source = self.tester, sink = self.connector, sourcebox = "outbox", sinkbox = "inbox"))
        self.pm.registerlinkage(linkage(source = self.tester, sink = self.connector, sourcebox = "signal", sinkbox = "control"))
        self.pm.registerlinkage(linkage(source = self.connector, sink = self.tester, sourcebox = "outbox", sinkbox = "inbox", pipewidth = 1))

    def test_linkagetest(self):
        """This test confirms behaviour required for other tests.  It is
        expected that linkages have a capacity of 2.  This test confirms that.
        *** FIX THIS FIRST (in the lossyConnector_test2.setUp() ) ***"""
        self.connector.send(1)
        self.deliver()
        self.connector.send(2)
        self.deliver()
        self.failUnlessRaises(noSpaceInBox, self.connector.send,3)
        
        
    def test_connectorpassesmessage(self):
        """main - inbox - This test confirms a single message is passed from
        inbox to outbox of the connector"""
        testmessage = "Test message."
        self.tester.send(testmessage)
        self.deliver()
        self.runtestedcomponent()
        self.deliver()
        self.failUnless(testmessage is self.tester.recv())
        
    def test_connectordropsmessages(self):
        """ main - inbox - This test confirms that messages are dropped if the outbox is full."""
        self.tester.send(1)
        self.deliver()
        self.tester.send(2)
        self.runtestedcomponent()
        self.deliver()
        self.tester.send(3)
        self.runtestedcomponent()
        self.deliver()
        self.runtestedcomponent()
        self.tester.recv() #1
        self.deliver()
        self.runtestedcomponent()
        self.deliver()
        self.tester.recv() #2
        self.deliver()
        self.runtestedcomponent()
        self.deliver()
        self.failIf(self.tester.dataReady()) #3 has been dropped.
        
    def test_connectorpassessomedropssome(self):
        """main - inbox - This is an extended test of dropping and passing messages that uses
        a known pattern of full buffers to predict when they will be dropped.
        It is currently programmed with the expectation that the linkages can
        contain 2 items."""
        self.tester.send(-1)
        self.deliver()
        self.runtestedcomponent()
        for i in xrange(100): # At this point there should always be one item in the out linkage.
            self.tester.send(i)
            self.deliver()
            self.tester.send('a') # This will be dropped.
            self.runtestedcomponent()
            self.deliver()
            self.runtestedcomponent()
            self.failUnless(self.tester.recv() == i - 1)

    def test_connectorshutsdown_producerfinished(self):
        """main - producerFinished->control - This test confirms that the connector shuts itself down when it is
        sent a producerFinished message."""
        self.tester.send(producerFinished(), "signal")
        self.deliver()
        self.connector.next()
        self.connector.next()
        self.failUnlessRaises(StopIteration, self.connector.next)

    def test_connectorshutsdown_shutdownmicroprocess(self):
        """main - shutdownMicroprocess->control - This test confirms that the connector shuts itself down when it is
        sent a shutdownMicroprocess message."""
        self.tester.send(shutdownMicroprocess(), "signal")
        self.deliver()
        self.connector.next()
        self.connector.next()
        self.failUnlessRaises(StopIteration, self.connector.next)
        
def suite():
   #This returns a TestSuite made from the tests in the linkage_Test class.  It is required for eric3's unittest tool.
   suite = unittest.makeSuite(lossyConnector_test1)
   suite.addTest(lossyConnector_test2)
   return suite
      
if __name__=='__main__':
   suite()
   unittest.main()

