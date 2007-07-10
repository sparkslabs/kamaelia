#!/usr/bin/env python

from likefile import LikeFile, schedulerThread
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
import unittest, random, Axon, threading, time

scheduler = schedulerThread(slowmo=0.001)
scheduler.start()
randlist = [random.random() for x in xrange(0, 10)]

class DyingShunt(component):
    """A component which passes all data through itself, and terminates on receipt of 
    shutdownMicroprocess() or producerFinished()"""
    Inboxes = { "inbox"   : "Input data",
                "control" : "Control data",
                "extrain"   : "An additional nonstandard inbox",
              }
    Outboxes = { "outbox" : "Input data is echoed here",
                 "signal" : "Control data is echoed here",
                 "extraout"  : "Extra data is echoed here",
               }
    def main(self):
        while True:
            yield 1
            while self.dataReady("inbox"):
                self.send(self.recv("inbox"), "outbox")
            while self.dataReady("extrain"):
                self.send(self.recv("extrain"), "extraout")
            while self.dataReady("control"):
                data = self.recv("control")
                self.send(data, "signal")
                if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
                    return

class Dummy(component):
    Inboxes = { "inbox"   : "Input data",
                "control" : "Control data",
                "extraout"   : "An additional nonstandard inbox",
              }
    Outboxes = { "outbox" : "Input data is echoed here",
                 "signal" : "Control data is echoed here",
                 "extrain"  : "Extra data is echoed here",
               }
    def main(self):
        while True:
            yield 1

class Test_DyingShunt(unittest.TestCase):
    """A test for the test dummy component used to test likefile. If this test passes, the behaviour of DyingShunt is assumed to always work."""
    def setUp(self):
        self.oldRun = Axon.Scheduler.scheduler.run
        self.scheduler = Axon.Scheduler.scheduler()
        Axon.Scheduler.scheduler.run = self.scheduler
        self.shunt = DyingShunt()
        self.inSrc = Dummy()
        self.inSrc.link((self.inSrc,"outbox"), (self.shunt,"inbox"))
        self.inSrc.link((self.inSrc,"signal"), (self.shunt,"control"))
        self.inSrc.link((self.inSrc,"extrain"), (self.shunt,"extrain"))
        self.outDest = Dummy()
        self.outDest.link((self.shunt,"outbox"), (self.outDest,"inbox"))
        self.outDest.link((self.shunt,"signal"), (self.outDest,"control"))
        self.outDest.link((self.shunt,"extraout"), (self.outDest,"extraout"))
        self.run = self.scheduler.main()
        self.shunt.activate()

    def tearDown(self):
        del self.run, self.shunt, Axon.Scheduler.scheduler.run
        Axon.Scheduler.scheduler.run = self.oldRun
    def runFor(self, iterations):
        for i in xrange(0, iterations):
            self.run.next()

    def test_passthrough(self):
        for i in randlist:
            self.inSrc.send(i, "outbox")
            self.inSrc.send(i + 1, "signal")
            self.inSrc.send(i + 2, "extrain")
        self.runFor(20) # shouldn't terminate
        for i in randlist:
            self.failUnless(self.outDest.recv("inbox") == i)
            self.failUnless(self.outDest.recv("control") == i + 1)
            self.failUnless(self.outDest.recv("extraout") == i + 2)
    def test_shutdown1(self):
        self.inSrc.send(shutdownMicroprocess(), "signal")
        self.failUnlessRaises(StopIteration, self.runFor, iterations = 10)
        self.failUnless(isinstance(self.outDest.recv("control"), shutdownMicroprocess)) # pass through the shutdown code
    def test_shutdown2(self):
        self.inSrc.send(producerFinished(), "signal")
        self.failUnlessRaises(StopIteration, self.runFor, iterations = 10)
        self.failUnless(isinstance(self.outDest.recv("control"), producerFinished)) # pass through the shutdown code


class test_LikeFile(unittest.TestCase):
    def setUp(self):
        self.numthreads = threading.activeCount()
        self.numcomponents = len(Axon.Scheduler.scheduler.run.threads)

    def tearDown(self):
        # the small timeout is necessary, since the shutdown signal is sent before
        # likefile has returned, and if we check immediately then it might not have died yet.
        time.sleep(0.5)
        self.failUnless(self.numcomponents == len(Axon.Scheduler.scheduler.run.threads))
        self.failUnless(self.numthreads == threading.activeCount())
        ## make sure also that creating then killing a likefile doesn't leave any crufty extra threads or extra scheduler entries.

    def test_nop(self):
        """Test that creating, activating, and deleting a wrapped component doesn't fail."""
        self.component = LikeFile(DyingShunt())
        self.component.activate()
        time.sleep(0.25) # I think this might be a threading issue - the instant shutdown is not being processed.
        self.component.shutdown()
        del self.component

    def testmany(self):
        compdict = dict()
        for i in xrange(1, 100): # test 100 concurrent likefiles.
            compdict[i] = LikeFile(DyingShunt(), extrainboxes = "extrain", extraoutboxes = "extraout")
            compdict[i].activate()
        time.sleep(0.1)
        for num, component in compdict.iteritems():
            for i in randlist:
                # i is a random integer between 0 and 1, so the following manipulations guarantee that each box on each
                # component gets a different number, to eliminate crosstalk passing a test.
                component.send(num + i, "inbox")
                component.send(num + i % 0.5, "control")
                component.send(num + i % 0.25, "extrain")
        for num, component in compdict.iteritems():
            for i in randlist:
                self.failUnless(component.recv("outbox") == num + i)
                self.failUnless(component.recv("signal") == num + i % 0.5)
                self.failUnless(component.recv("extraout") == num + i % 0.25)
        for component in compdict.itervalues():
            component.shutdown()

    def test_aborted(self):
        """test that creating but not activating a likefile wrapper doesn't leave any cruft in the scheduler,
        and that you can't perform IO on a pre-activated component."""
        component = LikeFile(DyingShunt())
        self.failUnlessRaises(AttributeError, component.recv)
        self.failUnlessRaises(AttributeError, component.send, "boo")
    def test_badboxwrap(self):
        """test that wrapping a nonexistent box will fail."""
        self.failUnlessRaises(KeyError, LikeFile, DyingShunt(), extrainboxes = "nonsenseaddbox")
        self.failUnlessRaises(KeyError, LikeFile, DyingShunt(), extraoutboxes = "nonsenseaddbox")
    def test_badboxuse(self):
        """test that IO on a box name that doesn't exist will fail."""
        component = LikeFile(DyingShunt())
        component.activate()
        self.failUnlessRaises(KeyError, component.send, "boo", "nonsensesendbox")
        self.failUnlessRaises(KeyError, component.recv, "nonsensesendbox")
        component.shutdown()
    def test_closed(self):
        """test that creating, activating, and then closing a likefile wrapper will result in an object you're not
        allowed to perform IO on."""
        component = LikeFile(DyingShunt())
        component.activate()
        time.sleep(0.1)
        component.shutdown()
        time.sleep(0.1)
        self.failUnlessRaises(AttributeError, component.recv)
        self.failUnlessRaises(AttributeError, component.send, "boo")



if __name__ == "__main__":
    unittest.main()
    import sys
    sys.tracebacklimit = 0
    # if the interpreter exits with active threads, this spams the console and pushes anything useful off the top of the page.