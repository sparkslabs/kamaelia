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

from Axon.Ipc import producerFinished, shutdownMicroprocess

import Kamaelia.Testing.KamTestCase as KamTestCase

import ForwarderComponent

class ForwarderComponentTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        self.forwarderComponent = ForwarderComponent.Forwarder()
        self.initializeSystem(self.forwarderComponent)
        
    def testSimpleUse(self):
        self.put("message1", 'inbox')
        self.put("message2", 'inbox')
        self.put("message3", 'inbox')
        self.put("message4", 'inbox')
        producerFinishedObj = producerFinished()
        self.put(producerFinishedObj, "control")
        # The following message will not be considered since the component has already finished
        self.put(producerFinishedObj, "control")
        for i in xrange(4):
            expected = "message%s" % (i + 1)
            actual   = self.get('outbox')
            self.assertEquals(expected, actual, "Failed on i = %s: <%s> != <%s>" % (i, expected, actual))
        self.assertOutboxEmpty('outbox')
            
        self.assertEquals(producerFinishedObj, self.get('signal'))
        self.assertOutboxEmpty('signal')

    def testSimpleSecondaryUse(self):
        self.put("message1", 'secondary-inbox')
        self.put("message2", 'secondary-inbox')
        self.put("message3", 'secondary-inbox')
        self.put("message4", 'secondary-inbox')
        producerFinishedObj = producerFinished()
        self.put(producerFinishedObj, "secondary-control")
        # The following message will not be considered since the component has already finished
        self.put(producerFinishedObj, "secondary-control")
        for i in xrange(4):
            expected = "message%s" % (i + 1)
            actual   = self.get('outbox')
            self.assertEquals(expected, actual, "Failed on i = %s: <%s> != <%s>" % (i, expected, actual))
        self.assertOutboxEmpty('outbox')
        self.assertEquals(producerFinishedObj, self.get('signal'))
        self.assertOutboxEmpty('signal')
    
    def testSimpleMixedUse(self):
        # Take into account that the yields are necessary, since the
        # Forwarder component can't ensure the order among messages received in
        # two different inboxes
        self.put("message1", 'inbox')
        self.put("message2", 'inbox')
        
        actual   = self.get('outbox')
        self.assertEquals("message1", actual)
        actual   = self.get('outbox')
        self.assertEquals("message2", actual)
        
        self.put("message3", 'secondary-inbox')
        self.put("message4", 'secondary-inbox')
        
        actual   = self.get('outbox')
        self.assertEquals("message3", actual)
        actual   = self.get('outbox')
        self.assertEquals("message4", actual)
        
        self.put("message5", 'inbox')
        
        actual   = self.get('outbox')
        self.assertEquals("message5", actual)
        
        self.put("message6", 'secondary-inbox')
        
        actual   = self.get('outbox')
        self.assertEquals("message6", actual)
        
        self.put("message7", 'inbox')
        
        actual   = self.get('outbox')
        self.assertEquals("message7", actual)
        
        producerFinishedObj = producerFinished()
        self.put(producerFinishedObj, "control")
        
        actual   = self.get('signal')
        self.assertEquals(producerFinishedObj, actual)
        
        self.assertOutboxEmpty('outbox')
        self.assertOutboxEmpty('signal')

def suite():
    return KamTestCase.makeSuite(ForwarderComponentTestCase.getTestCase())
    
if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
