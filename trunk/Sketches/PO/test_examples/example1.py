#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

########################################################################
#
# This is a very simple sample. In order to keep it simple, I write it
# all in the same file.
#
########################################################################
# This example only checks the output from a simple component
# 

import Axon
from Axon.Ipc import producerFinished

class SimpleComponent(Axon.Component.component):
    def main(self):
        self.send('msg1', 'outbox')
        yield 1
        self.send('msg2', 'outbox')
        yield 1
        self.send('msg3', 'outbox')
        yield 1
        self.send(producerFinished(self), 'signal')
        yield 1

# Import KamTestCase (this is subject to change)
import Kamaelia.Testing.KamTestCase as KamTestCase

# This is a TestCase. A TestCase contains multiple tests, and might contain
# some shared code for initialization and cleaning resources
class SimpleComponentTestCase(KamTestCase.KamTestCase):
    # This code will be executed BEFORE EACH test
    # It's not required, but it's very useful to initialize the component
    def setUp(self):
        # Instanciate the component under test
        self.simpleComponent = SimpleComponent()
        # Initialize the system
        self.initializeSystem(self.simpleComponent)
    
    # This code will be executed AFTER EACH test
    # It's also not required, but it's useful to release resources
    def tearDown(self):
        pass
        
    # Now, the tests. Every test is a method which starts by "test"
    def testRightBehaviour(self):
        # Let's wait for a message received from outbox, for a second
        dataReceived = self.get('outbox', timeout=1)
        # Now, since this is the first message, it must be 'msg1'
        self.assertEquals('msg1', dataReceived)
        # Let's wait for a message received from outbox, for two seconds
        dataReceived = self.get('outbox', timeout=2)
        # It must be 'msg2'
        self.assertEquals('msg2', dataReceived)
        # Let's wait for a message received from outbox, during the standard time
        dataReceived = self.get('outbox')
        # It must be 'msg3'
        self.assertEquals('msg3', dataReceived)
        # Let's wait for the signal
        dataReceived = self.get('signal')
        # It must inherit from Axon.IPC.producerFinished
        self.assertTrue(isinstance(dataReceived, producerFinished))
        # We check that nothing else is coming
        self.assertOutboxEmpty('control')
        self.assertOutboxEmpty('outbox')

# This method is not required, but it's useful to build a unittest-compatible
# TestSuite
def suite():
    # This is a classmethod which is present in all the KamTestCases. The
    # method returns a unittest-compatible TestCase, that will behave as
    # explained above, but through the standard unittest API. Thanks to this,
    # these tests can be integrated in any framework which relies on unittest,
    # so it may be easily integrated into software as apycot or CruiseControl, 
    # etc.
    unittestCompatibleTestCase = SimpleComponentTestCase.getTestCase()
    return KamTestCase.makeSuite(unittestCompatibleTestCase)

if __name__ == '__main__':
    # It will call suite() and execute that TestSuite
    KamTestCase.main(defaultTest='suite')
