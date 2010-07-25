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
        # This test fails because of a bug in 
        # Kamaelia.Protocol.HTTP.HTTPParser.HTTPParser.getBodyDependingOnHalfClose
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
    
    def test200withoutLengthAndWithoutClosingConnection(self):
        pass#TODO
    
    def testNoAnswer(self):
        # This test fails because of a bug in 
        # Kamaelia.Protocol.HTTP.HTTPParser.HTTPParser.getInitialLine
        # the self.shouldShutdown does not handle the fact that the 
        # provider might have finished, sending a producerFinished
        # message
        self.fakeHttpServer.stop()
        self.fakeHttpServer.join()
        # Now there is no server
        path = 'server.was.shutdown'
        p = Pipeline(
                OneShot('http://localhost:%i/%s' % (PORT, path)), 
                SimpleHTTPClient()
            )
        self.initializeSystem(p)
        signalMessage = self.get('signal', timeout=20)
        self.assertTrue(isinstance(signalMessage, producerFinished))
        # Is this actually correct?
        message       = self.get('outbox')
        self.assertEquals('', message)
        self.assertFinished()
        self.assertOutboxEmpty('outbox')
        self.assertOutboxEmpty('signal')
        
def suite():
    return KamTestCase.makeSuite(SimpleHTTPClientTestCase.getTestCase())

if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
