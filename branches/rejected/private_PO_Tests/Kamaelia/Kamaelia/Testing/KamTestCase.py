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

import unittest
from unittest import TestSuite, makeSuite, main

import Axon
import Axon.Scheduler             as Scheduler
import Axon.Handle                as Handle
import Axon.background            as background
from Axon.Ipc                     import shutdownMicroprocess
from Kamaelia.Chassis.Graphline   import Graphline

from MessageAdder                 import MessageAdder
from MessageStorer                import MessageStorer

import KamExpectMatcher
import KamMockObject

import new
import time
import Queue

class _AuxiliarTestCase(unittest.TestCase):
    """ 
    KamTestCase can't be a unittest.TestCase, since the test runners would not call
    some methods to start and stop the required infrastructure, and the "setUp" and 
    "tearDown" methods can be overriden by the user (and they commonly don't call 
    the super method), so it must delegate everything to a real unittest.TestCase.
    
    This class (_AuxiliarTestCase) will be used from KamTestCase to call the assert*
    and fail* methods, and to be called by the test runners. Each KamTestCase 
    instance will dynamically create a subclass of _AuxiliarTestCase and it will add
    a method per test method, that will call the real test in the KamTestCase class.
    """
    _kamtestcase = None
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._kamtestcase._register(self)
    def setUp(self):
        self._kamtestcase._initialize()
        self._kamtestcase.setUp()
    def tearDown(self):
        self._kamtestcase.tearDown()
        self._kamtestcase._finish()

class _dummyComponent(Axon.Component.component):
    """A dummy component. Functionality: None. Prevents the scheduler from dying immediately."""
    def main(self):
        while True:
            self.pause()
            yield 1

