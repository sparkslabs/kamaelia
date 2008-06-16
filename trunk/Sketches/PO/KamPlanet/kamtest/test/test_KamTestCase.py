#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
# 
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: PO

import KamTestCase
import unittest

import Axon
from Axon.Ipc import producerFinished

# Receives numbers and strings, and forwards them 
# converted to strings to outbox
class SimpleComponent(Axon.Component.component):
    Inboxes = {
            "inbox"   : "messages (strings)",
            "numbers" : "numbers (integers)", 
            "control"  : "signal messages are placed here", 
        }
    def main(self):
        while True:
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                self.send(data, 'outbox')
            while self.dataReady('numbers'):
                data = self.recv('numbers')
                self.send(str(data), 'outbox')
            while self.dataReady('control'):
                data = self.recv('control')
                self.send(data, 'signal')
                return
            if not self.anyReady():
                self.pause()
            yield 1

def getSimpleComponentTestCaseSucceeding():
    class SimpleSampleTestCase(KamTestCase.KamTestCase):
        def setUp(self):
            self.simpleSample = SimpleComponent()
            self.initializeSystem(self.simpleSample)
        
        def testForwardsNumbers(self):
            self.put(5, 'numbers')
            self.put(6, 'numbers')
            self.putYield(10)
            self.put(producerFinished(), 'control')
            self.assertStopping()
            self.assertEquals('5', self.get('outbox'))
            self.assertEquals('6', self.get('outbox'))
            self.assertOutboxEmpty('outbox')
            self.assertTrue(isinstance(self.get('signal'), producerFinished))
            self.assertOutboxEmpty('signal')
            
    return SimpleSampleTestCase

def getSimpleComponentTestCaseStoppingWhenStopping():
    class SimpleSampleTestCase(KamTestCase.KamTestCase):
        def testExample(self):
            simpleSample = SimpleComponent()
            self.initializeSystem(simpleSample)
            self.put(producerFinished(), 'control')
            self.assertStopping()
    return SimpleSampleTestCase

def getSimpleComponentTestCaseStoppingWhenNotStopping():
    class SimpleSampleTestCase(KamTestCase.KamTestCase):
        def testExample(self):
            simpleSample = SimpleComponent()
            self.initializeSystem(simpleSample)
            self.assertStopping()
    return SimpleSampleTestCase
    
def getSimpleComponentTestCaseNotStoppingWhenNotStopping():
    class SimpleSampleTestCase(KamTestCase.KamTestCase):
        def testExample(self):
            simpleSample = SimpleComponent()
            self.initializeSystem(simpleSample)
            self.assertNotStopping(clear=True)
    return SimpleSampleTestCase
    
def getSimpleComponentTestCaseNotStoppingWhenStopping():
    class SimpleSampleTestCase(KamTestCase.KamTestCase):
        def testExample(self):
            simpleSample = SimpleComponent()
            self.initializeSystem(simpleSample)
            self.put(producerFinished(), 'control')
            self.assertNotStopping()
    return SimpleSampleTestCase
    
def getVerySimpleTestCase(storer = None, withSetUp = True, withTearDown = True):
    if storer is None:
        storer = {}
        
    class SimpleSampleTestCase(KamTestCase.KamTestCase):
        def testExample(self):
            if not 'testCounter' in storer:
                storer['testCounter'] = 0
            storer['testCounter'] = storer['testCounter'] + 1
            
    if withSetUp:
        class SimpleSampleTestCase(SimpleSampleTestCase):
            def setUp(self):
                if not 'setUpCounter' in storer:
                    storer['setUpCounter'] = 0
                storer['setUpCounter'] = storer['setUpCounter'] + 1
    if withTearDown:
        class SimpleSampleTestCase(SimpleSampleTestCase):
            def tearDown(self):
                if not 'tearDownCounter' in storer:
                    storer['tearDownCounter'] = 0
                storer['tearDownCounter'] += storer['tearDownCounter'] + 1
    return SimpleSampleTestCase

class KamTestCaseTestCase(unittest.TestCase):
    def testGetTestCaseWithSetUpAndTearDown(self):
        myStorer = {}
        self.kamTestCase = getVerySimpleTestCase(storer=myStorer, withSetUp=True, withTearDown=True)
        self.testCase    = self.kamTestCase.getTestCase()
        self.assertEquals(
                        self.kamTestCase.testExample.func_code, 
                        self.testCase.testExample.func_code
                    )
        result = self._runTestCase(self.testCase)
        self.assertEquals(1, myStorer['testCounter'])
        self.assertEquals(1, myStorer['setUpCounter'])
        self.assertEquals(1,myStorer['tearDownCounter'])
        
    def testGetTestCaseWithoutSetUpAndTearDown(self):
        myStorer = {}
        self.kamTestCase = getVerySimpleTestCase(storer=myStorer, withSetUp=False, withTearDown=False)
        self.testCase    = self.kamTestCase.getTestCase()
        self.assertEquals(
                self.kamTestCase.testExample.func_code, 
                self.testCase.testExample.func_code
            )
        result = self._runTestCase(self.testCase)
        self.assertEquals(1, myStorer['testCounter'])
        self.assertFalse(myStorer.has_key('setUpCounter'))
        self.assertFalse(myStorer.has_key('tearDownCounter'))
    
    def _runTestCase(self, testCase):
        testSuite = unittest.makeSuite(testCase)
        result    = unittest.TestResult()
        testSuite.run(result)
        return result
        
    def testSimpleComponentRunning(self):
        kamTestCase = getSimpleComponentTestCaseSucceeding()
        testCase    = kamTestCase.getTestCase()
        result = self._runTestCase(testCase)
        self.assertTrue(result.wasSuccessful())
        
    def testStoppingWhenStopping(self):
        kamTestCase = getSimpleComponentTestCaseStoppingWhenStopping()
        testCase    = kamTestCase.getTestCase()
        result = self._runTestCase(testCase)
        self.assertTrue(result.wasSuccessful())
        
    def testStoppingWhenNotStopping(self):
        kamTestCase = getSimpleComponentTestCaseStoppingWhenNotStopping()
        testCase    = kamTestCase.getTestCase()
        result = self._runTestCase(testCase)
        self.assertFalse(result.wasSuccessful())
        
    def testNotStoppingWhenNotStopping(self):
        kamTestCase = getSimpleComponentTestCaseNotStoppingWhenNotStopping()
        testCase    = kamTestCase.getTestCase()
        result = self._runTestCase(testCase)
        self.assertTrue(result.wasSuccessful())
        
    def testNotStoppingWhenStopping(self):
        kamTestCase = getSimpleComponentTestCaseNotStoppingWhenStopping()
        testCase    = kamTestCase.getTestCase()
        result = self._runTestCase(testCase)
        self.assertFalse(result.wasSuccessful())
        
if __name__ == '__main__':
    unittest.main()
