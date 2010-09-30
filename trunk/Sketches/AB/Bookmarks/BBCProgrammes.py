#! /usr/bin/python

# Interface to BBC /programmes JSON etc
# - Identifies PID of current programme on a chosen channel
# - Provides output for PIDs in a chosen format (XML, RDF etc)
# - Identifies currently playing tracks on radio channels TODO

import cjson
import urllib2
import urllib
import httplib

from Axon.Component import component

from datetime import datetime, tzinfo, timedelta
from dateutil.parser import parse
from time import time, mktime
import pytz
import time as sleeper

# Should probably combine these all into one component given the amount of similarity
# OR - create a generic requester component and link all of these to it (removing the urllib stuff)

class GMT(tzinfo):
    def utcoffset(self,dt):
        return timedelta(hours=0,minutes=0)
    def tzname(self,dt):
        return "GMT"
    def dst(self,dt):
        return timedelta(0)

class WhatsOn(component):
    Inboxes = {
        "inbox" : "Receives a channel name to investigate in the 'key' format from self.channels",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "If a channel is on air, sends out programme info [pid,title,timeoffset,duration,expectedstarttime]",
        "signal" : ""
    }

    def __init__(self, proxy = False):
        super(WhatsOn, self).__init__()
        self.proxy = proxy
        # Define channel schedule URLs and DVB bridge channel formats
        self.channels = {"bbcone" : ["bbc one", "/bbcone/programmes/schedules/north_west/today"],
                "bbctwo" : ["bbc two", "/bbctwo/programmes/schedules/england"],
                "bbcthree" : ["bbc three", "/bbcthree/programmes/schedules"],
                "bbcfour" : ["bbc four", "/bbcfour/programmes/schedules"],
                "cbbc" : ["cbbc channel", "/cbbc/programmes/schedules"],
                "cbeebies" : ["cbeebies", "/cbeebies/programmes/schedules"],
                "bbcnews" : ["bbc news", "/bbcnews/programmes/schedules"],
                "radio1" : ["bbc radio 1", "/radio1/programmes/schedules/england"],
                "radio2" : ["bbc radio 2", "/radio2/programmes/schedules"],
                "radio3" : ["bbc radio 3", "/radio3/programmes/schedules"],
                "radio4" : ["bbc radio 4", "/radio4/programmes/schedules/fm"],
                "5live" : ["bbc r5l", "/5live/programmes/schedules"],
                "worldservice" : ["bbc world sv.", "/worldservice/programmes/schedules"],
                "6music" : ["bbc 6 music", "/6music/programmes/schedules"],
                "radio7" : ["bbc radio 7", "/radio7/programmes/schedules"],
                "1xtra" : ["bbc r1x", "/1xtra/programmes/schedules"],
                "bbcparliament" : ["bbc parliament", "/parliament/programmes/schedules"],
                "asiannetwork" : ["bbc asian net.", "/asiannetwork/programmes/schedules"],
                "sportsextra" : ["bbc r5sx", "/5livesportsextra/programmes/schedules"]}

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def getCurrentProg(self, channel):
        scheduleurl = "http://www.bbc.co.uk" + self.channels[channel][1] + ".json"
        syncschedurl = "http://beta.kamaelia.org:8082/dvb-bridge?command=channel&args=" + urllib.quote(self.channels[channel][0])
        synctimeurl = "http://beta.kamaelia.org:8082/dvb-bridge?command=time"

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

        # Grab SyncTV time data to work out the offset between local (NTP) and BBC time (roughly)
        try:
            req = urllib2.Request(synctimeurl,data,headers)
            syncconn = urllib2.urlopen(req)
        except httplib.BadStatusLine, e:
            print "DVB Bridge is inaccessible: " + str(e)
            syncconn = False
        except urllib2.HTTPError, e:
            print(e.code)
            syncconn= False
        except urllib2.URLError, e:
            syncconn = False
            print "URLError:", e.reason

        # Work out time difference
        if syncconn:
            content = syncconn.read()
            syncconn.close()
            try:
                decodedcontent = cjson.decode(content)
                if decodedcontent[0] == "OK":
                    difference = time() - decodedcontent[2]['time']
            except cjson.DecodeError, e:
                print "cjson.DecodeError:", e.message

        if 'difference' in locals():
        # Grab actual programme start time from DVB bridge channel page
            try:
                req = urllib2.Request(syncschedurl,data,headers)
                syncconn = urllib2.urlopen(req)
            except httplib.BadStatusLine, e:
                print "DVB Bridge is inaccessible: " + str(e)
                syncconn = False
            except urllib2.HTTPError, e:
                print(e.code)
                syncconn= False
            except urllib2.URLError, e:
                syncconn = False
                print "URLError:", e.reason

            if syncconn:
                content = syncconn.read()
                syncconn.close()
                try:
                    decodedcontent = cjson.decode(content)
                    if decodedcontent[0] == "OK":
                        proginfo = decodedcontent[2]['info']
                except cjson.DecodeError, e:
                    print "cjson.DecodeError:", e.message

        # Grab BBC schedule data for given channel
        try:
            req = urllib2.Request(scheduleurl,data,headers)
            conn1 = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print(e.code)
            conn1= False
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

            if 'proginfo' in locals():
                showdate = proginfo['NOW']['startdate']
                showtime = proginfo['NOW']['starttime']
                actualstart = proginfo['changed']
                showdatetime = datetime.strptime(str(showdate[0]) + "-" + str(showdate[1]) + "-" + str(showdate[2]) +
                    " " + str(showtime[0]) + ":" + str(showtime[1]) + ":" + str(showtime[2]),"%Y-%m-%d %H:%M:%S")

                # SyncTV produced data - let's trust that
                if 'decodedcontent' in locals():
                    for programme in decodedcontent['schedule']['day']['broadcasts']:
                        starttime = parse(programme['start'])
                        gmt = pytz.timezone("GMT")
                        starttime = starttime.astimezone(gmt)
                        starttime = starttime.replace(tzinfo=None)
                        # Identify which DVB bridge programme corresponds to the /programmes schedule to get PID
                        # FIXME: Turned off programme name checking as /programmes can show different info to DVB bridge
                        if showdatetime == starttime: # and string.lower(proginfo['NOW']['name']) == string.lower(programme['programme']['display_titles']['title']):
                            expectedstart = mktime(parse(programme['start']).astimezone(gmt).timetuple())
                            if 'difference' in locals():
                                offset = (expectedstart - actualstart) - difference
                            else:
                                offset = expectedstart - actualstart
                            pid = programme['programme']['pid']
                            title =  programme['programme']['display_titles']['title']
                            print [pid,title,offset,programme['duration'],programme['start']]
                            return [pid,title,offset,programme['duration'],programme['start']]
                            break

            else:
                # Work out what's on NOW here
                utcdatetime = datetime.now()

                # Analyse schedule
                if 'decodedcontent' in locals():
                    for programme in decodedcontent['schedule']['day']['broadcasts']:
                        starttime = parse(programme['start'])
                        starttime = starttime.replace(tzinfo=None)
                        endtime = parse(programme['end'])
                        endtime = endtime.replace(tzinfo=None)
                        if (utcdatetime >= starttime) & (utcdatetime < endtime):
                            pid = programme['programme']['pid']
                            title =  programme['programme']['display_titles']['title']
                            # Has to assume no offset as it knows no better
                            print [pid,title,0,programme['duration'],programme['start']]
                            return [pid,title,0,programme['duration'],programme['start']]
                            break

    def main(self):
        while not self.finished():
            if self.dataReady("inbox"):
                channel = self.recv("inbox")
                sleeper.sleep(1) # Temporary delay to ensure not hammering /programmes
                data = self.getCurrentProg(channel)
                self.send(data,"outbox")
            self.pause()
            yield 1

