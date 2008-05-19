#!/usr/bin/python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# RecordingChooser tests

import unittest
import sys ; sys.path.append("..")
from TopologyPVR import RecordingChooser
from TopologyPVR import directionNormaliser
from TopologyPVR import timestamper

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess


class RecordingChooser_Internal_InitialisationTests(unittest.TestCase):
    def test_Instantiate_NoArgs(self):
        "__init__ - Creating is fine"
        x=RecordingChooser()
      
    def test_Instiantiate_WithWinding(self):
        "__init__ - Creating with winding=true is fine"
        x=RecordingChooser(winding=True)
      
      
class RecordingChooser_Internal_IterateTests(unittest.TestCase):
    
    def __preroll(self, *arg, **argd):
        Axon.Scheduler.scheduler.run = Axon.Scheduler.scheduler()
        chooser = RecordingChooser(*arg, **argd).activate()

        target = Axon.Component.component().activate()

        chooser.link( (chooser, "outbox"), (target, "inbox") )
        chooser.link( (chooser, "signal"), (target, "control") )
        execute = Axon.Scheduler.scheduler.run.main()

        return chooser, target, execute
            
    
    def test_shutdown(self):
        """Shuts down in response to a shutdownMicroprocess message"""

        for msg in [producerFinished(self), shutdownMicroprocess(self)]:
            chooser = RecordingChooser().activate()

            for _ in xrange(0,10):
                chooser.next()
            self.assert_(0==len(chooser.outboxes["outbox"]))
            self.assert_(0==len(chooser.outboxes["signal"]))

            chooser._deliver( msg, "control" )
            try:
                for _ in xrange(0,10):
                    chooser.next()
                self.fail()
            except StopIteration:
                pass
            self.assert_(0==len(chooser.outboxes["outbox"]))
            self.assert_(1==len(chooser.outboxes["signal"]))
            received =  chooser._collect("signal")
            self.assert_( msg == received )
        
        
                
    
    def test_nooutputifempty(self):
        """Does not output anything if empty"""
        chooser, target, execute = self.__preroll()

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("NEXT", "inbox")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
                

    def test_simpleiterateforwards(self):
        """If filled with 'next' items, then you iterate forwards, you get them all out, but no more than that"""
        chooser, target, execute = self.__preroll()
        payload = ['a','b','1','8']

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
            
        for item in payload:
            chooser._deliver("NEXT", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("NEXT", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
       

                

    def test_iterateforwards(self):
        """You can continue to fill with items whilst getting them out"""
        chooser, target, execute = self.__preroll()
        payload = ['a','b','1','8']
        payload2 = ['p','q','7','36']

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
            
        for item in payload:
            chooser._deliver("NEXT", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload2:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
            
        for item in payload2:
            chooser._deliver("NEXT", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("NEXT", "inbox")
        
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
                
    def test_deferrediterateforwards(self):
        """If you iterate beyond the end, then as new items arrive they'll be output"""
        chooser, target, execute = self.__preroll()
        payload = ['a','b','1','8']

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload:
            chooser._deliver("NEXT", "inbox")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        for item in payload:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        
    def test_iterateforwardsbackwards(self):
        """You can iterate forwards, then back then forwards, etc"""
        chooser, target, execute = self.__preroll()
        payload = ['a','b','1','8']
        
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
            
        for item in payload:
            chooser._deliver("NEXT", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in reversed(payload[:-1]):    # nb last item not repeated
            chooser._deliver("PREV", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload[1:]:             # nb first item not repeated
            chooser._deliver("NEXT", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

            
    def test_backtrackatendendstop(self):
        """If you iterate forwards past the end, then reverse, you won't get the last item repeated"""
        chooser, target, execute = self.__preroll()
        payload = ['a','b','1','8']
        
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
            
        for item in payload:
            chooser._deliver("NEXT", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("NEXT", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("PREV", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        for item in reversed(payload[:-1]):
            chooser._deliver("PREV", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")
          

    
    def test_backtrackatstartendstop(self):
        """If you iterate backwards past the front, then go forwards again, you won't get the first item repeated"""
        chooser, target, execute = self.__preroll()
        payload = ['a','b','1','8']
        
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload:
            chooser._deliver(item, "prevItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
            
        for item in payload:
            chooser._deliver("PREV", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("PREV", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("NEXT", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        for item in reversed(payload[:-1]):
            chooser._deliver("NEXT", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")
          

    
    def test_jumpToFirstLast(self):
        """You can jump to the first or last item. With winding off, the item will be re-emitted if youre' already there"""
        chooser, target, execute = self.__preroll()
        payload = ['a','b','1','8']

        for item in payload:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        chooser._deliver("FIRST", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(target.dataReady("inbox"))
        self.assert_(payload[0] == target.recv("inbox"))
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("FIRST", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(target.dataReady("inbox"))
        self.assert_(payload[0] == target.recv("inbox"))
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("LAST", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(target.dataReady("inbox"))
        self.assert_(payload[-1] == target.recv("inbox"))
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("FIRST", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(target.dataReady("inbox"))
        self.assert_(payload[0] == target.recv("inbox"))
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        
    def test_winding(self):
        """With winding on, jumping will wind to the first or last item, emitting all items on the way. If you're already there, nothing is emitted"""
        chooser, target, execute = self.__preroll(winding=True)
        payload = ['a','b','1','8']

        for item in payload:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        chooser._deliver("FIRST", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(target.dataReady("inbox"))
        self.assert_(payload[0] == target.recv("inbox"))
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("FIRST", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("LAST", "inbox")
        for e in xrange(1,100): execute.next()
        for item in payload[1:]:
            self.assert_(target.dataReady("inbox"))
            self.assert_(item == target.recv("inbox"))
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("LAST", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("FIRST", "inbox")
        for e in xrange(1,100): execute.next()
        for item in reversed(payload[:-1]):
            self.assert_(target.dataReady("inbox"))
            self.assert_(item == target.recv("inbox"))
        self.assert_(not target.dataReady("inbox"))
        

    def test_simpleiteratebackwards(self):
        """If filled with 'prev' items, then you iterate backwards, you get them all out, but no more than that"""
        chooser, target, execute = self.__preroll()
        payload = ['a','b','1','8']

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload:
            chooser._deliver(item, "prevItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
            
        for item in payload:
            chooser._deliver("PREV", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("PREV", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
       

                

    def test_iteratebackwards(self):
        """You can continue to fill with items (backwards) whilst getting them out"""
        chooser, target, execute = self.__preroll()
        payload = ['a','b','1','8']
        payload2 = ['p','q','7','36']

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload:
            chooser._deliver(item, "prevItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
            
        for item in payload:
            chooser._deliver("PREV", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload2:
            chooser._deliver(item, "prevItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
            
        for item in payload2:
            chooser._deliver("PREV", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("PREV", "inbox")
        
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
                
    def test_deferrediteratebackwards(self):
        """If you iterate beyond the end, then as new items arrive they'll be output"""
        chooser, target, execute = self.__preroll()
        payload = ['a','b','1','8']

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in payload:
            chooser._deliver("PREV", "inbox")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        for item in payload:
            chooser._deliver(item, "prevItems")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"), "Expected item to be ready")
            self.assert_(item == target.recv("inbox"), "Expected "+str(item)+" to be emitted")

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
                                

    def test_startinmiddle(self):
        """If you add items to the front and back, then iterating, you start in the middle"""        
        chooser, target, execute = self.__preroll()
        prev = ['a','b','c','d']
        next = ['1','2','3','4','5']
        
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in prev:
            chooser._deliver(item, "prevItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in next:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        for item in next:
            chooser._deliver("NEXT", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"))
            self.assert_(item == target.recv("inbox"))
            self.assert_(not target.dataReady("inbox"))
            
        for item in reversed(next[:-1]):
            chooser._deliver("PREV", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"))
            self.assert_(item == target.recv("inbox"))
            self.assert_(not target.dataReady("inbox"))

        for item in prev:
            chooser._deliver("PREV", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"))
            self.assert_(item == target.recv("inbox"))
            self.assert_(not target.dataReady("inbox"))
            
        for item in reversed(prev[:-1]):
            chooser._deliver("NEXT", "inbox")
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"))
            self.assert_(item == target.recv("inbox"))
            self.assert_(not target.dataReady("inbox"))
                    
        
    def test_startinmiddle_jumptofirst(self):
        """If you add items to the front and back, then jump to first, you start at that point"""        
        chooser, target, execute = self.__preroll()
        prev = ['a','b','c','d']
        next = ['1','2','3','4','5']
        
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in prev:
            chooser._deliver(item, "prevItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in next:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("FIRST", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(target.dataReady("inbox"))
        self.assert_(prev[-1] == target.recv("inbox"))
        
    def test_startinmiddle_jumptolast(self):
        """If you add items to the front and back, then jump to last, you start at that point"""        
        chooser, target, execute = self.__preroll()
        prev = ['a','b','c','d']
        next = ['1','2','3','4','5']
        
        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in prev:
            chooser._deliver(item, "prevItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))

        for item in next:
            chooser._deliver(item, "nextItems")
            for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        
        chooser._deliver("LAST", "inbox")
        for e in xrange(1,10): execute.next()
        self.assert_(target.dataReady("inbox"))
        self.assert_(next[-1] == target.recv("inbox"))
        


class timestamperTests(unittest.TestCase):
    
    def __preroll(self, *arg, **argd):
        Axon.Scheduler.scheduler.run = Axon.Scheduler.scheduler()
        ontest = timestamper(*arg, **argd).activate()

        target = Axon.Component.component().activate()

        ontest.link( (ontest, "outbox"), (target, "inbox") )
        ontest.link( (ontest, "signal"), (target, "control") )
        execute = Axon.Scheduler.scheduler.run.main()

        return ontest, target, execute
            
    
    def test_shutdown(self):
        """Shuts down in response to a shutdownMicroprocess message"""

        for msg in [producerFinished(self), shutdownMicroprocess(self)]:
            ontest = timestamper().activate()

            for _ in xrange(0,10):
                ontest.next()
            self.assert_(0==len(ontest.outboxes["outbox"]))
            self.assert_(0==len(ontest.outboxes["signal"]))

            ontest._deliver( msg, "control" )
            try:
                for _ in xrange(0,10):
                    ontest.next()
                self.fail()
            except StopIteration:
                pass
            self.assert_(0==len(ontest.outboxes["outbox"]))
            self.assert_(1==len(ontest.outboxes["signal"]))
            received =  ontest._collect("signal")
            self.assert_( msg == received )

            
    def test_noinputnooutput(self):
        """No input, no output"""
        timestamper, target, execute = self.__preroll()
        
        for i in range(0,100):
            execute.next()
        self.assert_( not target.dataReady("inbox") )
        self.assert_( not target.dataReady("control") )
        
        
    def test_outputisinputtupledwithtimestamp(self):
        """Output is (timestamp, input)"""
        timestamper, target, execute = self.__preroll()

        data = ("flurble", "plig", 7)
        timestamper._deliver( data, "inbox")
        for i in range(0,10): execute.next()

        self.assert_( target.dataReady("inbox") )
        (ts, d) = target.recv("inbox")
        self.assert_( d == data )

        
    def test_timestampsascend(self):
        """Timestamps ascend. No two are the same."""
        timestamper, target, execute = self.__preroll()

        items1 = [ 'a', ('b',7), 'c', 'd', 'e' ]
        items2 = [ 9, 4, 2, None ]

        for item in items1:
            timestamper._deliver( item, "inbox")
            
        for i in range(0,100): execute.next()

        for item in items2:
            timestamper._deliver( item, "inbox")
            for i in range(0,10): execute.next()
        
        self.assert_( target.dataReady("inbox") )
        (prevts, d) = target.recv("inbox")
        self.assert_( d == items1[0] )
        
        for item in items1[1:] + items2:
            self.assert_( target.dataReady("inbox") )
            (ts, d) = target.recv("inbox")
            self.assert_( d == item )
            self.assert_( prevts < ts )
            prevts = ts
        
        

class directionNormaliser_Tests(unittest.TestCase):
    
    def __preroll(self, *arg, **argd):
        Axon.Scheduler.scheduler.run = Axon.Scheduler.scheduler()
        normaliser = directionNormaliser(*arg, **argd).activate()

        target = Axon.Component.component().activate()

        normaliser.link( (normaliser, "outbox"), (target, "inbox") )
        normaliser.link( (normaliser, "signal"), (target, "control") )
        execute = Axon.Scheduler.scheduler.run.main()

        return normaliser, target, execute
            
    
    def test_shutdown(self):
        """Shuts down in response to a shutdownMicroprocess message"""

        for msg in [producerFinished(self), shutdownMicroprocess(self)]:
            normaliser = directionNormaliser().activate()

            for _ in xrange(0,10):
                normaliser.next()
            self.assert_(0==len(normaliser.outboxes["outbox"]))
            self.assert_(0==len(normaliser.outboxes["signal"]))

            normaliser._deliver( msg, "control" )
            try:
                for _ in xrange(0,10):
                    normaliser.next()
                self.fail()
            except StopIteration:
                pass
            self.assert_(0==len(normaliser.outboxes["outbox"]))
            self.assert_(1==len(normaliser.outboxes["signal"]))
            received =  normaliser._collect("signal")
            self.assert_( msg == received )
        
        
        
    def test_behaviour1(self):
        """Does not output anything if nothing is passed in"""
        normaliser, target, execute = self.__preroll()

        for e in xrange(1,10): execute.next()
        self.assert_(not target.dataReady("inbox"))
        

    def test_behaviour1a(self):
        """First the first item, always the 2nd item of the tuple is returned"""
        normaliser, target, execute = self.__preroll()

        item = (5,'p','P')
        normaliser._deliver( item, "inbox" )
        for e in xrange(1,10): execute.next()
        self.assert_(target.dataReady("inbox"))
        self.assert_(target.recv("inbox") == item[1])
        

    def test_behaviour2(self):
        """When you go forwards through timestamps, the 2nd item of the tuple is returned"""
        normaliser, target, execute = self.__preroll()

        for item in [ (1,'a','A'), (2,'b','B'), (3,'c','C'), (4,'d','D') ]:
            normaliser._deliver( item, "inbox" )
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"))
            self.assert_(target.recv("inbox") == item[1])
            

    def test_behaviour3(self):
        """When you go backwards through timestamps, the 3nd item of the tuple is returned."""
        normaliser, target, execute = self.__preroll()

        item = (5,'p','P')
        normaliser._deliver( item, "inbox" )
        for e in xrange(1,10): execute.next()
        self.assert_(target.dataReady("inbox"))
        self.assert_(target.recv("inbox") == item[1])

        for item in [ (4,'a','A'), (3,'b','B'), (2,'c','C'), (1,'d','D') ]:
            normaliser._deliver( item, "inbox" )
            for e in xrange(1,10): execute.next()
            self.assert_(target.dataReady("inbox"))
            self.assert_(target.recv("inbox") == item[2])
            
        
                        
if __name__=='__main__':
   unittest.main()
