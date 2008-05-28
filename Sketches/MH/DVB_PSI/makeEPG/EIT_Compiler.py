#!/usr/bin/env python
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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

"""\
=================================================================
Compile EIT schedule and present-following tables from a schedule
=================================================================

Aim of this code is to compile some DVB SI table sections representing an EIT
schedule (EPG) and present-following (now&next) data. The input sources will
be some configuration files defining the schedule and programmes.


A schedule file consists of lines of the form::
    
    #     service-id   event-id   starttime            duration  programme-ref
    EVENT nnnn         nnnn       yyyy-mm-ddThh:mm:ss  hh:mm:ss  filename

Programme ref's are the filename containing programme metadata. Must be of the form::
    
    [programme]
    title            = The quick brown fox
    description      = In this exciting show, we follow the exciting adventures of Mr Quick the brown fox.
    duration         = 00:30:00
    content_type     = 0x01 0x14
    instance_crid    = /ABCD
    series_crid      = /1234
    transport_stream = dummy.ts

    

"""

import re
import os
import ConfigParser
import copy
from CreateSections import SerialiseEITSection
from CreateSections import PacketiseTableSections
from CreateSections import MakeTransportStreamPackets
import datetime
import time

from Parsing import parseInt
from Parsing import parseISOdateTime
from Parsing import parseList


class ScheduleEvent(object):
    def __init__(self):
        super(ScheduleEvent,self).__init__()
        self.event_id = 0
#        self.starttime = (0,0,0,0,0,0)
#        self.duration = (0,0,0)
        self.running_status = 1
        self.programme_info_file = None
        
    def __cmp__(self, other):
        if self.starttime < other.starttime:
            return -1
        elif self.starttime > other.starttime:
            return +1
        else:
            return 0
    
    def setStartISO(self, isoTimeString):
        self.starttime = parseISOdateTime(isoTimeString)
        
    def setDuration(self, hour,minute,second):
        self.duration = datetime.timedelta(hours=hour,minutes=minute,seconds=second)
        self.duration_tuple = (hour,minute,second)

    def setRunningStatus(self, status):
        status = status.lower().strip()
        try:
            self.running_status = \
            { "no"      : 1,
              "soon"    : 2,
              "pausing" : 3,
              "running" : 4 }[status]
        except KeyError:
            self.running_status = 1   # mark as not running

    def buildDescriptors(self, serviceDescriptors, programmes):
        servD = copy.deepcopy(serviceDescriptors)
        progD = copy.deepcopy(programmes[self.programme_info_file].descriptors)
        self.descriptors = []
        self.descriptors.extend(servD)
        self.descriptors.extend(progD)
        

