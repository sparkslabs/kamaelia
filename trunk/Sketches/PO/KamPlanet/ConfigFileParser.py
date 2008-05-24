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

import os

import Axon
from Axon.Ipc import producerFinished

from GeneralObjectParser import Field, GeneralObjectParser

def generateGeneralConfig():
    return GeneralObjectParser(
                name             = Field(str, 'Default name'), 
                link             = Field(str, 'http://default.link/'), 
                rssTemplateName  = Field(str, 'rss20.xml.tmpl'), 
                htmlTemplateName = Field(str, 'index.xml.tmpl'), 
                rssFileName      = Field(str, 'output%srss20.xml' % os.sep ), 
                htmlFileName     = Field(str, 'output%sindex.html' % os.sep ), 
                maxPostNumber    = Field(int, 10),
            )

def generateFeed():
    return GeneralObjectParser(
                url        = Field(str, 'http://default.url/'), 
                name       = Field(str, 'default name'), 
                face       = Field(str, 'image.jpg'), 
                faceWidth  = Field(str, '64'), 
                faceHeight = Field(str, '64'),
            )

class ConfigFileParser(Axon.Component.component):
    Outboxes = {
        "outbox"           : "Not used",
        "signal"           : "From component...",
        "feeds-outbox"     : "It will send one by one the parsed feeds. Instances of str by the moment",
        "config-outbox"    : "It will send an instance of GeneralConfig when parsed",
    }
    def __init__(self, **argd):
        super(ConfigFileParser, self).__init__(**argd)
        self.feeds = []
        self.config       = None
        self.finished     = False

        # Temporal variables, for xml parsing
        self.temp_config           = generateGeneralConfig()
        self.temp_feed             = None
        self.parsing_general       = False
        self.parsing_feed          = False
        self.parsing_feeds         = False
        self.parsing_general_field = None
        self.parsing_feed_field    = None

    def parsingXml(self, data):
        # Main XML skeleton
        if data[0] == '/document':
            self.finished = True
        elif data[0] == 'element' and data[1] == 'general':
            self.parsing_general = True
        elif data[0] == '/element' and data[1] == 'general':
            self.parsing_general = False
            self.config = self.temp_config.generateResultObject()
        elif data[0] == 'element' and data[1] == 'feeds':
            self.parsing_feeds = True
        elif data[0] == '/element' and data[1] == 'feeds':
            self.parsing_feeds = False
        
        # Parsing general head
        if self.parsing_general:
            if data[0] == 'element' and data[1] in self.temp_config.getFieldNames():
                self.parsing_general_field = data[1]
            elif data[0] == '/element' and data[1] in self.temp_config.getFieldNames():
                self.parsing_general_field = None
            
            if data[0] == 'chars' and self.parsing_general_field is not None:
                prev = getattr(self.temp_config,  self.parsing_general_field)
                prev.parsedValue = prev.parsedValue + data[1]
        
        # Parsing feeds
        if self.parsing_feeds:
            if data[0] == 'element' and data[1] == 'feed':
                self.parsing_feed = True
                self.temp_feed = generateFeed()                
                url = data[2].get('url')
                self.temp_feed.url.parsedValue = url
                
            elif data[0] == '/element' and data[1] == 'feed':
                self.parsing_feed = False
                self.feeds.append(self.temp_feed.generateResultObject())
            if self.parsing_feed:
                if data[0] == 'element' and data[1] in self.temp_feed.getFieldNames():
                    self.parsing_feed_field = data[1]
                elif data[0] == '/element' and data[1] in self.temp_feed.getFieldNames():
                    self.parsing_feed_field = None
                
                if data[0] == 'chars' and self.parsing_feed_field is not None:
                    prev = getattr(self.temp_feed,  self.parsing_feed_field)
                    prev.parsedValue = prev.parsedValue + data[1]
        
    def main(self):
        while True:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                self.parsingXml(data)

            # If the general config has been parsed, send it
            if self.config is not None:
                self.send(self.config,  'config-outbox')
                self.config = None
            
            # Send the parsed feeds
            while len(self.feeds) > 0:
                for feed in self.feeds:
                    self.send(feed,"feeds-outbox")
                self.feeds = []
            
            # If we're done, finish
            if self.finished:
                self.send(producerFinished(self), "signal")
                return
                
            if not self.anyReady():
                self.pause()
                
            yield 1
