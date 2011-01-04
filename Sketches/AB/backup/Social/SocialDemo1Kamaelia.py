#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
#

#import Axon
import os
import cjson
#import urllib
import urllib2
import string

from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
#from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess

from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline

# Class for word freq analysis
class WordFreqAnalysis(component):
    Inboxes = ["inbox", "control"]
    Outboxes = ["outbox", "signal"]

    def __init__(self, useexclusions = False):
        super(WordFreqAnalysis, self).__init__()
        self.exclusions = ["a","able","about","across","after","all","almost","also","am",\
                        "among","an","and","any","are","as","at","be","because","been","but",\
                        "by","can","cannot","could","dear","did","do","does","either","else",\
                        "ever","every","for","from","get","got","had","has","have","he","her",\
                        "hers","him","his","how","however","i","if","in","into","is","it",\
                        "its","just","least","let","like","likely","may","me","might","most",\
                        "must","my","neither","no","nor","not","of","off","often","on","only",\
                        "or","other","our","own","rather","said","say","says","she","should",\
                        "since","so","some","than","that","the","their","them","then","there",\
                        "these","they","this","tis","to","too","twas","us","wants","was","we",\
                        "were","what","when","where","which","while","who","whom","why","will",\
                        "with","would","yet","you","your"]
        self.useexclusions = useexclusions

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                text = self.recv("inbox")
                text = string.lower(text)
                # Remove punctuation
                for items in """!"#$%&()*+,-./:;<=>?@[\\]?_'`{|}?""":
                    text = string.replace(text,items,"")
                    words = string.split(text)
                # Remove common words (if requested)
                if self.useexclusions:
                    for word in words:
                        if word not in self.exclusions:
                            filteredwords = word
                    # Use 'filteredwords' from here
                    counts = {}
                    for word in filteredwords:
                        try:
                            counts[w] = counts[w] + 1
                        except KeyError:
                            counts[w] = 1
                else:
                    # Use 'words' from here
                    for word in words:
                        try:
                            counts[w] = counts[w] + 1
                        except KeyError:
                            counts[w] = 1

                self.send(counts,"outbox")

            self.pause()
            yield 1


# Class for sourcing data (or streams of data) from URLs with or without a proxy
class GrabDataFromURI(threadedcomponent):
    Inboxes = ["inbox", "control"]
    Outboxes = ["outbox", "data", "signal"]

    def __init__(self, uri, stream = False, proxy = False, username = False, password = False, post = False):
        super(GrabDataFromURI, self).__init__()
        self.uri = uri
        self.stream = stream
        self.proxy = proxy
        self.username = username
        self.password = password
        self.post= post

    def main(self):
        # Configure proxy
        if self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})

        # Configure authentication
        if self.username & self.password:
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, self.uri, self.username, self.password)
            authhandler = urllib2.HTTPBasicAuthHandler(passman)

        if proxyhandler & authhandler:
            opener = urllib2.build_opener(proxyhandler, authhandler)
        elif proxyhandler:
            opener = urllib2.build_opener(proxyhandler)
        elif authhandler:
            opener = urllib2.build_opener(authhandler)
        else:
            opener = urllib2.build_opener()

        urllib2.install_opener(opener)

        while 1:
            # Get stuff!
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                if data == "connect":
                    try:
                        if self.post:
                            self.conn = urllib2.urlopen(self.uri,self.post)
                        else:
                            self.conn = urllib2.urlopen(self.uri)
                        self.send("success","outbox")
                    except URLError, e:
                        self.send(e.reason,"outbox")
                elif data == "read":
                    if self.conn:
                        if stream:
                            try:
                                content = self.conn.readline()
                                self.send(content,"data")
                                self.send("dataready","outbox")
                            except Exception, e: #FIXME
                                self.send("disconnected","outbox")
                        else:
                            try:
                                content = self.conn.read()
                                self.send(content,"data")
                                self.send("dataready","outbox")
                            except Exception, e: #FIXME
                                self.send("disconnected","outbox")
                    else:
                        self.send("disconnected","outbox")
                elif data == "disconnect":
                    try:
                        self.conn.close()
                        self.send("disconnected","outbox")
                    except Exception, e:
                        self.send("disconnected","outbox")
                        
            self.pause() # erm, will this work?

