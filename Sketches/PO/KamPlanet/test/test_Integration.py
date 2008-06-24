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

import kamtest.KamTestCase as KamTestCase

import KamPlanet

import FakeHttpServer
import os
import tempfile
import time

PORT=7779

TEST_CONFIG_TEMPLATE = 'test%sconfig-template.xml' % os.sep

PLANET_PYTHON_FEEDS_PATH   = '/feeds/planet.python/'
PLANET_KAMAELIA_FEEDS_PATH = '/feeds/kamaelia/'

VERBOSE = True

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
        
    def test10Feeds(self):
        self._testPlanetPythonFeeds(feeds=10, timeout=100)
            
    def test20Feeds(self):
        self._testPlanetPythonFeeds(feeds=20, timeout=100)
            
    def test30Feeds(self):
        self._testPlanetPythonFeeds(feeds=30, timeout=100)
            
    def test40Feeds(self):
        self._testPlanetPythonFeeds(feeds=40, timeout=100)
            
    def test50Feeds(self):
        self._testPlanetPythonFeeds(feeds=50, timeout=200)
            
    def test60Feeds(self):
        self._testPlanetPythonFeeds(feeds=60, timeout=400)

    def test100Feeds(self):
        self._testPlanetPythonFeeds(feeds=100, timeout=500)
            
    def tearDown(self):
        if VERBOSE:
            print "It took %s seconds" % (time.time() - self._startTime)
        self.fakeHttpServer.stop()
        self.fakeHttpServer.join()
    
def suite():
    return KamTestCase.makeSuite(IntegrationTestCase.getTestCase())

if __name__ == '__main__':
    KamTestCase.main()
