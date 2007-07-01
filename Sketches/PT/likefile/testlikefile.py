#!/usr/bin/env python

from likefile import LikeFile, schedulerThread
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
import unittest, random, Axon, threading, time

scheduler = schedulerThread(slowmo=0.001)
scheduler.start()


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
        self.randlist = [random.random() for x in xrange(0, 10)]
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
        for i in self.randlist:
            self.inSrc.send(i, "outbox")
            self.inSrc.send(i + 1, "signal")
            self.inSrc.send(i + 2, "extrain")
        self.runFor(20) # shouldn't terminate
        for i in self.randlist:
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


class test_LikeFileClosure(unittest.TestCase):
    def build(self):
        self.component = LikeFile(DyingShunt())
        self.component.activate()
        time.sleep(0.1)

    def collapse(self):
        self.component.shutdown()
        del self.component

    def test_setup_shutdown(self):
        """a test to make sure that there's no cruft left in a scheduler from the passing existence of
        a likefile, assuming the wrapped component honours shutdown messages."""
        numthreads, numcomponents = threading.activeCount, len(Axon.Scheduler.scheduler.run.threads)
        self.build()
        self.collapse()
        time.sleep(0.1)
        self.failUnless(numcomponents == len(Axon.Scheduler.scheduler.run.threads))

if __name__ == "__main__":
    unittest.main()