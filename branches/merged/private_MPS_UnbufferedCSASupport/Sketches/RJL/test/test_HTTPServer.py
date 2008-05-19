#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

# Test the module loads
import unittest

import Axon
import Axon.Scheduler as Scheduler
from Axon.Ipc import shutdown
from HTTPServer import HTTPServer

class Recorder(Axon.Component.component):
    def __init__(self):
        super(Recorder, self).__init__()
        self.heard = []
        
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                temp = self.recv("inbox")
                #print temp
                self.heard.append(temp)
            
            while self.dataReady("control"):
                temp = self.recv("control")
    
class HTTPServer_Test(unittest.TestCase):
    """A set of tests for the HTTPServer class."""
        
    def test_SmokeTest(self):
        """__init__ - Called with no arguments succeeds"""
        P = HTTPServer()
        self.assert_(isinstance(P, Axon.Component.component))
        
    def test_shutdownMessageCausesShutdown(self):
        """main - If the component recieves a shutdown() message, the component shuts down"""
        P = HTTPServer()
        P.activate()

        P._deliver(shutdown(), "control")

        componentExit = False
        for i in xrange(2000):
            try:
                P.next()
            except StopIteration:
                componentExit = True
                break
        if not componentExit:
            self.fail("When sent a shutdown message, the component should shutdown")
            
    def test_shouldPause(self):
        """main - If the component receives no input it pauses"""
        P = HTTPServer()
        P.activate()

        componentExit = False
        for i in xrange(2000):
            if not P._isRunnable():
                break
            try:
                P.next()
            except StopIteration:
                componentExit = True
                break
        if componentExit or P._isRunnable():
            self.fail("If the component receives no input it should pause rather than busywait")        
if __name__=='__main__':
   unittest.main()
