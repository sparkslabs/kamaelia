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

import KamTestCase

import KamTemplateProcessor
import ConfigFileParser

import feedparser

DUMMY_TEMPLATE = 'dummy.tmpl'

PLANET_NAME      = 'planet name'

FEED_URL   = "http://sample.feed/"

BLOG_TITLE       = "Blog title"
BLOG_LINK        = "http://blog.link/"
BLOG_DESCRIPTION = "blog description"
BLOG_DATE        = "Sat, 10 May 2008 18:25:53 +0000"
POST_TITLE       = "Post title"
POST_LINK        = "http://link.sample"
POST_DATE        = "Mon, 28 Apr 2008 18:16:45 +0000"
POST_CREATOR     = "Author name"
POST_GID         = "http://permalink/"
POST_DESCRIPTION = "Post description"
SAMPLE_RSS = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" 
        xmlns:content="http://purl.org/rss/1.0/modules/content/"
        xmlns:wfw="http://wellformedweb.org/CommentAPI/"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        >
        <channel>
            <title>%(BLOG_TITLE)s</title>
            <link>%(BLOG_LINK)s</link>
            <description>%(BLOG_DESCRIPTION)s</description>
            <pubDate>%(BLOG_DATE)s</pubDate>

            <generator>http://wordpress.org/?v=2.0.12-alpha</generator>
            <language>en</language>
            <item>
                <title>%(POST_TITLE)s</title>
                <link>%(POST_LINK)s</link>
                <pubDate>%(POST_DATE)s</pubDate>
                <dc:creator>%(POST_CREATOR)s</dc:creator>
                <guid isPermaLink="false">%(POST_GID)s</guid>
                <description><![CDATA[%(POST_DESCRIPTION)s]]></description>
            </item>
        </channel>
    </rss>""" % {
        "BLOG_TITLE"       : BLOG_TITLE, 
        "BLOG_LINK"        : BLOG_LINK, 
        "BLOG_DESCRIPTION" : BLOG_DESCRIPTION, 
        "BLOG_DATE"        : BLOG_DATE, 
        "POST_TITLE"       : POST_TITLE, 
        "POST_LINK"        : POST_LINK, 
        "POST_DATE"        : POST_DATE, 
        "POST_CREATOR"     : POST_CREATOR, 
        "POST_GID"         : POST_GID, 
        "POST_DESCRIPTION" : POST_DESCRIPTION,
    }

class KamTemplateProcessorTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        self.kamTemplateProcessor = KamTemplateProcessor.KamTemplateProcessor(
                                    'htmlTemplateName',
                                    'htmlFileName'
                                )
        self.kamTemplateProcessor.VERBOSE = False
        self.initializeSystem(self.kamTemplateProcessor)
    
    def testShutdown(self):
        shutdownMicroprocessObj = shutdownMicroprocess()
        self.messageAdder.addMessage(shutdownMicroprocessObj, 'control')
        self.assertStopping()
        messages = self.messageStorer.getMessages('signal')
        self.assertEquals(1, len(messages))
        self.assertEquals(shutdownMicroprocessObj, messages[0])
    
    def generateConfigObj(self):
        conf = ConfigFileParser.generateGeneralConfigObject()
        conf.htmlTemplateName.parsedValue += DUMMY_TEMPLATE
        conf.maxPostNumber.parsedValue    += '10'
        conf.name.parsedValue             += PLANET_NAME
        return conf.generateResultObject()
    
    def generateFeedObj(self, feedUrl):
        feed = ConfigFileParser.generateFeed()
        feed.url.parsedValue += feedUrl
        return feed.generateResultObject()
    
    # TODO: this is too simple, test what happens when config or control messages
    # come before all posts or sth like that
    def testSimpleUse(self):
        feedparsed = feedparser.parse(SAMPLE_RSS)
        feedparsed.href = FEED_URL
        self.messageAdder.addMessage(feedparsed, 'feeds-inbox')
        
        entry = { 
                 'feed'     : feedparsed.feed, 
                 'entry'    : feedparsed.entries[0], 
                 'encoding' : feedparsed.encoding, 
            }
        self.messageAdder.addMessage(entry, 'posts-inbox')
        
        channel = self.generateFeedObj(FEED_URL)
        self.messageAdder.addMessage(channel, 'channels-inbox')
        
        self.messageAdder.addYield(50)
        
        configObj = self.generateConfigObj()
        self.messageAdder.addMessage(configObj, 'config-inbox')
        
        self.messageAdder.addYield(50)
        
        self.messageAdder.addMessage(producerFinished(), 'control')
        self.assertStopping()
        
        messages = self.messageStorer.getMessages('signal')
        self.assertEquals(1, len(messages))
        self.assertTrue(isinstance(messages[0], producerFinished))
        
        messages = self.messageStorer.getMessages('create-output')
        self.assertEquals(1, len(messages))
        self.assertEquals(configObj.htmlFileName, messages[0])
        
        messages = self.messageStorer.getMessages('outbox')
        self.assertEquals(1, len(messages))
        output = messages[0]
        outputlines = [line.strip() for line in output.split('\n') if line.strip() != '']
        
        #print outputlines
        ptr = 0
        self.assertEquals(PLANET_NAME, outputlines[ptr])
        ptr += 1
        self.assertTrue(outputlines[ptr].lower().startswith('kamplanet'))
        ptr += 1
        self.assertEquals("rss20.xml", outputlines[ptr])
        ptr += 1
        self.assertEquals(PLANET_NAME, outputlines[ptr])
        ptr += 1
        self.assertEquals("rss", outputlines[ptr])
        ptr += 1
        self.assertEquals(POST_LINK, outputlines[ptr])
        #etc. (TODO)

def suite():
    return KamTestCase.makeSuite(KamTemplateProcessorTestCase)
    
if __name__ == '__main__':
    KamTestCase.main()
