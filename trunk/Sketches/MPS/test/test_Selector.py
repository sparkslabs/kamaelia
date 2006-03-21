#!/usr/bin/python

import unittest

import sys; sys.path.append("../")
import Selector as SELECTORMODULE
from Selector import Selector

import Axon
from Axon.Ipc import shutdown
from Kamaelia.KamaeliaIPC import newReader

class SmokeTests_Selector(unittest.TestCase):
    def test_SmokeTest(self):
        """__init__ - Called with no arguments succeeds"""
        S = Selector()
        self.assert_(isinstance(S, Axon.Component.component))

    def test_RunsForever(self):
        """main - Run with no messages, keeps running"""
        S = Selector()
        S.activate()
        for i in xrange(1,100):
            try:
                S.next()
            except StopIteration:
                self.fail("Component should run until told to stop. Failed on iteration: "+str(i))

    def test_PausesUntilFirstMessage(self):
        """main - Before we recieve any messages telling us what to watch for, the system should pause and yield"""
        S = Selector()
        S.activate()
        V = S.next()
        self.assert_(S._isRunnable() is not True)

    def test_shutdownMessageCausesShutdown(self):
        """main - If the component recieves a shutdown() message, the component shuts down"""
        S = Selector()
        S.activate()

        S._deliver(shutdown(),"control")

        componentExit = False
        for i in xrange(2000):
            try:
                S.next()
            except StopIteration:
                componentExit = True
                break
        if not componentExit:
            self.fail("When sent a shutdown message, the component should shutdown")

class MockSelect:
   """This is needed because we need to test that select is being used correctly"""
   def __init__(self):
       self.log = [] 
   # We're using this simply as a namespace.
   def select(self,*args):
       self.log.append(("select", args))

class Readables_Selector(unittest.TestCase):
    def test_SelectIsMockable(self):
        "main - The module uses select, and that is externally mockable"
        try:
            SELECTORMODULE.select
        except AttributeError:
            self.fail("Should import the select module")

    def test_SendingAReadableMessageResultsInItBeingSelectedAgainst(self):
        "main - If we send a newReader message to the notify inbox, it results in the selectable reader being selected on in the readers set"
        MOCKSELECTORMODULE = MockSelect()
        SELECTORMODULE.select = MOCKSELECTORMODULE
        S = Selector()
        S.activate()
        S._deliver(newReader(S,"LOOKINGFORTHIS"),"notify")
        for i in xrange(100):
            S.next()
        func, args = MOCKSELECTORMODULE.log[0]
        self.assertEqual("select", func, "select was called in the main loop")
        self.assertEqual(["LOOKINGFORTHIS"], args[0], "The selectable was added to the list of readables")
        self.assertEqual([], args[1], "Writable set should be empty")
        self.assertEqual([], args[2], "Exception set should be empty")
        self.assertEqual(0, args[3], "The select should be non-blocking")

if __name__=="__main__":
    unittest.main()
