#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
import feedparser
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.OneShot import OneShot
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Feedparser(Axon.Component.component):
    def main(self):
        while True:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                parseddata = feedparser.parse(data)
                self.send(parseddata, "outbox")

            while self.dataReady("control"):
                data = self.recv("control")
                self.send(data,"signal")
                return

            if not self.anyReady():
                self.pause()
            yield 1

def makeFeedParser(feedUrl):
    return Pipeline(
            OneShot(feedUrl), 
            SimpleHTTPClient(), #TODO: SimpleHTTPClient doesn't seem to have proxy support
            Feedparser()
        )

# TODO: write a pool in order to avoid too many concurrent petitions
class FeedParserFactory(Axon.Component.component):
    Inboxes = {
        "inbox"          : "Information coming from the socket",
        "control"        : "From component...",
        "_parsed-feeds"  : "Feedparser drops here the feeds", 
    }
    Outboxes = {
        "outbox"         : "From component...", 
        "signal"         : "From component...", 
    }
    def __init__(self, **argd):
        super(FeedParserFactory, self).__init__(**argd)
        self.mustStop         = None
        self.providerFinished = False

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

    def main(self):
        while True:
            mustStop, providerFinished = self.checkControl()
            if mustStop:
                self.send(mustStop,"signal")
                # TODO: should I send this message to my children?
                # Yes, but first I need a PlugSplitter in order to connect
                # my "_signal" to many "control"s. The problem is that 
                # creating that PlugSplitter I would need another treatment
                # for the "if providerFinished and len(self.childComponents()) == 0"
                # block. In the next commit...
                return
            
            self.handleChildTerminations()
            
            while self.dataReady("inbox"):
                feed = self.recv("inbox")
                child = makeFeedParser(feed.url)
                self.link( (child, 'outbox'), (self, '_parsed-feeds') )
                self.addChildren(child)
                child.activate()
            
            while self.dataReady("_parsed-feeds"):
                parseddata = self.recv("_parsed-feeds")
                self.send(parseddata,"outbox")
            
            if providerFinished and len(self.childComponents()) == 0:
                self.send(producerFinished(self),"signal")
                return
            
            if not self.anyReady():
                self.pause()
            yield 1

