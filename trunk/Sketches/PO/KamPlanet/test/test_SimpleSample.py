#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*-*- encoding: utf-8 -*-*-
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
# Licensed to the BBC under a Contributor Agreement: PO

from Axon.Ipc import producerFinished
import Kamaelia.Testing.KamTestCase as KamTestCase
import Kamaelia.Testing.KamExpectMatcher as KamExpectMatcher
from SimpleSample import SimpleComponent

class SimpleSampleTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        self.simpleSample = SimpleComponent()
        self.initializeSystem(self.simpleSample)
        
    def testForwardsNumbers(self):
        self.put(5, 'numbers')
        self.put(6, 'numbers')
        self.put(producerFinished(), 'control')
        self.assertEquals('5', self.get('outbox'))
        self.assertEquals('6', self.get('outbox'))
        self.assertOutboxEmpty('outbox')
        self.assertTrue(isinstance(self.get('signal'), producerFinished))
        self.assertOutboxEmpty('signal')
        
    def testForwardsNumbersWithExpect(self):
        self.put(5, 'numbers')
        self.put(6, 'numbers')
        self.put(7, 'numbers')
        self.put(producerFinished(), 'control')
        self.expect(KamExpectMatcher.RegexpMatcher('^6$'), 'outbox')
        self.assertEquals('7', self.get('outbox'))
        self.assertOutboxEmpty('outbox')
        self.assertTrue(isinstance(self.get('signal'), producerFinished))
        self.assertOutboxEmpty('signal')

def suite():
    return KamTestCase.makeSuite(
            SimpleSampleTestCase.getTestCase()
        )
        
if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
