#!/usr/bin/env python
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
#
# test suite for graphline

import unittest

from Kamaelia.Chassis.Graphline import Graphline

from Axon.Component import component
from Axon.Scheduler import scheduler
from Axon.Ipc import producerFinished, shutdownMicroprocess


class MockChild(component):

    def __init__(self):
        super(MockChild,self).__init__()
        self._stopNow = False
        self.wasActivated=False

    def stopNow(self):
        self._stopNow = True
        
    def main(self):
        self.wasActivated=True
        while not self._stopNow:
            yield 1


class Test_Graphline(unittest.TestCase):

    def setup_initialise(self,*listargs,**dictargs):
        self.children = {}
        for key in dictargs.keys():
            if key != "linkages":
                self.children[key] = dictargs[key]
        
        self.scheduler = scheduler()
        scheduler.run = self.scheduler

        self.graphline = Graphline(*listargs, **dictargs)
        
        self.run = self.scheduler.main()

    def setup_activate(self):
        self.graphline.activate(Scheduler=self.scheduler)
        
    def runFor(self, cycles):
        numcycles=cycles*(3+len(self.children))    # approx this many components in the system
        for i in range(0,numcycles): self.run.next()




    def test_smokeTest(self):
        """Instantiating a graphline with no arguments results in a ValueError exception"""
        self.failUnlessRaises(ValueError, Graphline)
        
        
    def test_graphlineNoLinkagesArg(self):
        """Instantiating with components as named arguments, but specifying no linkages argument results in a ValueError exception"""
        self.failUnlessRaises(ValueError, Graphline, A=component(), B=component())


    def test_graphlineEmptyLinkagesArg(self):
        """Instantiating with components as named arguments, and specifying an empty linkages argument succeeds"""
        Graphline(A=component(), B=component(), linkages={})


    def test_graphlineNoComponentsEmptyLinkagesArg(self):
        """Instantiating with no components as named arguments, and specifying an empty linkages argument succeeds"""
        Graphline(linkages={})


    def test_graphlineHasChildren(self):
        """Instantiating a graphline, components specified as named arguments, eg. A=component() and B=component() become children of the graphline once activated and run."""
        self.setup_initialise(A=component(), B=component(), linkages={})
        self.setup_activate()
        
        self.runFor(cycles=1)
        
        gChildren = self.graphline.childComponents()
        for c in self.children.values():
            self.assertTrue(c in gChildren)
        
        
    def test_unactivatedGraphlineHasNoChildren(self):
        """Instantiating a graphline, components specified as named arguments, eg. A=component() and B=component() will not be children of the graphline before it is activated and run"""
        self.setup_initialise(A=component(), B=component(), linkages={})
        
        gChildren = self.graphline.childComponents()
        for c in self.children.values():
            self.assertFalse(c in gChildren)
        

    def test_activatesChildrenOnlyWhenActivated(self):
        """Children are activated as soon as the Graphline itself is activated, but no sooner."""
        self.setup_initialise(A=MockChild(), B=MockChild(), C=MockChild(), linkages={})

        for child in self.children.values():
            self.assertFalse(child.wasActivated)

        self.setup_activate()
        self.runFor(cycles=1)
        self.runFor(cycles=3)
        
        for child in self.children.values():
            self.assertTrue(child.wasActivated)
        
        
    def test_linkagesBetweenComponents(self):
        """A linkage from "outbox" to "inbox" between two named child components "A" and "B" can be specified by specifying a "linkages" argument containing a dictionary with an entry: ("A","outbox"):("B","inbox"). Data sent to A's "outbox"  will reach B's "inbox"."""
        A=MockChild()
        B=MockChild()
        self.setup_initialise(A=A, B=B, linkages={("A","outbox"):("B","inbox")})

        self.setup_activate()
        self.runFor(cycles=1)

        DATA=object()
        A.send(DATA,"outbox")        
        self.runFor(cycles=1)
        
        self.assertTrue(B.dataReady("inbox"))
        self.assertEquals(DATA, B.recv("inbox"))
        
        
if __name__ == "__main__":
    unittest.main()
    

