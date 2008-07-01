#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
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
# Licensed to the BBC under a Contributor Agreement: PO

from Axon.Ipc import producerFinished
import kamtest.KamTestCase as KamTestCase
import kamtest.KamExpectMatcher as KamExpectMatcher
from SimpleSample import SimpleComponent

class SimpleSampleTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        print "setUp..."
        self.simpleSample = SimpleComponent()
        self.initializeSystem(self.simpleSample)
        
    def tearDown(self):
        print "tearDown..."
        
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
