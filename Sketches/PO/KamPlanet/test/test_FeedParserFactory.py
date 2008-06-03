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

from Axon.Ipc                  import producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Pipeline import pipeline

import pmock

import KamTestCase
import KamMockObject
import FeedParserFactory

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
    
class FeedParserTestCase(KamTestCase.KamTestCase):     
    def setUp(self):
        self.feedParser = FeedParserFactory.Feedparser(FEED_URL)
        self.initializeSystem(self.feedParser)
        
    def testFeedparser(self):
        self.messageAdder.addMessage(SAMPLE_RSS, 'inbox')
        self.messageAdder.addMessage(producerFinished(), 'control')
        self.runMessageExchange()
        
        messages = self.messageStorer.getMessages("outbox")
        self.assertEquals(1, len(messages))
        msg = messages[0]
        
        # Just check that the feedparser object works as expected
        self.assertEquals(BLOG_TITLE,        msg.feed.title)
        self.assertEquals(BLOG_LINK,         msg.feed.link)
        self.assertEquals(BLOG_DESCRIPTION,  msg.feed.subtitle)
        self.assertEquals(BLOG_DATE,         msg.feed.updated)
        
        self.assertEquals(1, len(msg.entries))
        self.assertEquals(POST_TITLE,        msg.entries[0].title)
        self.assertEquals(POST_LINK,         msg.entries[0].link)
        self.assertEquals(POST_DATE,         msg.entries[0].date)
        self.assertEquals(POST_CREATOR,      msg.entries[0].author)
        self.assertEquals(POST_GID,          msg.entries[0].id)
        self.assertEquals(POST_DESCRIPTION,  msg.entries[0].description)
        
class WrappedFeedParserFactory(FeedParserFactory.FeedParserFactory):
    def __init__(self, mockedFeedParserMaker, *argv,  **kwargv):
        super(WrappedFeedParserFactory, self).__init__(*argv, **kwargv)
        self.__mockedFeedParserMaker = mockedFeedParserMaker
        
    def makeFeedParser(self,  feedUrl):
        self.__mockedFeedParserMaker.makeFeedParser(feedUrl)
        
class FeedParserFactoryTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        self.mockedFeedParser = pmock.Mock()
        self.feedParserFactory = WrappedFeedParserFactory(self.mockedFeedParser)
        self.initializeSystem(self.feedParserFactory)
    
    def testNoFeedProducerFinished(self):
        self.messageAdder.addMessage(producerFinished(), 'control')
        self.runMessageExchange()
        messages = self.messageStorer.getMessages("signal")
        self.assertEquals(1, len(messages))
        self.assertTrue(isinstance(messages[0], producerFinished))
        
    def testNoFeedShutdown(self):
        self.messageAdder.addMessage(shutdownMicroprocess(), 'control')
        self.runMessageExchange()
        messages = self.messageStorer.getMessages("signal")
        self.assertEquals(1, len(messages))
        self.assertTrue(isinstance(messages[0], shutdownMicroprocess))
        
    def test1Feed(self):
        mockFeedParser = KamMockObject.KamMockObject(pipeline).activate()
        mockFeedParser.stopMockObject(100) #TODO
        #TODO : not added the feed
        self.messageAdder.addMessage(producerFinished(), 'control')
        self.runMessageExchange()
        
def suite():
    return KamTestCase.TestSuite((
                KamTestCase.makeSuite(FeedParserTestCase), 
                KamTestCase.makeSuite(FeedParserFactoryTestCase), 
            ))

if __name__ == '__main__':
    KamTestCase.main()
