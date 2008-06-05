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

import Axon.Scheduler             as Scheduler
from Kamaelia.Chassis.Graphline   import Graphline

from MessageAdder                 import MessageAdder
from MessageStorer                import MessageStorer

class KamTestCase(unittest.TestCase):
    
    # TODO: this number of steps depends too much on the situation :-S
    DEFAULT_STEP_NUMBER = 1000
    
    def __init__(self, *argd, **kwargs):
        # Might not be an object
        unittest.TestCase.__init__(self, *argd, **kwargs)
        self._kamtest_initialized = False
        
    def initializeSystem(self, inputComponentUnderTest, outputComponentUnderTest = None):
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
            
        self.messageAdder         = MessageAdder(publicInboxNames)
        self.messageStorer        = MessageStorer(publicOutboxNames)
        
        linkages = {}
        
        for publicInbox in publicInboxNames:
            linkages[('MESSAGE_ADDER', publicInbox)]                = ('INPUT_COMPONENT_UNDER_TEST', publicInbox)
        
        for publicOutbox in publicOutboxNames:
            linkages[('OUTPUT_COMPONENT_UNDER_TEST', publicOutbox)] = ('MESSAGE_STORER', publicOutbox)
        
        self.graph = Graphline(
            MESSAGE_ADDER               = self.messageAdder,
            INPUT_COMPONENT_UNDER_TEST  = inputComponentUnderTest,
            OUTPUT_COMPONENT_UNDER_TEST = outputComponentUnderTest,
            MESSAGE_STORER              = self.messageStorer, 
            linkages                    = linkages, 
        )
        
        self._kamtest_initialized = True
    
    def _listThreads(self):
        scheduler = self.graph.__class__.schedulerClass.run
        threads   = scheduler.listAllThreads()
        scheduler.debuggingon = False
        return threads
        
    def clearThreads(self):
        # Reboot the scheduler
        self.graph.__class__.schedulerClass.run = None
        self.graph.__class__.schedulerClass()
        
    # TODO: this shouldn't be overriden; maybe I need to use delegation instead of inheritance
    def tearDown(self):
        if self._kamtest_initialized:
            scheduler = self.graph.__class__.schedulerClass.run
            scheGenerator  = scheduler.main(0, canblock=False)
            n = 0
            try:
                while n < 100:
                    scheGenerator.next()
                    n += 1
            except StopIteration, si:
                pass
            
            threads = self._listThreads()
            
            self.clearThreads()
            
            if len(threads) > 0:
                raise self.failureException("Processes still running: %s" % threads)
    
    def _runSteps(self, steps):
        if steps is None:
            steps = self.DEFAULT_STEP_NUMBER
        self.messageAdder.stopMessageAdder(steps)
        self.messageStorer.stopMessageStorer(steps)
        
        self.graph.activate()
        scheduler      = self.graph.__class__.schedulerClass.run
        scheGenerator  = scheduler.main(0, canblock=False)
        
        # TODO: These numbers must change
        # Lower to this values doesn't work
        # Higher will work in KamPlanet ConfigFileParser, but 
        # it's not sure that it will work when testing other 
        # classes. 
        # I wouldn't mind setting them to 100 or whatever
        # but take a closer look
        MAGIC_NUMBER_BEFORE_SETTING_LIST_THREADS = 6
        MAGIC_NUMBER_TO_BE_ADDED_TO_STEPS        = 5
        
        # In the beginning, calling _listThreads will return []
        for _ in xrange(MAGIC_NUMBER_BEFORE_SETTING_LIST_THREADS):
            scheGenerator.next()
        
        # Later the real iteration
        for _ in xrange(steps + MAGIC_NUMBER_TO_BE_ADDED_TO_STEPS): 
            try:
                n = len(self._listThreads())
                if n == 0:
                    break
                iteration_counter = 0
                while iteration_counter < n:
                    scheGenerator.next()
                    iteration_counter += 1
                    n = len(self._listThreads())
            except StopIteration:
                break        
    
    def assertStopping(self, msg = None, steps = None):
        """
        assertStopping(msg, steps) -> None
        
        It will run the scheduler several times, assuring that the 
        messageAdder and the messageStorer will be run "steps" times.
        
        The idea is to iterate the minimum number of times so we 
        assure that the scheduler is run the number of $(steps 
        provided * the number of threads being run at each step). It's
        not a real problem to let it run more times, but at some point
        it must finish. When it finishes, if there is any thread still
        alive, it will raise an AssertionError with the message "msg"
        (if provided).
        """
        self._runSteps(steps)
        # Check the number of threads
        threads = self._listThreads()
        if len(threads) > 0:
            # first clean creating a new scheduler
            self.graph.__class__.schedulerClass.run = Scheduler.scheduler()
            # then raise the failureException
            raise self.failureException(msg or "Processes still running: %s" % threads)

    def assertNotStopping(self, msg = None, steps = None, clear = False):
        """
        runMessageExchange(msg, steps) -> None
        
        It will run the scheduler several times, assuring that the 
        messageAdder and the messageStorer will be run "steps" times.
        
        The idea is to iterate the minimum number of times so we 
        assure that the scheduler is run the number of $(steps 
        provided * the number of threads being run at each step). It's
        not a real problem to let it run more times, but at some point
        it must finish. When it finishes, if there is any thread still
        alive, it will raise an AssertionError with the message "msg"
        (if provided).
        """
        self._runSteps(steps)
        
        # Check the number of threads
        threads = self._listThreads()
        if len(threads) == 0:
            self.clearThreads()
            # then raise the failureException
            raise self.failureException(msg or "Processes still running: %s" % threads)
        else:
            if clear:
                self.clearThreads()


import pmock

# pmock extension. 
# TODO: it should be part of pmock instead of KamTestCase, just as it seems to be at jMock:
# http://www.jmock.org/javadoc/2.4.0/org/jmock/Expectations.html#exactly(int)
# 
class ExactInvocationMatcher(pmock.InvokedRecorderMatcher):
    def __init__(self, number, *args,  **kwargs):
        super(ExactInvocationMatcher, self).__init__(*args, **kwargs)
        self._number  = number
        self._counter = 0
        
    def __str__(self):
        def plural_times(times):
            if times == 1:
                return "time"
            else:
                return "times"
                
        return "expected %s %s and invoked %s %s" % (
                                    self._number, 
                                    plural_times(self._number), 
                                    self._counter, 
                                    plural_times(self._counter), 
                            )
        
    def matches(self, invocation):
        return self._counter < self._number
        
    def invoked(self, invocation):
        super(ExactInvocationMatcher, self).invoked(invocation)
        self._counter += 1
        
    def verify(self):
        if self._counter < self._number:
            raise AssertionError("More times expected")
        
def exactly(number):
    return ExactInvocationMatcher(number)
