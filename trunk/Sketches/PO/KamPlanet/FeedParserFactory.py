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

import Axon
import feedparser
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Splitter import Plug, PlugSplitter
from Kamaelia.Util.OneShot import OneShot
from Axon.Ipc import producerFinished, shutdownMicroprocess

from ForwarderComponent import Forwarder

SAVE = 'pickle'

if SAVE == 'pickle':
    import pickle
    FILENAME = 'feeds-control.tmp'
    def reset():
        pickle.dump({}, open(FILENAME, 'w'))
        
    def started(url):
        data = pickle.load(open(FILENAME))
        data[url] = 'started'
        pickle.dump(data, open(FILENAME, 'w'))
        
    def stopped(url):
        data = pickle.load(open(FILENAME))
        data[url] = 'stopped'
        pickle.dump(data, open(FILENAME, 'w'))

    reset()
else:
    def started(url):
        pass
    def stopped(url):
        pass

class Feedparser(Axon.Component.component):
    """
    Feedparser(feedUrl) -> Feedparser object
    
    It receives the content of a feed and sends the parsed 
    content. The parsed content is in a feedparser.FeedParserDict 
    object. It sets the 'href' attribute to the feedUrl.
    """
    def __init__(self, feedUrl):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Feedparser, self).__init__()
        self.feedUrl = feedUrl
        
    def main(self):
        while True:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                parseddata = feedparser.parse(data)
                parseddata.href = self.feedUrl
                if parseddata.has_key('bozo_exception'):
                    self.send(producerFinished(self),"signal")
                    stopped(self.feedUrl)
                    return
                else:
                    self.send(parseddata, "outbox")
                    self.send(producerFinished(self),"signal")
                    stopped(self.feedUrl)
                    return
            
            if self.dataReady("control"):
                data = self.recv("control")
                self.send(data,"signal")
                if not isinstance(data, producerFinished):
                    print data
                stopped(self.feedUrl)
                return

            if not self.anyReady():
                self.pause()
            yield 1

class FeedParserFactory(Axon.Component.component):
    """
    FeedParserFactory() -> FeedParserFactory object
    
    It receives different feed URLs throught the "inbox" inbox 
    and returns each post parsed through the "outbox" outbox.
    
    This class can handles multiple concurrent petitions, retrieves
    the content of the feed and parses it with the feedparser library.
    The result is a feedparser.FeedParserDict per each feed URL 
    provided.
    """
    Inboxes = {
        "inbox"          : "Strings representing different URLs of feeds",
        "control"        : "From component...",
        "_parsed-feeds"  : "Parsed feeds retrieved from FeedParserFactory children", 
    }
    Outboxes = {
        "outbox"         : "feedparser.FeedParserDict object representing a parsed feed", 
        "signal"         : "From component...", 
        "_signal"        : "To the internal parsers",
    }
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(FeedParserFactory, self).__init__(**argd)
        self.mustStop         = None
        self.providerFinished = False

    def makeFeedParser(self, feedUrl):
        """ 
        makeFeedParser(feedUrl) -> Pipeline
        
        It returns a pipeline which does not expect any input except for signals and
        sends the parsed data through the "outbox" outbox.
        """
        started(feedUrl)
        return Pipeline(
                OneShot(feedUrl), 
                SimpleHTTPClient(), # TODO: SimpleHTTPClient doesn't seem to have proxy support
            )
            
    def checkControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg,producerFinished):
                self.providerFinished = True
            elif isinstance(msg,shutdownMicroprocess):
                self.mustStop = msg
        return self.mustStop, self.providerFinished
        
    def handleChildTerminations(self): #taken from Carousel.py
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)
                
    def initiateInternalSplitter(self):
        self.internalSplitter = PlugSplitter()
        self.link((self,'_signal'), (self.internalSplitter, 'control'))
        self.addChildren(self.internalSplitter)
        self.internalSplitter.activate()
        
    def linkChildToInternalSplitter(self, child):
        forwarder = Forwarder()
        plug = Plug(self.internalSplitter,  forwarder)
        plug.activate()
        plug.link((plug, 'signal'), (child, 'control'))
        child.link((child, 'signal'), (plug, 'control'))
        
    def createChild(self, feed):
        child = self.makeFeedParser(feed.url)
        child = Pipeline(child, Feedparser(feed.url))
        self.link( (child, 'outbox'), (self, '_parsed-feeds') )
        self.linkChildToInternalSplitter(child)
        return child
        
    def waitForChildren(self, signalMessage):
        self.send(signalMessage,"_signal")
        while len(self.childComponents()) > 0:
            self.handleChildTerminations()
            yield 1
        
    def main(self):
        self.initiateInternalSplitter()
        yield 1
        
        while True:
            mustStop, providerFinished = self.checkControl()
            if mustStop:
                self.send(mustStop,"signal")
                return
            
            self.handleChildTerminations()
            
            while self.dataReady("inbox"):
                feed = self.recv("inbox")
                child = self.createChild(feed)
                self.addChildren(child)
                child.activate()
                
            while self.dataReady("_parsed-feeds"):
                parseddata = self.recv("_parsed-feeds")
                self.send(parseddata,"outbox")
                
            if providerFinished and len(self.childComponents()) == 1:
                # TODO: CHECK IF THIS IS THE PROBLEM
                # It's actually only waiting for the plugsplitter
                for _ in self.waitForChildren(producerFinished(self)):
                    yield 1
                pfinished = producerFinished(self)
                self.send(pfinished,"signal")
                return
                
            if not self.anyReady():
                self.pause()
            yield 1
            