class Schedule(object):
    def __init__(self, infile, timenow):
        super(Schedule,self).__init__()
        self.events = []
        self.timenow = timenow

        COMMENT = re.compile(r"^\s*[#].*$")
        EMPTY = re.compile(r"^\s*$")
        EVENT = re.compile(r"^\s*event\s+(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d)\s+(\d\d):(\d\d):(\d\d)\s+(\d+)\s+(.*)\s*$", re.I)
        for line in infile:
            if re.match(COMMENT, line):
                pass
            elif re.match(EMPTY, line):
                pass
            else:
                match = re.match(EVENT, line)
                if match:
                    e = ScheduleEvent()
                    e.setStartISO(match.group(1))
                    e.setDuration(hour   = int(match.group(2)),
                                  minute = int(match.group(3)),
                                  second = int(match.group(4)),
                              )
                    e.event_id   = int(match.group(5))
                    e.programme_info_file = match.group(6)
                    
                    # resolve running status
                    if timenow >= e.starttime and timenow < e.starttime + e.duration:
                        e.setRunningStatus("running")
                    else:
                        e.setRunningStatus("no")
                    
                    self.events.append(e)
                    
        # sort into chronological order
        self.events.sort()
            
        
    def buildDescriptors(self, serviceDescriptors, programmes):
        for event in self.events:
            event.buildDescriptors(serviceDescriptors,programmes)
            
            
    def findPresentFollowing(self):
        """\
        Reduces down the set of events to only those needed for Present-Following table data
        """
        # find the one marked as running (the "present") then find the one after it (the "following")
        presentEvent = None
        for event in self.events:
            if presentEvent is None:
                if event.running_status == 4:
                    presentEvent = event
            else:
                return [ presentEvent, event ]
    
        # nothing is present, so lets do a more exhaustive search for following
        # (find first event in the future, going through them in ascending order)
        for event in self.events:
            if event.starttime > self.timenow:
                return [ event ]
        
        return [] # really can't find anything
        
    def buildScheduleSections(self,tableIds,version,onid,tsid,serviceId,serviceDescriptors):
        return self.buildSections(tableIds,version,onid,tsid,serviceId,serviceDescriptors,True)
    
    def buildPfSections(self,tableIds,version,onid,tsid,serviceId,serviceDescriptors):
        return self.buildSections(tableIds,version,onid,tsid,serviceId,serviceDescriptors,False)
    
    def buildSections(self,tableIds,version,onid,tsid,serviceId,serviceDescriptors,schedule):
        
        if schedule:
            events = self.events
        else:
            events = self.findPresentFollowing()
        
        # now build the sections
        self.serialiser = SerialiseEITSection()
        sectionedEvents = self.groupEventsBySection(events)
        return self.compileSections(tableIds,
                version,
                onid,
                tsid,
                serviceId,
                sectionedEvents,
                )
        
        
    def groupEventsBySection(self, events):
        eventGroups = []
        
        # first pass, go through compiling just event sections and getting them grouped
        # then we'll know how many table sections there actually are, and we can then
        # build the full tables
        remainingEvents = [ \
            { \
                "event_id"       : e.event_id,
                "starttime"      : e.starttime.timetuple()[0:6],
                "duration"       : e.duration_tuple,
                "running_status" : e.running_status,
                "free_CA_mode"   : False,
                "descriptors"    : e.descriptors,
            } \
            for e in events ]
        
        while len(remainingEvents) > 0:
            (serialisedEvents, count) = self.serialiser.consumeEvents(remainingEvents)
            eventGroups.append(serialisedEvents)
            for _ in range(count):
                remainingEvents.pop(0)
    
        return eventGroups
    
    def compileSections(self,tableIds,version,onid,tsid,serviceId,eventGroups):
        # now we know how it is going to spread across sections and table ids, we can build
        # the full sections
        numTables = len(eventGroups) / 256
        if  len(eventGroups) % 256 > 0:
            numTables = numTables + 1
            
        section = {
#            "table_id" : -1,
            "current"  : True,
            "service_id" : serviceId,
            "version" : version % 32,
#            "section" : -1,
#            "last_section" : -1,
            "last_table_id" : tableIds[numTables-1],
            "original_network_id" : onid,
            "transport_stream_id" : tsid,
        }
        
        sections = []
        tid = 0
        sectionNum = 0
        remainingSections = len(eventGroups)
        for eg in eventGroups:
            assert(remainingSections > 0)
            section["table_id"] = tableIds[tid]
            section["section"] = sectionNum
            section["last_section"] = min(remainingSections-1, 255)
            sectionNum += 1
            remainingSections -= 1
            if sectionNum > 255:
                sectionNum = 0
                tid += 1
                
            serialisedSection = self.serialiser.serialise(section, prebuiltEvents=eg)
            sections.append(serialisedSection)
            
        assert(remainingSections == 0)

        return sections


class Programme(object):
    def __init__(self, programme_file):
        super(Programme,self).__init__()
        self.descriptors = []
        
        parser = ConfigParser.ConfigParser()
        parser.read(programme_file)
        
        # mandatory bits
        duration         = parser.get("programme","duration").strip()
        match = re.match(re.compile("^(\d\d):(\d\d):(\d\d)$"),duration)
        self.duration = (match.group(1), match.group(2), match.group(3))
        self.ts_file     = parser.get("programme", "transport_stream").strip()
        
        # optional(ish) bits
        if parser.has_option("programme","title") and parser.has_option("programme","description"):
            self.title       = parser.get("programme","title").strip()
            self.description = parser.get("programme","description").strip()
            self.addShortEventDescriptor()
        else:
            pass # perhaps we should actually throw an error here
        
        if parser.has_option("programme","content_type"):
            ctype = parser.get("programme","content_type")
            level1, level2 = ctype.split(" ")
            self.content_type = ( parseInt(level1), parseInt(level2) )
            self.addContentTypeDescriptor()
            
        if parser.has_option("programme","instance_crid"):
            self.instance_crid = parser.get("programme","instance_crid").strip()
            self.addInstanceCridDescriptor()
        
        if parser.has_option("programme","series_crid"):
            self.series_crid = parser.get("programme","series_crid").strip()
            self.addSeriesCridDescriptor()

    def addShortEventDescriptor(self):
        self.descriptors.append( (0x4d, { "type" : "short_event",
            "language_code" : 'eng',
            "name"          : self.title,
            "text"          : self.description,
            } ) )
            

    def addContentTypeDescriptor(self):
        self.descriptors.append( (0x54, { "type" : "content",
            "content_level_1" : self.content_type[0],
            "content_level_2" : self.content_type[1],
            "user1" : 0,
            "user2" : 0,
            } ) )
            
    def addInstanceCridDescriptor(self):
        self.descriptors.append( (0x76, { "type" : "content_identifier",
            "crids" : [ { "type" : "instance", "crid" : self.instance_crid } ],
            } ) )

    def addSeriesCridDescriptor(self):
        self.descriptors.append( (0x76, { "type" : "content_identifier",
            "crids" : [ { "type" : "part of series", "crid" : self.series_crid } ],
            } ) )


