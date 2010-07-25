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