class KamTestCase(object):
    INITIALIZATION_TIMEOUT = 5
    _dummyComponentInstance = None
    
    def __init__(self, prefix = 'test', *argd, **kwargs):
        super(KamTestCase, self).__init__()
        
        self._kamtest_initialized = False
        self._createTestCase(prefix)
        self._fillTestCaseMethods()
        
    def getTestCase(klazz):
        return klazz().TestCaseClass
    getTestCase = classmethod(getTestCase)
        
    def _createTestCase(self, prefix):
        testMethodNames = [ x for x in dir(self) if x.startswith(prefix) and callable(getattr(self,x)) ]
        testMethods = {}
        for methodName in testMethodNames:
            testMethods[methodName] = getattr(self, methodName)
        testMethods['_kamtestcase'] = self
        self.TestCaseClass = type(self.__class__.__name__ + 'TestCase', (_AuxiliarTestCase,), testMethods)
            
    def _register(self, testCase):
        self._testCase = testCase
        
    def _fillTestCaseMethods(self):
        """ fillTestCaseMethods() -> None
        
        Takes all the assert* and fail* methods in TestCase, and dynamically creates
        methods in "self" that internally call those methods in the twin testCase.
        """
        methods = [ x
                    for x in dir(unittest.TestCase)
                    if x.startswith('assert') or x.startswith('fail')
                ]
                
        def _method_caller(self,*args,**kwargs):
            method = getattr(self._testCase, METHOD_NAME)
            return method(*args, **kwargs)
            
        for methodName in methods:
                method = new.function(_method_caller.func_code, {
                        'METHOD_NAME' : methodName,
                        'getattr'      : getattr,
                        }, methodName)
                setattr(self.__class__, methodName, method)
    
    def createMock(self, inputComponentToMock, outputComponentToMock = None):
        if outputComponentToMock is None:
            outputComponentToMock = inputComponentToMock
        mock = KamMockObject._KamMockObject(inputComponentToMock, outputComponentToMock)
        self._mocks.append(mock)
        return mock
        
    def initializeSystem(self, inputComponentUnderTest, outputComponentUnderTest = None):
        """ initializeSystem(inputComponentUnderTest, [outputComponentUnderTest])
        
        Initializes the kamaelia system, creating a MessageAdder and a MessageStorer which
        interact with the inboxes of inputComponentUnderTest and the outboxes of 
        outputComponentUnderTest.If no outputComponentUnderTest is provided, it falls to 
        inputComponentUnderTest. This method should be called by the user (for example in
        the overriden setUp method).
        """
        if outputComponentUnderTest is None:
            outputComponentUnderTest = inputComponentUnderTest
            
        publicInboxNames = [ inboxName 
                      for inboxName in inputComponentUnderTest.Inboxes 
                        if not inboxName.startswith('_')
                ]
        publicOutboxNames = [ outboxName 
                       for outboxName in outputComponentUnderTest.Outboxes 
                        if not outboxName.startswith('_')
                ]
            
        self._messageAdder         = MessageAdder(publicInboxNames)
        self._messageStorer        = MessageStorer(publicOutboxNames)
        
        linkages = {
            ('', 'control') : ('MESSAGE_ADDER', 'control'), 
        }
        
        for publicInbox in publicInboxNames:
            linkages[('MESSAGE_ADDER', publicInbox)]                = ('INPUT_COMPONENT_UNDER_TEST', publicInbox)
        
        for publicOutbox in publicOutboxNames:
            linkages[('OUTPUT_COMPONENT_UNDER_TEST', publicOutbox)] = ('MESSAGE_STORER', publicOutbox)
        
        self._graph = Graphline(
            MESSAGE_ADDER               = self._messageAdder,
            INPUT_COMPONENT_UNDER_TEST  = inputComponentUnderTest,
            OUTPUT_COMPONENT_UNDER_TEST = outputComponentUnderTest,
            MESSAGE_STORER              = self._messageStorer, 
            linkages                    = linkages, 
        )
        
        self._lf = Handle.Handle(
                    self._graph, 
            ).activate()
        
        if KamTestCase._dummyComponentInstance is None:
            KamTestCase._dummyComponentInstance = _dummyComponent().activate()
            if background.background.lock.acquire(False):
                background.background.lock.release()
                bg = background.background()
                bg.start()
        
        # TODO: not thread-safe...
        max_time = time.time() + self.INITIALIZATION_TIMEOUT
        while len(self._graph.children) == 0:
            cur_time = time.time()
            if cur_time >= max_time:
                raise self.failureException(
                    "Graph children were not created in %s seconds" % self.INITIALIZATION_TIMEOUT
                )
            time.sleep(0.1)
            
        self._kamtest_initialized = True

    def put(self, msg, inbox):
        self._messageAdder.addMessage(msg, inbox)
        
    def get(self, outbox, timeout = 3):
        initial = time.time()
        while time.time() < initial + timeout:
            try:
                #return self._lf.get(outbox)
                return self._messageStorer.getMessage(outbox)
            except IndexError:
                time.sleep(0.1)                
        return self._lf.get(outbox)
        
    def expect(self, matcher, outbox, timeout=5):
        self.assertTrue(isinstance(matcher, KamExpectMatcher.Matcher))
        max_time = time.time() + timeout
        messages = []
        while True:
            remaining = max_time - time.time()
            if remaining <= 0.0:
                raise self.failureException("Expected message: %s not arrived. Arrived messages: %s" %
                                    (matcher, messages)
                            )
            try:
                data = self.get(outbox, timeout=remaining)
            except Queue.Empty:
                raise self.failureException("Expected message: %s not arrived. Arrived messages: %s" %
                                    (matcher, messages)
                            )
            messages.append(data)
            if matcher.matches(data):
                break
                
    def assertOutboxEmpty(self, outbox, msg = None, timeout=0):
        try:
            self.get(outbox, timeout=timeout)
        except Queue.Empty:
            pass # Expected
        else:
            raise self.failureException(
                            msg or "Outbox %s not empty: %s" % (
                                outbox, 
                                self._messageStorer.getMessages(outbox)
                            )
                )

    def clearThreads(self):
        self._messageAdder.addMessage(shutdownMicroprocess(), 'control')
        self._messageAdder.stopMessageAdder(5)
        self._messageStorer.stopMessageStorer(0)
    
    def _initialize(self):
        """ _initialize()
        
        Called before each test, initializes the kamaelia environment.
        """
        self._mocks = []
        self._kamtest_initialized = False
        self._graph = None
        
    def _childrenDone(self):
        realChildren = [ child for child in self._graph.childComponents()
            if child != self._messageAdder and child != self._messageStorer ]
        return len([ child for child in realChildren if not child._isStopped() ]) == 0
    
    def _hasFinished(self, timeout):
        maxTime = time.time() + timeout
        while not self._childrenDone():
            curTime = time.time()
            time.sleep(0.1)
            if maxTime <= curTime:
                return False
        return True
        
    def assertFinished(self, timeout = 0.5,  msg = None):
        if not self._hasFinished(timeout):
            raise self.failureException(
                    msg or "Graph has not finished yet"
                )
                
    def assertNotFinished(self, timeout = 0.5,  msg = None):
        """ assertNotFinished([timeout] [,msg])
        
        Raises a self.failureException if the process has finished before "timeout" 
        seconds have passed. IMPORTANT: if this assert succeeds, "timeout" will have
        passed, so providing high values will produce slow tests!
        """
        if self._hasFinished(timeout):
            raise self.failureException(
                    msg or "Graph has already finished"
                )
    
    def _finish(self):
        """ _finish()
        
        Called after each test, cleans the kamaelia environment.
        """
        if self._kamtest_initialized:
            self.clearThreads()
            self._lf.put(shutdownMicroprocess(), 'control')
            import time
            time.sleep(1)
            self.assertFinished()
            
    def setUp(self):
        pass # To be overriden by the user
        
    def tearDown(self):
        pass # To be overriden by the user
        