def loadService(servicefile):
    f = open(servicefile,"r")
    data = f.read()
    return eval(data)   # yeah, dangerous, but I'll hopefully fix later


class GeneralConfig(object):
    def __init__(self,configFile):
        super(GeneralConfig,self).__init__()
        parser = ConfigParser.ConfigParser()
        parser.read(configFile)
    
        self.onid = parseInt(parser.get("mux", "onid"))
        self.tsid = parseInt(parser.get("mux", "tsid"))
        self.pf_tableIds = [parseInt(x) for x in parseList(parser.get("present-following","table-ids"))]
        self.sch_tableIds = [parseInt(x) for x in parseList(parser.get("schedule","table-ids"))]


def parseArgs():
    import sys
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="infile",
        action="store", type="string", default="-",
        help="read schedule from the specified file, or stdin if '-' or not specified",
        metavar="FILE")
    
    parser.add_option("-s", "--service", dest="servicefile",
        action="store", type="string", default=None,
        help=r'the service file defining service ID and default descriptors,',
        metavar="FILE")
        
    parser.add_option("-g", "--generalconfig", dest="configfile",
        action="store", type="string", default=None,
        help="read service and general mux config from the specified file",
        metavar="FILE")
        
    parser.add_option("-p", "--present-following", dest="pf_outfile",
        action="store", type="string", default=None,
        help="destination filename for present-following table sections",
        metavar="FILE")

    parser.add_option("-c", "--schedule", dest="sch_outfile",
        action="store", type="string", default=None,
        help="destination filename for schedule table sections",
        metavar="FILE")

    parser.add_option("-t", "--tableversion", dest="version",
        action="store", type="int", default=None,
        help="the version number to use for the table",
        )
        
    parser.add_option("-n", "--timenow", dest="timenow",
        action="store", type="string", default=None,
        help="Datetime in ISO format YYYY-MM-DDTHH:MM:SS (must be exactly this format)",
        )
        
    parser.add_option("-m", "--mux", dest="mux",
        action="store_true", default=False,
        help="Optional. Set to output a transport stream containing sections in ts packets of pid 0x12",
        )
        
    (options, args) = parser.parse_args()
    
    if options.servicefile is None:
        sys.stderr.write("You must specify the service description file (option '-s')\n")
        sys.exit(1)
        
    if options.configfile is None:
        sys.stderr.write("You must specify the global config file (option '-c')\n")
        sys.exit(1)
        
    if options.timenow is None:
        sys.stderr.write("You must specify time for which schedule/pf is built (option '-n')\n")
        sys.exit(1)
        
    options.timenow = parseISOdateTime(options.timenow)

    return options

if __name__ == "__main__":
    import sys
    options = parseArgs()
        

    if options.infile == "-":
        infile = sys.stdin
    else:
        infile = open(options.infile,"r")
        
    # stage 1 - parse the schedule
    schedule = Schedule(infile, options.timenow)
    
    # stage 2 - determine what programmes are in the schedule and read metadata for them
    programmes = {}
    for item in schedule.events:
        progInfoFile = item.programme_info_file
        if not programmes.has_key(progInfoFile):
            programmes[progInfoFile] = Programme(progInfoFile)
    
    # stage 3 - determine what services are in the schedule and read configs for them
    serviceId, serviceDescriptors = loadService(options.servicefile)
    
    # stage 4 - read global config - eg. ONID and TSID values
    generalConfig = GeneralConfig(options.configfile)
    
    # stage 5 - construct full descriptors for all events
    schedule.buildDescriptors(serviceDescriptors, programmes)
    print options.mux
    if options.sch_outfile is not None:
        # write out the 'schedule' table sections
        sections = schedule.buildScheduleSections(
            generalConfig.sch_tableIds,
            options.version,
            generalConfig.onid,
            generalConfig.tsid,
            serviceId,
            serviceDescriptors,
            )
        if not options.mux:
            f=open(options.sch_outfile, "wb")
            f.write("".join(sections))
            f.close()
        else:
            ts = []
            packetiser = PacketiseTableSections(MakeTransportStreamPackets(0x12))
            for section in sections:
                ts.extend(packetiser.packetise(section))
            f=open(options.sch_outfile, "wb")
            f.write("".join(ts))
            f.close()
        
    if options.pf_outfile is not None:
        # write out the 'present-following' table sections
        sections = schedule.buildPfSections(
            generalConfig.pf_tableIds,
            options.version,
            generalConfig.onid,
            generalConfig.tsid,
            serviceId,
            serviceDescriptors,
            )
        if not options.mux:
            f=open(options.pf_outfile, "wb")
            f.write("".join(sections))
            f.close()
        else:
            ts = []
            packetiser = PacketiseTableSections(MakeTransportStreamPackets(0x12))
            for section in sections:
                ts.extend(packetiser.packetise(section))
            f=open(options.pf_outfile, "wb")
            f.write("".join(ts))
            f.close()
    