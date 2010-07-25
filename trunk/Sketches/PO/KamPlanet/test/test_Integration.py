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

import Kamaelia.Testing.KamTestCase as KamTestCase

import KamPlanet

import FakeHttpServer
import os
import tempfile
import time

PORT=7779

TEST_CONFIG_TEMPLATE = 'test%sconfig-template.xml' % os.sep

PLANET_PYTHON_FEEDS_PATH   = '/feeds/planet.python/'
PLANET_KAMAELIA_FEEDS_PATH = '/feeds/kamaelia/'

VERBOSE = False

# First approach
class IntegrationTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        self.fakeHttpServer = FakeHttpServer.FakeHttpServer(PORT)
        self.fakeHttpServer.start()
        self.fakeHttpServer.waitUntilHandling()
        self._startTime = time.time()
        
    def _configureFeeds(self):
        responses = {}
        for i in range(100):
            pathName = PLANET_PYTHON_FEEDS_PATH  + 'feed%s.xml' % i
            fileName = 'feeds%sfeed%s.xml' % (os.sep, i)
            responses[pathName] = dict(
                body = open(fileName).read(), 
                contentType = 'text/xml', 
                code = 200
            )
        for i in range(6):
            pathName = PLANET_KAMAELIA_FEEDS_PATH + 'feed%s.xml' % i
            fileName = 'feeds%skamaelia_feed%s.xml' % (os.sep, i)
            responses[pathName] = dict(
                body = open(fileName).read(), 
                contentType = 'text/xml', 
                code = 200
            )
        self.fakeHttpServer.setResponses(responses)
    
    def _createConfiguration(self, numberOfFeeds, path):
        feeds = []
        for i in range(numberOfFeeds):
            feeds.append("""<feed url="%s">
                    <name>Blog number %s</name>
                    </feed>
                """ % (
                       'http://localhost:%s%sfeed%s.xml' % (PORT, path, i), 
                       i
                    )
            )
        return open(TEST_CONFIG_TEMPLATE).read() % {
                        'FEEDS' : ''.join(feeds)
                    }
                    
    def testKamaeliaFeeds(self):
        self._configureFeeds()
        configuration = self._createConfiguration(6, PLANET_KAMAELIA_FEEDS_PATH)
        fd, name = tempfile.mkstemp()
        os.close(fd)
        try:
            open(name, 'w').write(configuration)
            kamPlanet = KamPlanet.KamPlanet(name)
            kamPlanet.start()
            self.initializeSystem(kamPlanet.component)
            self.assertFinished(timeout=30)
        finally:
            os.remove(name)
        
    def _testPlanetPythonFeeds(self, feeds, timeout):
        if VERBOSE:
            import introspector
            introspector.activate()
        self._configureFeeds()
        configuration = self._createConfiguration(feeds, PLANET_PYTHON_FEEDS_PATH)
        fd, name = tempfile.mkstemp()
        os.close(fd)
        try:
            open(name, 'w').write(configuration)
            kamPlanet = KamPlanet.KamPlanet(name)
            kamPlanet.start()
            self.initializeSystem(kamPlanet.component)
            self.assertFinished(timeout=timeout)
        finally:
            os.remove(name)
            
    def test0Feeds(self):
        self._testPlanetPythonFeeds(feeds=0, timeout=100)
        
    def test1Feeds(self):
        self._testPlanetPythonFeeds(feeds=1, timeout=100)
        
#    def test10Feeds(self):
#        self._testPlanetPythonFeeds(feeds=10, timeout=100)
#            
#    def test20Feeds(self):
#        self._testPlanetPythonFeeds(feeds=20, timeout=100)
#            
#    def test30Feeds(self):
#        self._testPlanetPythonFeeds(feeds=30, timeout=100)
#            
#    def test40Feeds(self):
#        self._testPlanetPythonFeeds(feeds=40, timeout=100)
#            
#    def test50Feeds(self):
#        self._testPlanetPythonFeeds(feeds=50, timeout=200)
            
    def test60Feeds(self):
        self._testPlanetPythonFeeds(feeds=60, timeout=400)

#    def test100Feeds(self):
#        self._testPlanetPythonFeeds(feeds=100, timeout=500)
            
    def tearDown(self):
        if VERBOSE:
            print "It took %s seconds" % (time.time() - self._startTime)
        self.fakeHttpServer.stop()
        self.fakeHttpServer.join()
    
def suite():
    return KamTestCase.makeSuite(IntegrationTestCase.getTestCase())

if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
