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
from HTTPParser import HTTPParser

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
    
class HTTPParser_Test(unittest.TestCase):
    """A set of tests for the HTTPParser class."""
    def test_smokeTest(self):
        """__init__ - Called with no arguments succeeds"""
        P = HTTPParser()
        self.assert_(isinstance(P, Axon.Component.component))
        
    def test_shutdownMessageCausesShutdown(self):
        """main - If the component recieves a shutdown() message, the component shuts down"""
        P = HTTPParser()
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
        P = HTTPParser()
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
    
    def test_validRequest(self):       
        P = HTTPParser()
        R = Recorder()
        R.link( (P, "outbox"), (R, "inbox"))
        R.activate()
        P.activate()
        P._deliver("HEAD http://localhost/temp.txt?wibble&foo=bar HTTP/1.1\r\nConnection: keep-alive\r\nHost: localhost\r\n\r\n", "inbox")
        componentExit = False
        for i in xrange(2000):
            if len(R.heard) > 0:
                break
            try:
                P.next()
                R.next()
            except StopIteration:
                pass
                
        if len(R.heard) == 0:
            self.fail("If the component receives a valid and complete HTTP request it should output a request object")
        else:
            requestobject = R.heard[0]
            if requestobject.get("uri-server","") != "localhost":
                self.fail("If the component receives a valid and complete HTTP request it should output a request object containing the correct uri-server item")
            elif requestobject.get("raw-uri","") != "/temp.txt?wibble&foo=bar":
                self.fail("If the component receives a valid and complete HTTP request it should output a request object containing the correct raw-uri item")
            elif requestobject.get("version","") != "1.1":
                self.fail("If the component receives a valid and complete HTTP request it should output a request object containing the correct version item")
            elif requestobject.get("bad",True) != False:
                self.fail("If the component receives a valid and complete HTTP request it should output a request object containing \"bad\":False")
        
    def test_incoherentRequest(self):
        """main - Non-HTTP requests are marked bad"""
        P = HTTPParser()
        R = Recorder()
        R.link( (P, "outbox"), (R, "inbox"))
        R.activate()
        P.activate()
        P._deliver("ecky\n\n\n\n", "inbox")
        componentExit = False
        for i in xrange(2000):
            if len(R.heard) > 0:
                break
            try:
                P.next()
                R.next()
            except StopIteration:
                pass
        if len(R.heard) == 0:
            self.fail("If the component receives non-HTTP requests it should send on a bad request message - none sent")
        elif not R.heard[0].get("bad",False):
            self.fail("If the component receives non-HTTP requests it should send on a bad request message")
                        
if __name__=='__main__':
   unittest.main()
