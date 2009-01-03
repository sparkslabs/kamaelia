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

import Kamaelia.Testing.KamTestCase as KamTestCase
import PostSorter
import ConfigFileParser

import feedparser
import time

# Still a lot needs to be tested, this is just a proof of concept
class PostSorterTestCase(KamTestCase.KamTestCase):
    
    def setUp(self):
        self.postSorter = PostSorter.PostSorter()
        self.initializeSystem(self.postSorter)

    def createConfigObject(self,  maxNumber):
        class AnonymousClass(object):
            def __init__(self, **argd):
                super(AnonymousClass, self).__init__()
                self.__dict__.update(argd)
        return AnonymousClass(
                maxPostNumber = maxNumber
            )
    
    NO_DATE = object()
    
    def generateFeeds(self, number, date = None, name = 'feed'):
        feeds = []
        for i in xrange(number):
            if date is None:
                date = time.gmtime()
            
            if date == self.NO_DATE:
                entries = [feedparser.FeedParserDict()]
            else:
                entries = [feedparser.FeedParserDict(
                        updated_parsed = date
                    )]
                    
            feeds.append(
                feedparser.FeedParserDict(
                    feed     = '%s-%i' % (name, i), 
                    encoding = 'UTF-8',
                    entries  = entries
                )
            )
        return feeds
        
    def generate100feeds(self):
        return self.generateFeeds(100)
    
    def testMax1feed(self):
        # Max: 1 feed
        # Provided: 100 feeds
        configObject = self.createConfigObject(1)
        self.put(configObject, 'config-inbox')
        feeds = self.generate100feeds()
        for feed in feeds:
            self.put(feed, 'inbox')
        self.put(producerFinished(), "control")
        _ = self.get('outbox')
        self.assertOutboxEmpty('outbox')
    
    def testTooFewFeeds(self):
        # Max: 200 feeds
        # Provided: 100 feeds
        configObject = self.createConfigObject(200)
        self.put(configObject, 'config-inbox')
        feeds = self.generate100feeds()
        for feed in feeds:
            self.put(feed, 'inbox')
        self.put(producerFinished(), "control")
        for _ in xrange(100):
            self.get('outbox')
        self.assertOutboxEmpty('outbox')
                
    def testMax10feeds(self):
        # Max: 10 feeds
        # Provided: 100 feeds
        configObject = self.createConfigObject(10)
        self.put(configObject, 'config-inbox')
        feeds = self.generate100feeds()
        for feed in feeds:
            self.put(feed, 'inbox')
        self.put(producerFinished(), "control")
        for _ in xrange(10):
            self.get('outbox')
        self.assertOutboxEmpty('outbox')
        
    def testOrder(self):
        feeds = []
        the_date        = time.gmtime()
        cur_year        = the_date[0]
        # One year after
        the_future_date = (cur_year + 1, ) + the_date[1:]
        # One year before
        the_past_date   = (cur_year - 1, ) + the_date[1:]
        
        feeds.extend(self.generateFeeds(2, self.NO_DATE,    'notime'))
        feeds.extend(self.generateFeeds(2, the_future_date, 'future'))
        feeds.extend(self.generateFeeds(2, the_past_date,   'past'))
        feeds.extend(self.generateFeeds(2, the_date,        'present'))
        feeds.extend(self.generateFeeds(2, self.NO_DATE,    'notime'))
        
        configObject = self.createConfigObject(10)
        self.put(configObject, 'config-inbox')
        
        for feed in feeds:
            self.put(feed, 'inbox')
        self.put(producerFinished(), "control")
        for _ in range(2):
            msg = self.get('outbox')
            self.assertEquals(cur_year + 1, msg['entry']['updated_parsed'][0])
        for _ in range(2):
            msg = self.get('outbox')
            self.assertEquals(cur_year    , msg['entry']['updated_parsed'][0])
        for _ in range(2):
            msg = self.get('outbox')
            self.assertEquals(cur_year - 1, msg['entry']['updated_parsed'][0])
        for _ in range(4):
            msg = self.get('outbox')
            self.assertFalse(msg['entry'].has_key('updated_parsed'))
        self.assertOutboxEmpty('outbox')

    def testFilterOrder(self):
        feeds = []
        the_date        = time.gmtime()
        cur_year        = the_date[0]
        # One year after
        the_future_date = (cur_year + 1, ) + the_date[1:]
        # One year before
        the_past_date   = (cur_year - 1, ) + the_date[1:]
        
        feeds.extend(self.generateFeeds(2, self.NO_DATE,    'notime'))
        feeds.extend(self.generateFeeds(2, the_future_date, 'future'))
        feeds.extend(self.generateFeeds(2, the_past_date,   'past'))
        feeds.extend(self.generateFeeds(2, the_date,        'present'))
        feeds.extend(self.generateFeeds(2, self.NO_DATE,    'notime'))
        
        configObject = self.createConfigObject(5)
        self.put(configObject, 'config-inbox')
        
        for feed in feeds:
            self.put(feed, 'inbox')
        self.put(producerFinished(), "control")
        for _ in range(2):
            msg = self.get('outbox')
            self.assertEquals(cur_year + 1, msg['entry']['updated_parsed'][0])
        for _ in range(2):
            msg = self.get('outbox')
            self.assertEquals(cur_year    , msg['entry']['updated_parsed'][0])
        for _ in range(1):
            msg = self.get('outbox')
            self.assertEquals(cur_year - 1, msg['entry']['updated_parsed'][0])
        self.assertOutboxEmpty('outbox')

def suite():
    return KamTestCase.makeSuite(PostSorterTestCase.getTestCase())

if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
