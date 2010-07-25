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
# This example interacts with the input and the output of a simple component
# skipping some messages
# 

import Axon
from Axon.Ipc import producerFinished

class SimpleComponent(Axon.Component.component):
    def main(self):
        while True:
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                # It sends it twice
                self.send(data, 'outbox')
                self.send(data, 'outbox')
                
            while self.dataReady('control'):
                data = self.recv('control')
                self.send(data, 'signal')
                return
            yield 1

import Kamaelia.Testing.KamTestCase as KamTestCase
import Kamaelia.Testing.KamExpectMatcher as KamExpectMatcher

class SimpleComponentTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        self.simpleComponent = SimpleComponent()
        self.initializeSystem(self.simpleComponent)
    
    def testRightBehaviour(self):
        # We put one message
        self.put('msg1', 'inbox')
        dataReceived = self.get('outbox', timeout=1)
        # We receive it twice
        self.assertEquals('msg1', dataReceived)
        dataReceived = self.get('outbox', timeout=1)
        self.assertEquals('msg1', dataReceived)
        # Then kill it
        msg = producerFinished()
        self.put(msg, 'control')
        dataReceived = self.get('signal')
        self.assertEquals(msg, dataReceived)
        self.assertOutboxEmpty('control')
        self.assertOutboxEmpty('outbox')
        
    def testSkipping(self):
        # We put one message
        self.put('msg1', 'inbox')
        # We put another message
        self.put('msg2', 'inbox')
        
        # We skip the 'msg1' messages that was sent, and we move to the first 'msg2' message
        self.expect(KamExpectMatcher.Matcher('msg2'),'outbox')
        
        # After it there should be another 'msg2' message:
        dataReceived = self.get('outbox', timeout=1)
        self.assertEquals('msg2', dataReceived)
        # Then kill it
        msg = producerFinished()
        self.put(msg, 'control')
        dataReceived = self.get('signal')
        self.assertEquals(msg, dataReceived)
        
        # And after it... nothing else
        self.assertOutboxEmpty('control')
        self.assertOutboxEmpty('outbox')
        
    def testSkippingWithRegex(self):
        # We put one message
        self.put('msg1', 'inbox')
        # We put another message
        self.put('msg2', 'inbox')
        
        # We skip the 'msg1' messages that was sent, and we move 
        # to the first message that is a str and ends with '2'
        self.expect(KamExpectMatcher.RegexpMatcher('.*2$'),'outbox')
        
        # After it there should be another 'msg2' message:
        dataReceived = self.get('outbox', timeout=1)
        self.assertEquals('msg2', dataReceived)
        # Then kill it
        msg = producerFinished()
        self.put(msg, 'control')
        dataReceived = self.get('signal')
        self.assertEquals(msg, dataReceived)
        
        # And after it... nothing else
        self.assertOutboxEmpty('control')
        self.assertOutboxEmpty('outbox')

def suite():
    return KamTestCase.makeSuite(SimpleComponentTestCase.getTestCase())

if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