class DataProcessor(component):
    Inboxes = ["inbox", "control", "scheduleInStatus", "scheduleInData", "twitterInStatus", "twitterInData", "fromAnalysis"]
    Outboxes = ["outbox", "signal", "scheduleOut", "twitterOut", "toAnalysis", "dataOut"]

    def __init__(self):
        super(DataProcessor, self).__init__()
        self.starttime = False
        self.endtime = False
        self.pid = False

    def getCurrentShow(self):
        # This is far from done
        if self.starttime & self.endtime:
            utcdatetime = datetime.now()
            if (utcdatetime >= self.starttime) & (utcdatetime < self.endtime):
                # Program is currently on, return its pid
                return pid
            elif (utcdatetime > self.endtime):
                pass
                # Program finished, get the next one
        else:
            self.send("connect","scheduleOut")
            self.send("read","scheduleOut")

    def main(self):
        while 1:
            #TODO: Actually write this - although most of it can be copied from the existing version
            # Should probably look in more detail about what needs to be split off for concurrency too - stream reading is already though so that should help
            self.pause()
            yield 1


if __name__=="__main__":
    # Do stuff
    # Load Config
    try:
        homedir = os.path.expanduser("~")
        file = open(homedir + "/twitter-login.conf")
    except IOError, e:
        print ("Failed to load login data - exiting")
        sys.exit(0)

    raw_config = file.read()
    file.close()

    # Read Config
    config = cjson.decode(raw_config)
    username = config['username']
    password = config['password']

    # Set up URLs
    twitterurl = "http://stream.twitter.com/1/statuses/filter.json"
    scheduleurl = "http://www.bbc.co.uk/radio1/programmes/schedules/england.json"
    #scheduleurl = "http://www.bbc.co.uk/bbcone/programmes/schedules/north_west/today.json"
    #scheduleurl = "http://www.bbc.co.uk/bbctwo/programmes/schedules/england/today.json"

    postdata = {'track' : 'bbcr1' + "," + 'scott_mills' + "," + 'scottmills' + "," + 'radio1' + "," + 'radio 1'}
    #postdata = XXXXX # TODO

    system = Graphline(DATAPROCESSOR = DataProcessor(),
                       BBCGRABBER = GrabDataFromURI(uri = scheduleurl, proxy = config['proxy']),
                       TWITGRABBER = GrabDataFromURI(uri = twitterurl,stream = True,username = username, password = password, proxy = config['proxy'], post = postdata),
                       ANALYSIS = WordFreqAnalysis(),
                       CONSOLE = ConsoleEchoer(),
                       linkages = {(DATAPROCESSOR, "scheduleOut") : (BBCGRABBER, "inbox"),
                                   (BBCGRABBER, "outbox") : (DATAPROCESSOR, "scheduleInStatus"),
                                   (BBCGRABBER, "data") : (DATAPROCESSOR, "scheduleInData"),

                                   (DATAPROCESSOR, "twitterOut") : (TWITGRABBER, "inbox"),
                                   (TWITGRABBER, "outbox") : (DATAPROCESSOR, "twitterInStatus"),
                                   (TWITGRABBER, "data") : (DATAPROCESSOR, "twitterInData"),

                                   (DATAPROCESSOR, "toAnalysis") : (ANALYSIS, "inbox"),
                                   (ANALYSIS, "outbox") : (DATAPROCESSOR, "fromAnalysis"),
                                   
                                   (DATAPROCESSOR, "dataOut") : (CONSOLE, "inbox")},
                          ).run()

