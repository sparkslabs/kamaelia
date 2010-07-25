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
from Kamaelia.XML.SimpleXMLParser import SimpleXMLParser

import Kamaelia.Testing.KamTestCase as KamTestCase

import ConfigFileParser

class ConfigFileParserTestCase(KamTestCase.KamTestCase):
    SAMPLE_CONFIG1 = """<?xml version="1.0" encoding="UTF-8"?>
            <kamplanetconfig>
                <general>
                    <name>Kamaelia Planet</name>
                    <link>http://somewhere/</link>
                    <rssTemplateName>rss20.xml.tmpl</rssTemplateName>
                    <htmlTemplateName>index.html.tmpl</htmlTemplateName>
                    <rssFileName>output/rss20.xml</rssFileName>

                    <htmlFileName>output/index.html</htmlFileName>
                    <maxPostNumber>30</maxPostNumber>
                </general>
                <feeds>
                    <feed url="http://localhost/blog1">
                        <name>blog1</name>
                    </feed>
                    <feed url="http://localhost/blog2">
                        <name>blog2</name>
                        <face>imgs/blog2.png</face>
                        <faceHeight>12345</faceHeight>
                        <faceWidth>54321</faceWidth>
                    </feed>
                </feeds>
            </kamplanetconfig>
        """
    
    def setUp(self):
        self.xmlParser        = SimpleXMLParser()
        self.configFileParser = ConfigFileParser.ConfigFileParser()
        
        self.xmlParser.link((self.xmlParser, 'outbox'), (self.configFileParser, 'inbox'))
        self.xmlParser.link((self.xmlParser, 'signal'), (self.configFileParser, 'control'))
        
        self.initializeSystem(self.xmlParser,  self.configFileParser)
    
    def runWithSampleConfig(self, sampleConfig):
        self.put(sampleConfig, 'inbox')
        self.put(producerFinished(), "control")
        
    def testSampleConfigNotStopping(self):
        self.put(self.SAMPLE_CONFIG1, 'inbox')
        # I actively say that I don't care which threads are still running
        self.assertNotFinished()
        
    def testSignal(self):
        self.runWithSampleConfig(self.SAMPLE_CONFIG1)
        
        signalMsg      = self.get('signal')
        self.assertTrue(
            isinstance(
                       signalMsg, 
                       producerFinished
            )
        )
        self.assertTrue(
            self.configFileParser, 
            signalMsg.caller
        )
        self.assertOutboxEmpty('signal')
    
    def testGeneralConfig(self):
        self.runWithSampleConfig(self.SAMPLE_CONFIG1)
        configMsg = self.get('config-outbox')
        self.assertEquals('Kamaelia Planet', configMsg.name)
        self.assertOutboxEmpty('config-outbox')
        
    def testFeedsOutbox(self):
        self.runWithSampleConfig(self.SAMPLE_CONFIG1)
        firstFeedMessage = self.get('feeds-outbox')
        self.assertEquals("http://localhost/blog1", firstFeedMessage.url )
        self.assertEquals("blog1",                  firstFeedMessage.name )
        self.assertEquals(
                    ConfigFileParser.DEFAULT_FACE_HEIGHT,
                    firstFeedMessage.faceHeight
                )
        self.assertEquals(
                    ConfigFileParser.DEFAULT_FACE_WIDTH,
                    firstFeedMessage.faceWidth 
                )
        self.assertEquals(
                    ConfigFileParser.DEFAULT_FACE,
                    firstFeedMessage.face
                )
        
        secondFeedMessage = self.get('feeds-outbox')
        self.assertEquals("http://localhost/blog2", secondFeedMessage.url )
        self.assertEquals("blog2",                  secondFeedMessage.name )
        self.assertEquals(
                    '12345',
                    secondFeedMessage.faceHeight
                )
        self.assertEquals(
                    '54321',
                    secondFeedMessage.faceWidth 
                )
        self.assertEquals(
                    'imgs/blog2.png',
                    secondFeedMessage.face
                )
        self.assertOutboxEmpty('feeds-outbox')
        
def suite():
    return KamTestCase.makeSuite(ConfigFileParserTestCase.getTestCase())
    
if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
    
