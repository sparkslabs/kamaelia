#! /usr/bin/python

'''
Interface to BBC /programmes JSON etc
- Identifies PID of current programme on a chosen channel
- Provides output for PIDs in a chosen format (XML, RDF etc)
- Identifies currently playing tracks on radio channels TODO
'''

import json as cjson
import pytz
import string
import time
import urllib
from dateutil.parser import parse
from datetime import datetime, timedelta, tzinfo

from Axon.Ipc import producerFinished
from Axon.Ipc import shutdownMicroprocess
from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent

from Kamaelia.Apps.SocialBookmarks.Print import Print

class GMT(tzinfo):
    def utcoffset(self,dt):
        return timedelta(hours=0,minutes=0)
    def tzname(self,dt):
        return "GMT"
    def dst(self,dt):
        return timedelta(0)

class WhatsOn(threadedcomponent):
    Inboxes = {
        "inbox" : "Receives a channel name to investigate in the 'key' format from self.channels",
        "datain" : "Return path for requests to HTTP getter component",
        "control" : ""
    }
    Outboxes = {
        "outbox" : "If a channel is on air, sends out programme info [pid,title,timeoffset,duration,expectedstarttime]",
        "dataout" : "URLs out for data requests to HTTP getter",
        "signal" : ""
    }

    def __init__(self, proxy = False):
        super(WhatsOn, self).__init__()
        self.proxy = proxy
        # Define channel schedule URLs and DVB bridge channel formats
        self.channels = {"bbcone" : ["bbc one", "/bbcone/programmes/schedules/north_west"],
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

    def main(self):
        while not self.finished():
            if self.dataReady("inbox"):
                channel = self.recv("inbox")
                time.sleep(1) # Temporary delay to ensure not hammering /programmes

                # Setup in case of URL errors later
                data = None

                # Define URLs for getting schedule data and DVB bridge information
                # By BBC convention, schedule info runs to 5am the next day
                if datetime.utcnow().hour < 5:
                    scheduleurl = "http://www.bbc.co.uk" + self.channels[channel][1] + "/" + time.strftime("%Y/%m/%d",time.gmtime(time.time()-86400)) + ".json"
                else:
                    scheduleurl = "http://www.bbc.co.uk" + self.channels[channel][1] + "/" + time.strftime("%Y/%m/%d",time.gmtime(time.time())) + ".json"
                #syncschedurl = "http://beta.kamaelia.org:8082/dvb-bridge?command=channel&args=" + urllib.quote(self.channels[channel][0])
                #synctimeurl = "http://beta.kamaelia.org:8082/dvb-bridge?command=time"
                syncschedurl = "http://10.92.164.147:8082/dvb-bridge?command=channel&args=" + urllib.quote(self.channels[channel][0])
                synctimeurl = "http://10.92.164.147:8082/dvb-bridge?command=time"

                content = None
#                # Grab SyncTV time data to work out the offset between local (NTP) and BBC time (roughly)
#                self.send([synctimeurl], "dataout")
#                while not self.dataReady("datain"):
#                    self.pause()
#                    yield 1
#                recvdata = self.recv("datain")
#                if recvdata[0] == "OK":
#                    content = recvdata[1]
#                else:
#                    content = None

                # Work out time difference between local time and BBC time
                if content != None:
                    try:
                        decodedcontent = cjson.decode(content)
                        if decodedcontent[0] == "OK":
                            difference = time.time() - decodedcontent[2]['time']
                    except cjson.DecodeError:
                        e = sys.exc_info()[1]
                        Print("cjson.DecodeError:", e.message)

                if 'difference' in locals():  # FIXME *SOB*
                    # Grab actual programme start time from DVB bridge channel page
                    self.send([syncschedurl], "dataout")
                    while not self.dataReady("datain"):
                        self.pause()  # Add timeout ?
#                        yield 1
                    recvdata = self.recv("datain")
                    if recvdata[0] == "OK":
                        content = recvdata[1]
                    else:
                        content = None

                    if content != None:
                        try:
                            decodedcontent = cjson.decode(content)
                            if decodedcontent[0] == "OK":
                                proginfo = decodedcontent[2]['info']
                        except cjson.DecodeError:
                            e = sys.exc_info()[1]
                            Print("cjson.DecodeError:", e.message)

                # Grab BBC schedule data for given channel
                self.send([scheduleurl], "dataout")
                while not self.dataReady("datain"):
                    self.pause()  # FIXME Add timeout?
#                    yield 1
                recvdata = self.recv("datain")
                if recvdata[0] == "OK":
                    content = recvdata[1]
                else:
                    content = None

                # Read and decode schedule
                if content != None:
                    try:
                        decodedcontent = cjson.decode(content)
                    except cjson.DecodeError:
                        e = sys.exc_info()[1]
                        Print("cjson.DecodeError:", e.message)

                    if 'proginfo' in locals():
                        showdate = proginfo['NOW']['startdate']
                        showtime = proginfo['NOW']['starttime']
                        actualstart = proginfo['changed']
                        showdatetime = datetime.strptime(str(showdate[0]) + "-" + str(showdate[1]) + "-" + str(showdate[2]) +
                            " " + str(showtime[0]) + ":" + str(showtime[1]) + ":" + str(showtime[2]),"%Y-%m-%d %H:%M:%S")

                        # SyncTV (DVB Bridge) produced data - let's trust that
                        if 'decodedcontent' in locals():
                            for programme in decodedcontent['schedule']['day']['broadcasts']:
                                starttime = parse(programme['start'])
                                gmt = pytz.timezone("GMT")
                                starttime = starttime.astimezone(gmt)
                                starttime = starttime.replace(tzinfo=None)
                                # Attempt to identify which DVB bridge programme corresponds to the /programmes schedule to get PID
                                if showdatetime == starttime or (showdatetime + timedelta(minutes=1) == starttime and string.lower(proginfo['NOW']['name']) == string.lower(programme['programme']['display_titles']['title'])) or (showdatetime - timedelta(minutes=1) == starttime and string.lower(proginfo['NOW']['name']) == string.lower(programme['programme']['display_titles']['title'])):
                                    duration = (proginfo['NOW']['duration'][0] * 60 * 60) + (proginfo['NOW']['duration'][1] * 60) + proginfo['NOW']['duration'][2]
                                    progdate = parse(programme['start'])
                                    tz = progdate.tzinfo
                                    utcoffset = datetime.strptime(str(tz.utcoffset(progdate)),"%H:%M:%S")
                                    utcoffset = utcoffset.hour * 60 * 60
                                    # Something's not right with the code below #TODO #FIXME
                                    timestamp = time.mktime(showdatetime.timetuple()) + utcoffset
                                    if 'difference' in locals():
                                        offset = (timestamp - actualstart) - difference
                                    else:
                                        offset = timestamp - actualstart
                                    pid = programme['programme']['pid']
                                    title =  programme['programme']['display_titles']['title']
                                    # Fix for unicode errors caused by some /programmes titles
                                    if (not isinstance(title,str)) and (not isinstance(title,unicode)):
                                        title = str(title)
                                    Print(pid,title,offset,duration,showdatetime, "GMT",utcoffset)
                                    data = [pid,title,offset,duration,timestamp,utcoffset]
                                    

                    else:
                        # Couldn't use the DVB Bridge, so work out what's on NOW here
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
                                    # Fix for unicode errors caused by some /programmes titles
                                    if (not isinstance(title,str)) and (not isinstance(title,unicode)):
                                        title = str(title)
                                    # Has to assume no offset between scheduled and actual programme start time as it knows no better because of the lack of DVB bridge
                                    progdate = parse(programme['start'])
                                    tz = progdate.tzinfo
                                    utcoffset = datetime.strptime(str(tz.utcoffset(progdate)),"%H:%M:%S")
                                    utcoffset = utcoffset.hour * 60 * 60
                                    timestamp = time.mktime(progdate.timetuple()) - utcoffset
                                    Print(pid,title,0,programme['duration'],programme['start'],utcoffset)
                                    data = [pid,title,0,programme['duration'],timestamp,utcoffset]
                                    

                self.send(data,"outbox")
            if not self.anyReady():
                self.pause()
#            yield 1
            

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

    def main(self):
        while not self.finished():
            if self.dataReady("inbox"):
                # TODO This component is unfinished as it was never found to be needed
                channel = self.recv("inbox")
                time.sleep(1) # Temporary delay to ensure not hammering /programmes
                nowplayingurl = "http://www.bbc.co.uk" + self.channels[channel] + ".json"

                npdata = None
                # Grab BBC data
                self.send([nowplayingurl], "dataout")
                while not self.dataReady("datain"):
                    yield 1
                    self.pause()
                recvdata = self.recv("datain")
                if recvdata[0] == "OK":
                    content = recvdata[1]
                else:
                    content = None

                # Read and decode now playing info
                if content != None:
                    try:
                        decodedcontent = cjson.decode(content)
                    except cjson.DecodeError:
                        e = sys.exc_info()[1]
                        Print("cjson.DecodeError:", e.message)

                # Analyse now playing info
                if decodedcontent:
                    # Not finished! - now playing json file is empty if nothing is playing!
                    npdata = False


                self.send(npdata,"outbox")
            self.pause()
            yield 1
