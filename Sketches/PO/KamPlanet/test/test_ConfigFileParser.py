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
    
