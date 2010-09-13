#! /usr/bin/python

# Interface to BBC /programmes JSON etc
# - Identifies PID of current programme on a chosen channel
# - Provides output for PIDs in a chosen format (XML, RDF etc)
# - Identifies currently playing tracks on radio channels

import cjson
import urllib2

from Axon.Component import component

from datetime import datetime
from dateutil.parser import parse

# Should probably combine these all into one component given the amount of similarity
# OR - create a generic requester component and link all of these to it (removing the urllib stuff)

class WhatsOn(component):
    Inboxes = ["inbox", "control"]
    Outboxes = ["outbox", "signal"]

    def __init__(self, proxy = False):
        super(WhatsOn, self).__init__()
        self.proxy = proxy
        self.channels = {"bbcone" : "/bbcone/programmes/schedules/london/today",
                "bbctwo" : "/bbctwo/programmes/schedules/england",
                "bbcthree" : "/bbcthree/programmes/schedules",
                "bbcfour" : "/bbcfour/programmes/schedules",
                "cbbcchannel" : "/cbbc/programmes/schedules",
                "cbeebies" :"/cbeebies/programmes/schedules",
                "bbcnews" : "/bbcnews/programmes/schedules",
                "radio1" : "/radio1/programmes/schedules/england",
                "radio2" : "/radio2/programmes/schedules",
                "radio3" : "/radio3/programmes/schedules",
                "radio4" : "/radio4/programmes/schedules/fm",
                "radio5" : "/5live/programmes/schedules"}

    def getCurrentProg(self, channel):
        scheduleurl = "http://www.bbc.co.uk" + self.channels[channel] + ".json"

        # Work out what's on NOW here
        utcdatetime = datetime.now()

        # Configure proxy and opener
        if self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})
            bbcopener = urllib2.build_opener(proxyhandler)
        else:
            bbcopener = urllib2.build_opener()

        # Get ready to grab BBC data
        urllib2.install_opener(bbcopener)
        headers = {'User-Agent' : "BBC R&D Grabber"}
        data = ""

        # Grab BBC data
        try:
            req = urllib2.Request(scheduleurl,data,headers)
            conn1 = urllib2.urlopen(req)
        except urllib2.URLError, e:
            conn1 = False
            print "URLError:", e.reason

        # Read and decode schedule
        if conn1:
            content = conn1.read()
            conn1.close()
            try:
                decodedcontent = cjson.decode(content)
            except cjson.DecodeError, e:
                print "cjson.DecodeError:", e.message

            # Analyse schedule
            if decodedcontent:
                for programme in decodedcontent['schedule']['day']['broadcasts']:
                    starttime = parse(programme['start'])
                    starttime = starttime.replace(tzinfo=None)
                    endtime = parse(programme['end'])
                    endtime = endtime.replace(tzinfo=None)
                    if (utcdatetime >= starttime) & (utcdatetime < endtime):
                        pid = programme['programme']['pid']
                        title =  programme['programme']['display_titles']['title']
                        return [pid,title]
                        break

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                channel = self.recv("inbox")
                data = self.getCurrentProg(channel)
                self.send(data,"outbox")
            self.pause()
            yield 1

class NowPlaying(component):
    Inboxes = ["inbox", "control"]
    Outboxes = ["outbox", "signal"]

    def __init__(self, proxy = False):
        super(NowPlaying, self).__init__()
        self.proxy = proxy
        self.channels = {"radio1" : "/radio1/nowplaying/latest"}

    def getCurrentTrack(self, channel):
        nowplayingurl = "http://www.bbc.co.uk" + self.channels[channel] + ".json"

        # Configure proxy and opener
        if self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})
            bbcopener = urllib2.build_opener(proxyhandler)
        else:
            bbcopener = urllib2.build_opener()

        # Get ready to grab BBC data
        urllib2.install_opener(bbcopener)
        headers = {'User-Agent' : "BBC R&D Grabber"}
        data = ""

        # Grab BBC data
        try:
            req = urllib2.Request(nowplayingurl,data,headers)
            conn1 = urllib2.urlopen(req)
        except urllib2.URLError, e:
            conn1 = False
            print "URLError:", e.reason

        # Read and decode now playing info
        if conn1:
            content = conn1.read()
            conn1.close()
            try:
                decodedcontent = cjson.decode(content)
            except cjson.DecodeError, e:
                print "cjson.DecodeError:", e.message

        # Analyse now playing info
        if decodedcontent:
            # Not finished! - now playing json file is empty if nothing is playing!
            return False

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                channel = self.recv("inbox")
                npdata = self.getCurrentTrack(channel)
                self.send(npdata,"outbox")
            self.pause()
            yield 1

class ProgrammeData(component):
    # NOTE: This component could be replaced by a generic HTTP content grabber provided it allows for proxies

    Inboxes = ["inbox", "control"]
    Outboxes = ["outbox", "signal"]

    def __init__(self, proxy = False):
        super(ProgrammeData, self).__init__()
        self.proxy = proxy
        self.programmesurl = "http://www.bbc.co.uk/programmes/"

    def getProgrammeData(self, pid, format):
        url = self.programmesurl + pid + "." + format

        # Configure proxy and opener
        if self.proxy:
            proxyhandler = urllib2.ProxyHandler({"http" : self.proxy})
            bbcopener = urllib2.build_opener(proxyhandler)
        else:
            bbcopener = urllib2.build_opener()

        # Get ready to grab BBC data
        urllib2.install_opener(bbcopener)
        headers = {'User-Agent' : "BBC R&D Grabber"}
        data = ""

        # Grab BBC data
        try:
            req = urllib2.Request(url,data,headers)
            conn1 = urllib2.urlopen(req)
        except urllib2.URLError, e:
            conn1 = False
            print "URLError:", e.reason

        # Read and return programme data
        if conn1:
            content = conn1.read()
            conn1.close()
            return content

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                request = self.recv("inbox")
                pid = request[0]
                format = request[1]
                progdata = self.getProgrammeData(pid,format)
                self.send(progdata,"outbox")
            self.pause()
            yield 1