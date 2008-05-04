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
            SimpleHTTPClient(),
            Feedparser()
        )

class FeedParserFactory(Axon.Component.component):
    Inboxes = {
        "inbox"         : "Information coming from the socket",
        "control"       : "From component...",
        "parsed-feeds"  : "Feedparser drops here the feeds" 
    }
    def __init__(self, **argd):
        super(FeedParserFactory, self).__init__(**argd)
        self.mustStop = None
        self.pleaseStop = None

    def checkControl(self): #taken from Carousel.py
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg,producerFinished):
                self.pleaseStop = msg
            elif isinstance(msg,shutdownMicroprocess):
                self.mustStop = msg
        return self.mustStop, self.pleaseStop

    def handleChildTerminations(self): #taken from Carousel.py
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)

    def main(self):
        while True:
            # TODO: make two states, just as in Carousel.py, to avoid new parsed-feeds
            # /inbox when pleaseStop != None
            mustStop, pleaseStop = self.checkControl()
            if mustStop:
                self.send(mustStop,"signal")
                return

            self.handleChildTerminations()

            while self.dataReady("inbox"):
                feed = self.recv("inbox")
                child = makeFeedParser(feed)
                self.link( (child, 'outbox'), (self, 'parsed-feeds') )
                self.addChildren(child)
                child.activate()
                yield 1

            while self.dataReady("parsed-feeds"):
                parseddata = self.recv("parsed-feeds")
                self.send(parseddata,"outbox")
                yield 1

            if pleaseStop and len(self.childComponents()) == 0:
                self.send(pleaseStop,"signal")
                return

            if not self.anyReady():
                self.pause()
            yield 1

