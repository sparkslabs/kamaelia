#!/usr/bin/python

import unittest

import sys; sys.path.append("../")
import Selector as SELECTORMODULE
from Selector import Selector

import Axon
from Axon.Ipc import shutdown
from Kamaelia.KamaeliaIPC import newReader, removeReader, newWriter, removeWriter, newExceptional, removeExceptional

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
   def __init__(self, results=None):
       self.log = [] 
       self.results = results
   # We're using this simply as a namespace.
   def select(self,*args):
       self.log.append(("select", args))
       readers,writers, excepts, timeout = args
       if self.results is not None:
           try:
               result = self.results[0]
               del self.results[0]
               return result
           except IndexError:
               return [],[],[]
       else:
           return readers,writers, excepts
   def addResults(self, results):
       self.results.extend(results)


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
        for i in xrange(100): S.next()
        dummyservice = (Axon.Component.component(), "inbox")
        S._deliver(newReader(S,( dummyservice, "LOOKINGFORTHIS")),"notify")
        for i in xrange(100): S.next()
        func, args = MOCKSELECTORMODULE.log[0]
        self.assertEqual("select", func, "select was called in the main loop")
        self.assertEqual(["LOOKINGFORTHIS"], args[0], "The selectable was added to the list of readables")
        self.assertEqual([], args[1], "Writable set should be empty")
        self.assertEqual([], args[2], "Exception set should be empty")
        self.assertEqual(0, args[3], "The select should be non-blocking")

    def test_WeSendTheSelectorAServiceAndSelectableOnlySelectsTheSelectable(self):
        "main - When we send the newReader message, it also includes a service upon which the selector can talk back to us. The selector only selects on the selectable part of the newReader message"

        MOCKSELECTORMODULE = MockSelect()
        SELECTORMODULE.select = MOCKSELECTORMODULE
        S = Selector()
        S.activate()
        for i in xrange(100): S.next()
        dummyservice = (Axon.Component.component(), "inbox")
        S._deliver(newReader(S,( dummyservice, "LOOKINGFORTHIS") ),"notify")
        for i in xrange(100): S.next()
        func, args = MOCKSELECTORMODULE.log[0]
        self.assertEqual("select", func, "select was called in the main loop")
        self.assertEqual(["LOOKINGFORTHIS"], args[0])#, "The selectable was added to the list of readables")
        self.assertEqual([], args[1], "Writable set should be empty")
        self.assertEqual([], args[2], "Exception set should be empty")
        self.assertEqual(0, args[3], "The select should be non-blocking")

    def test_SendingMultipleReadersResultsInAllSelected(self):
        "main - Sending multiple newReader messages results in all being select()ed"

        MOCKSELECTORMODULE = MockSelect()
        SELECTORMODULE.select = MOCKSELECTORMODULE
        S = Selector()
        S.activate()
        for i in xrange(100): S.next()
        dummyservice = (Axon.Component.component(), "inbox")
        S._deliver(newReader(S,( dummyservice, "LOOKINGFORTHIS") ),"notify")
        S._deliver(newReader(S,( dummyservice, "LOOKINGFORTHISTOO") ),"notify")
        S._deliver(newReader(S,( dummyservice, "LOOKINGFORANDTHIS") ),"notify")
        for i in xrange(100): 
            S.next()
        lastfunc, lastargs = None, None
        i = 0
        func, args = MOCKSELECTORMODULE.log[i]
        while not( (lastfunc, lastargs) == (func, args)): # Search for quiescent state
            i = i + 1
            lastfunc, lastargs = func, args
            func, args = MOCKSELECTORMODULE.log[i]

        self.assertEqual("select", func, "select was called in the main loop")
        self.assertEqual(["LOOKINGFORTHIS","LOOKINGFORTHISTOO","LOOKINGFORANDTHIS"], args[0])#, "The selectable was added to the list of readables")

    def test_ActivityOnReaderResultsInMessageOnReadersService(self):
        "main - Activity on the selectable results in a message appearing in the service provided to the selector"

        MOCKSELECTORMODULE = MockSelect()
        SELECTORMODULE.select = MOCKSELECTORMODULE
        S = Selector()
        S.activate()
        for i in xrange(100): S.next()
        D = Axon.Component.component() 
        dummyservice = (D, "inbox")
        S._deliver(newReader(S,( dummyservice, "LOOKINGFORTHIS") ),"notify")

        for i in xrange(100):
            S.next();
            try:
               S.postoffice.next()
            except:
               pass
        self.assert_(not ( len(D.inboxes["inbox"]) == 0 ) )
        selectable = D.recv("inbox")
        self.assertEqual(selectable,"LOOKINGFORTHIS")#, "The value returned should be the selectable we originally asked for")

    def test_ActivityOnAnyReaderResultsInMessageOnThatReadersService(self):
        "main - Activity on a selectable results in a message appearing in the service provided to the selector for that selectable"

        MOCKSELECTORMODULE = MockSelect(results=[ (["LOOKINGFORTHIS"],[],[]), 
                                                  (["THENFORTHIS"],[],[]), 
                                                  (["ANDTHENFORTHIS"],[],[]) ])
        SELECTORMODULE.select = MOCKSELECTORMODULE
        S = Selector()
        S.activate()
        for i in xrange(100): S.next()
        D = Axon.Component.component()
        E = Axon.Component.component()
        F = Axon.Component.component()
        dummyservice1 = (D, "inbox")
        S._deliver(newReader(S,( dummyservice1, "LOOKINGFORTHIS") ),"notify")
        dummyservice2 = (E, "inbox")
        S._deliver(newReader(S,( dummyservice2, "THENFORTHIS") ),"notify")
        dummyservice3 = (F, "inbox")
        S._deliver(newReader(S,( dummyservice3, "ANDTHENFORTHIS") ),"notify")

        for i in xrange(100):
            S.next();
            try:
               S.postoffice.next()
            except:
               pass
        selectable = D.recv("inbox")
        self.assertEqual(selectable,"LOOKINGFORTHIS")#, "The value returned should be the selectable we originally asked for")
        selectable = E.recv("inbox")
        self.assertEqual(selectable,"THENFORTHIS")#, "The value returned should be the selectable we originally asked for")
        selectable = F.recv("inbox")
        self.assertEqual(selectable,"ANDTHENFORTHIS")#, "The value returned should be the selectable we originally asked for")

    def test_RemoveReader_ResultsInReaderNoLongerBeingSelectedOrWiredIn(self):
        "main - Sending a remove reader message unwires/links a component, and also removes it's selectable from the readers list"
        MOCKSELECTORMODULE = MockSelect(results=[ ([], [], [] )])
        SELECTORMODULE.select = MOCKSELECTORMODULE
        S = Selector()
        S.activate()
        for i in xrange(100): S.next()
        D = Axon.Component.component() 
        dummyservice = (D, "inbox")
        S._deliver(newReader(S,( dummyservice, "LOOKINGFORTHIS") ),"notify")
        S._deliver(removeReader(S,"LOOKINGFORTHIS"),"notify")

        for i in xrange(100):
            S.next();
            try:
               S.postoffice.next()
            except:
               pass
        self.assert_( len(D.inboxes["inbox"]) == 0 )



    def test_ActivityOnAnyWriterResultsInMessageOnThatWritersService(self):
        "main - Activity on a selectable results in a message appearing in the service provided to the selector for that selectable"

        MOCKSELECTORMODULE = MockSelect(results=[ ([],["LOOKINGFORTHIS"],[]), 
                                                  ([],["THENFORTHIS"],[]), 
                                                  ([],["ANDTHENFORTHIS"],[]) ])
        SELECTORMODULE.select = MOCKSELECTORMODULE
        S = Selector()
        S.activate()
        for i in xrange(100): S.next()
        D = Axon.Component.component()
        E = Axon.Component.component()
        F = Axon.Component.component()
        dummyservice1 = (D, "inbox")
        S._deliver(newWriter(S,( dummyservice1, "LOOKINGFORTHIS") ),"notify")
        dummyservice2 = (E, "inbox")
        S._deliver(newWriter(S,( dummyservice2, "THENFORTHIS") ),"notify")
        dummyservice3 = (F, "inbox")
        S._deliver(newWriter(S,( dummyservice3, "ANDTHENFORTHIS") ),"notify")

        for i in xrange(100):
            S.next();
            try:
               S.postoffice.next()
            except:
               pass
        selectable = D.recv("inbox")
        self.assertEqual(selectable,"LOOKINGFORTHIS")#, "The value returned should be the selectable we originally asked for")
        selectable = E.recv("inbox")
        self.assertEqual(selectable,"THENFORTHIS")#, "The value returned should be the selectable we originally asked for")
        selectable = F.recv("inbox")
        self.assertEqual(selectable,"ANDTHENFORTHIS")#, "The value returned should be the selectable we originally asked for")

    def test_RemoveWriter_ResultsInWriterNoLongerBeingSelectedOrWiredIn(self):
        "main - Sending a remove writer message unwires/links a component, and also removes it's selectable from the writers list"
        MOCKSELECTORMODULE = MockSelect(results=[ ([], [], [] )])
        SELECTORMODULE.select = MOCKSELECTORMODULE
        S = Selector()
        S.activate()
        for i in xrange(100): S.next()
        D = Axon.Component.component() 
        dummyservice = (D, "inbox")
        S._deliver(newWriter(S,( dummyservice, "LOOKINGFORTHIS") ),"notify")
        S._deliver(removeWriter(S,"LOOKINGFORTHIS"),"notify")

        for i in xrange(100):
            S.next();
            try:
               S.postoffice.next()
            except:
               pass
        print 
        self.assert_( len(D.inboxes["inbox"]) == 0 )

    def test_ActivityOnAnyExceptionalResultsInMessageOnThatExceptionalsService(self):
        "main - Activity on a selectable results in a message appearing in the service provided to the selector for that selectable"

        MOCKSELECTORMODULE = MockSelect(results=[ ([],[],["LOOKINGFORTHIS"]), 
                                                  ([],[],["THENFORTHIS"]), 
                                                  ([],[],["ANDTHENFORTHIS"]) ])
        SELECTORMODULE.select = MOCKSELECTORMODULE
        S = Selector()
        S.activate()
        for i in xrange(5): S.next()
        D = Axon.Component.component()
        E = Axon.Component.component()
        F = Axon.Component.component()
        dummyservice1 = (D, "inbox")
        S._deliver(newExceptional(S,( dummyservice1, "LOOKINGFORTHIS") ),"notify")
        dummyservice2 = (E, "inbox")
        S._deliver(newExceptional(S,( dummyservice2, "THENFORTHIS") ),"notify")
        dummyservice3 = (F, "inbox")
        S._deliver(newExceptional(S,( dummyservice3, "ANDTHENFORTHIS") ),"notify")

        for i in xrange(5):
            S.next();
            try:
               S.postoffice.next()
            except:
               pass
        selectable = D.recv("inbox")
        self.assertEqual(selectable,"LOOKINGFORTHIS")#, "The value returned should be the selectable we originally asked for")
        selectable = E.recv("inbox")
        self.assertEqual(selectable,"THENFORTHIS")#, "The value returned should be the selectable we originally asked for")
        selectable = F.recv("inbox")
        self.assertEqual(selectable,"ANDTHENFORTHIS")#, "The value returned should be the selectable we originally asked for")

    def test_RemoveExceptional_ResultsInExceptionalNoLongerBeingSelectedOrWiredIn(self):
        "main - Sending a remove exceptional message unwires/links a component, and also removes it's selectable from the exceptionals list"
        MOCKSELECTORMODULE = MockSelect(results=[ ([], [], [] )])
        SELECTORMODULE.select = MOCKSELECTORMODULE
        S = Selector()
        S.activate()
        for i in xrange(100): S.next()
        D = Axon.Component.component() 
        dummyservice = (D, "inbox")
        S._deliver(newExceptional(S,( dummyservice, "LOOKINGFORTHIS") ),"notify")
        S._deliver(removeExceptional(S,"LOOKINGFORTHIS"),"notify")

        for i in xrange(100):
            S.next();
            try:
               S.postoffice.next()
            except:
               pass
        self.assert_( len(D.inboxes["inbox"]) == 0 )

if __name__=="__main__":
    unittest.main()
