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

from Kamaelia.Util.OneShot import OneShot
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient

import FakeHttpServer
PORT=7779

class SimpleHTTPClientTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        self.fakeHttpServer = FakeHttpServer.FakeHttpServer(PORT)
        self.fakeHttpServer.start()
        self.fakeHttpServer.waitUntilHandling()
        
    def tearDown(self):
        self.fakeHttpServer.stop()
        self.fakeHttpServer.join()
        
    def _test200response(self, body, timeout):
        responses = {}
        path = 'foo'
        responses['/' + path] = dict(
                    body = body, 
                    contentType = 'text', 
                    code = 200, 
                )
        self.fakeHttpServer.setResponses(responses)
        p = Pipeline(
                OneShot('http://localhost:%i/%s' % (PORT, path)), 
                SimpleHTTPClient()
            )
        self.initializeSystem(p)
        self.assertEquals(body, self.get('outbox', timeout=timeout) )
        signalMessage = self.get('signal')
        self.assertTrue(isinstance(signalMessage, producerFinished))
        self.assertFinished()
        self.assertOutboxEmpty('outbox')
        self.assertOutboxEmpty('signal')
        
    def test_small200response(self):
        self._test200response('bar', 30)

    def test_big200response(self):
        size = 50 * 1024 * 1024 # 50 MB
        self._test200response('0' * size, 100)
    
    def test_302response(self):
        responses = {}
        oldpath = 'old.addr'
        oldbody = 'nothing to see here'
        newpath = 'new.addr'
        newbody = 'found me!'
        responses['/' + oldpath] = dict(
                    body = oldbody, 
                    code = 302,
                    locationAddr = 'http://localhost:%i/%s' % (PORT, newpath)
                )
        responses['/' + newpath] = dict(
                    body = newbody, 
                    code = 200, 
                )
        self.fakeHttpServer.setResponses(responses)
        
        p = Pipeline(
                OneShot('http://localhost:%i/%s' % (PORT, oldpath)), 
                SimpleHTTPClient()
            )
        self.initializeSystem(p) 
        self.assertEquals(newbody, self.get('outbox', timeout=30))
        signalMessage = self.get('signal')
        self.assertTrue(isinstance(signalMessage, producerFinished))
        self.assertFinished()
        self.assertOutboxEmpty('outbox')
        self.assertOutboxEmpty('signal')
        
    def test404response(self):
        responses = {}
        path = 'not.found'
        body = '404 not found'
        responses['/' + path] = dict(
                    body = body, 
                    contentType = 'text', 
                    code = 404, 
                )
        self.fakeHttpServer.setResponses(responses)
        p = Pipeline(
                OneShot('http://localhost:%i/%s' % (PORT, path)), 
                SimpleHTTPClient()
            )
        self.initializeSystem(p)
        self.assertEquals(body, self.get('outbox', timeout=30))
        signalMessage = self.get('signal')
        self.assertTrue(isinstance(signalMessage, producerFinished))
        self.assertFinished()
        self.assertOutboxEmpty('outbox')
        self.assertOutboxEmpty('signal')
        
    def test200withoutLength(self):
        responses = {}
        path = 'foo'
        body = 'whatever'
        path = 'without.length'
        responses['/' + path] = dict(
                    body = body, 
                    contentType = 'text', 
                    code = 200, 
                    dontProvideLength = True, 
                )
        self.fakeHttpServer.setResponses(responses)
        p = Pipeline(
                OneShot('http://localhost:%i/%s' % (PORT, path)), 
                SimpleHTTPClient()
            )
        self.initializeSystem(p)
        self.assertEquals(body, self.get('outbox', timeout=30) )
        signalMessage = self.get('signal')
        self.assertTrue(isinstance(signalMessage, producerFinished))
        self.assertFinished()
        self.assertOutboxEmpty('outbox')
        self.assertOutboxEmpty('signal')
        
def suite():
    return KamTestCase.makeSuite(SimpleHTTPClientTestCase.getTestCase())

if __name__ == '__main__':
    KamTestCase.main()