class NowPlaying(component):
    Inboxes = {
        "inbox" : "",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "",
        "signal" : ""
    }

    def __init__(self, proxy = False):
        super(NowPlaying, self).__init__()
        self.proxy = proxy
        self.channels = {"radio1" : "/radio1/nowplaying/latest"}

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

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
        while not self.finished():
            if self.dataReady("inbox"):
                channel = self.recv("inbox")
                sleeper.sleep(1) # Temporary delay to ensure not hammering /programmes
                npdata = self.getCurrentTrack(channel)
                self.send(npdata,"outbox")
            self.pause()
            yield 1

class ProgrammeData(component):
    # NOTE: This component could be replaced by a generic HTTP content grabber provided it allows for proxies

    Inboxes = {
        "inbox" : "Receives a PID and a data format",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "Sends out the retrieved raw data",
        "signal" : ""
    }

    def __init__(self, proxy = False):
        super(ProgrammeData, self).__init__()
        self.proxy = proxy
        self.programmesurl = "http://www.bbc.co.uk/programmes/"

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def getProgrammeData(self, pid, format):
        # Basic /programmes content grabber - user defined PID and data format

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
        except urllib2.HTTPError, e:
            print(e.code)
            conn1= False
        except urllib2.URLError, e:
            conn1 = False
            print "URLError:", e.reason

        # Read and return programme data
        if conn1:
            content = conn1.read()
            conn1.close()
            return content

    def main(self):
        while not self.finished():
            if self.dataReady("inbox"):
                request = self.recv("inbox")
                sleeper.sleep(1) # Temporary delay to ensure not hammering /programmes
                pid = request[0]
                format = request[1]
                progdata = self.getProgrammeData(pid,format)
                self.send(progdata,"outbox")
            self.pause()
            yield 1