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
from KamTestCase                  import KamTestCase

import PostSorter
import ConfigFileParser

import feedparser
import time

# Still a lot needs to be tested, this is just a proof of concept
class PostSorterTestCase(KamTestCase):
    
    def setUp(self):
        self.postSorter = PostSorter.PostSorter()
        self.initializeSystem(self.postSorter,  self.postSorter)

    def createConfigObject(self,  maxNumber):
        class AnonymousClass(object):
            def __init__(self, **argd):
                super(AnonymousClass, self).__init__()
                self.__dict__.update(argd)
        return AnonymousClass(
                maxPostNumber = maxNumber
            )
            
    def generate100feeds(self):
        feeds = []
        for i in xrange(100):
            feeds.append(
                feedparser.FeedParserDict(
                    feed     = 'feed%i' % i, 
                    encoding = 'UTF-8',
                    entries = [feedparser.FeedParserDict(
                        updated_parsed = time.gmtime()
                    )]
                )
            )
        return feeds

    def testMax1feed(self):
        configObject = self.createConfigObject(1)
        self.messageAdder.addMessage(configObject, 'config-inbox')
        feeds = self.generate100feeds()
        for feed in feeds:
            self.messageAdder.addMessage(feed, 'inbox')
        self.messageAdder.addMessage(producerFinished(), "control")
        self.runMessageExchange()
        storedMessages = self.messageStorer.getMessages("outbox")
        self.assertEquals(
                    1, 
                    len(storedMessages)
                )
                
    def testMax10feeds(self):
        configObject = self.createConfigObject(10)
        self.messageAdder.addMessage(configObject, 'config-inbox')
        feeds = self.generate100feeds()
        for feed in feeds:
            self.messageAdder.addMessage(feed, 'inbox')
        self.messageAdder.addMessage(producerFinished(), "control")
        self.runMessageExchange()
        storedMessages = self.messageStorer.getMessages("outbox")
        self.assertEquals(
                    10, 
                    len(storedMessages)
                )
    
if __name__ == '__main__':
    import unittest
    unittest.main()
