#!/usr/bin/env python
#
# (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# test suite for GetHostByName

from dns import GetHostByName
import Axon, unittest, time, socket, md5, warnings
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Dummy(Axon.Component.component):
    def main(self):
        while 1:
            yield 1

class Test_GetHostByName(unittest.TestCase):

    def setUp(self):
        self.scheduler = Axon.Scheduler.scheduler()
        Axon.Scheduler.scheduler.run = self.scheduler

    def setup_tests(self, lookupargs = None):
        self.lookup = GetHostByName(lookupargs).activate(Scheduler = self.scheduler)
        self.inSrc = Dummy()
        self.inSrc.link((self.inSrc,"outbox"), (self.lookup,"inbox"))
        self.inSrc.link((self.inSrc,"signal"), (self.lookup,"control"))
        self.outDest = Dummy()
        self.outDest.link((self.lookup,"outbox"), (self.outDest,"inbox"))
        self.outDest.link((self.lookup,"signal"), (self.outDest,"control"))
        self.run = self.scheduler.main()

    def tearDown(self):
        del self.run, self.outDest, self.inSrc, self.lookup, self.scheduler
        # these aren't created in self.setUp so be sure to always call setup_tests manually.

    def sendToInbox(self,data):
        self.inSrc.send(data,"outbox")
    def sendToControl(self,data):
        self.inSrc.send(data,"signal")
    def dataReadyOutbox(self):
        return self.outDest.dataReady("inbox")
    def dataReadySignal(self):
        return self.outDest.dataReady("control")
    def dataReadyAny(self):
        return self.outDest.anyReady()
    def recvOutbox(self):
        return self.outDest.recv("inbox")
    def recvSignal(self):
        return self.outDest.recv("control")

    def runUntil(self, timeout = 1):
        """Runs the scheduler until the lookup component emits a message of some description"""
        thetime = time.time()
        while not self.dataReadyAny():
            self.run.next()
            if time.time() > thetime + timeout:
                self.fail("timeout reached")


    def compareLookup(self, hostname, fail = False):
        """Compares a direct call to gethostbyname() with the result of a 
        previously-inserted call to the component which has now processed
        it. set fail to True or False to determine whether the lookup 
        should fail or work, or any other value (such as None) to test 
        indiscriminately"""
        try: 
            result = socket.gethostbyname(hostname)
            self.failUnless(self.recvOutbox() == (hostname, result))
            if fail == True: self.fail("hostname %s resolvable!" % hostname)
        except socket.gaierror, e:
            self.failUnless(self.recvSignal() == (hostname, e[1]))
            if fail == False: warnings.warn("%s expected to be resolvable, isn't. Perhaps you are offline? Tests may not be comprehensive." % hostname) #self.fail("hostname %s not resolvable!" % hostname)

    def checkStop(self, stopped):
        """Checks to make sure that the lookup component has ended when we think it should."""
        time.sleep(0.01) # let the thread have a chance to die.
        try:
            for i in xrange(0, 100):
                self.run.next()
        except StopIteration: pass # if the scheduler is over, then everything is stopped.
        self.failUnless(self.lookup._isStopped() == stopped)

    def testLinearSucceed(self):
        """A non-existent hostname lookup will fail sanely."""
        self.setup_tests()
        hostname = "slashdot.org"
        self.sendToInbox(hostname)
        self.runUntil()
        self.compareLookup(hostname, fail = False)
        self.failUnless(not self.lookup._isStopped()) # should still be active
        self.checkStop(stopped = False)

    def testLinearFail(self):
        """A hostname lookup will succeed sanely."""
        self.setup_tests()
        hostname = "Q" + md5.new("slashdot.org").hexdigest() # this is not likely to be a valid hostname
        self.sendToInbox(hostname)
        self.runUntil()
        self.compareLookup(hostname, fail = True)
        self.checkStop(stopped = False)

    def testLinearShutdown(self):
        """A producerFinished() shutdown signal will be handled properly."""
        self.setup_tests()
        self.sendToControl(producerFinished())
        self.runUntil()
        self.failUnless(isinstance(self.recvSignal(), producerFinished))
        self.checkStop(stopped = True)

    def testLinearShutdown2(self):
        """A shutdownMicroprocess() shutdown signal will be handled properly."""
        self.setup_tests()
        self.sendToControl(shutdownMicroprocess())
        self.runUntil()
        self.failUnless(isinstance(self.recvSignal(), producerFinished))
        self.checkStop(stopped = True)

    def testLinearTypicalUsage(self):
        self.setup_tests()
        """A typical usage pattern is tested. 10 or 15 sequential lookups, some to the same host, some of which fail."""
        hostlist = ["slashdot.org", "kamaelia.sourceforge.net", "bbc.co.uk", "bbc.co.uk", 
        "somehostnamethatimadeupinthehopeitfails.co", "192.168.0.1",
        "♖♘♗♕♔♗♘♖"] # now it's just getting silly
        for host in hostlist:
            self.sendToInbox(host)
        for host in hostlist:
            self.runUntil()
            self.compareLookup(host, fail = None) # either win or lose, doesn't matter, what matters is consistency

    def OneShot(self, hostname, fail = False):
        self.setup_tests(hostname)
        self.runUntil()
        self.compareLookup(hostname, fail)
        self.failUnless(self.dataReadySignal) # the mandatory immediate shutdown is also present
        self.failUnless(isinstance(self.recvSignal(), producerFinished))
        self.checkStop(stopped = True)

    def testOneShotFail(self):
        """A non-existent hostname lookup will fail sanely - one-shot version."""
        self.OneShot("Q" + md5.new("slashdot.org").hexdigest(), fail = True) # this is an unlikely hostname
    def testOneShotSucceed(self):
        """A hostname lookup will succeed sanely - one-shot version."""
        self.OneShot("slashdot.org", fail = False)

    


if __name__ == "__main__":
    unittest.main()