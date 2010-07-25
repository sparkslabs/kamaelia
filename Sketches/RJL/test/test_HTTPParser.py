#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
