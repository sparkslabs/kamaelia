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
    
    #     service-id   event-id   starttime            duration  running                  programme-ref
    EVENT nnnn         nnnn       yyyy-mm-dd hh:mm:ss  hh:mm:ss  NO|SOON|PAUSING|RUNNING  filename

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
from CreatePSI import SerialiseEITSection


class ScheduleEvent(object):
    def __init__(self):
        super(ScheduleEvent,self).__init__()
        self.service_id = 0
        self.event_id = 0
        self.starttime = (0,0,0,0,0,0)
        self.duration = (0,0,0)
        self.running_status = 1
        self.programme_info_file = None
    
    def setStart(self, year, month, day, hour, minute, second):
        self.starttime = (year,month,day,hour,minute,second)
        
    def setDuration(self, hour,minute,second):
        self.duration = (hour,minute,second)

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

    def buildDescriptors(self, services, programmes):
        progD = copy.deepcopy(programmes[self.programme_info_file].descriptors)
        servD = copy.deepcopy(services[self.service_id])
        self.descriptors = []
        self.descriptors.extend(progD)
        self.descriptors.extend(servD)
        

class Schedule(object):
    def __init__(self):
        super(Schedule,self).__init__()
        self.events = []

    def read(self, infile):
        COMMENT = re.compile(r"^\s*[#].*$")
        EMPTY = re.compile(r"^\s*$")
        EVENT = re.compile(r"^\s*event\s+(\d+)\s+(\d+)\s+(\d\d\d\d)-(\d\d)-(\d\d)\s+(\d\d):(\d\d):(\d\d)\s+(\d\d):(\d\d):(\d\d)\s+(no|soon|pausing|running)\s+(.*)\s*$", re.I)
        for line in infile:
            if re.match(COMMENT, line):
                pass
            elif re.match(EMPTY, line):
                pass
            else:
                match = re.match(EVENT, line)
                if match:
                    e = ScheduleEvent()
                    e.service_id = int(match.group(1))
                    e.event_id   = int(match.group(2))
                    e.setStart(year   = int(match.group(3)),
                               month  = int(match.group(4)),
                               day    = int(match.group(5)),
                               hour   = int(match.group(6)),
                               minute = int(match.group(7)),
                               second = int(match.group(8)),
                              )
                    e.setDuration(hour   = int(match.group(9)),
                                  minute = int(match.group(10)),
                                  second = int(match.group(11)),
                              )
                    e.setRunningStatus(match.group(12))
                    e.programme_info_file = match.group(13)
                    
                    self.events.append(e)
            
    def buildDescriptors(self, services, programmes):
        for event in self.events:
            event.buildDescriptors(services,programmes)
            
            
    def subsetToPF(self):
        """\
        Reduces down the set of events to only those needed for Present-Following table data
        """
        raise "Not implemented"
    
    
    def buildSections(self,tableIds,version,onid,tsid,services):
        # first sort into separate services and internally within each, into chronological order
        eventsByService = {}
        for sid in services.keys():
            eventsByService[sid] = []
            
        for event in self.events:
            e = (event.starttime, event)
            eventsByService[event.service_id].append(e)
    
        for sid in eventsByService.keys():
            eventsByService[sid].sort()
            eventsByService[sid] = [ e for (_,e) in eventsByService[sid] ]
            
        sections = []
        for sid in eventsByService.keys():
            sections.extend( self.buildServiceSections(tableIds,
                version,
                onid,
                tsid,
                sid,
                eventsByService[sid],
                ))
                
        return sections
    
    def buildServiceSections(self,tableIds,version,onid,tsid,serviceId,relevantEvents):
        
        serialiser = SerialiseEITSection()
        eventGroups = []
        
        # first pass, go through compiling just event sections and getting them grouped
        # then we'll know how many table sections there actually are, and we can then
        # build the full tables
        remainingEvents = [ \
            { \
                "event_id"       : e.event_id,
                "starttime"      : e.starttime,
                "duration"       : e.duration,
                "running_status" : e.running_status,
                "free_CA_mode"   : False,
                "descriptors"    : e.descriptors,
            } \
            for e in relevantEvents ]
        
        while len(remainingEvents) > 0:
            (serialisedEvents, count) = serialiser.consumeEvents(remainingEvents)
            eventGroups.append(serialisedEvents)
            for _ in range(count):
                remainingEvents.pop(0)

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
                
            serialisedSection = serialiser.serialise(section, prebuiltEvents=eg)
            sections.append(serialisedSection)
            
        assert(remainingSections == 0)

        return sections

def parseInt(string):
    HEX = re.compile("^\s*0x[0-9a-f]+\s*$", re.I)
    DEC = re.compile("^\s*\d+\s*$", re.I)
        
    if re.match(DEC,string):
        return int(string, 10)
    elif re.match(HEX,string):
        return int(string, 16)
    else:
        return int(string)

def parseList(string):
    CAR_CDR = re.compile(r"^\s*(\S+)(\s+.*)?$")
    tail = string.strip()
    theList = []
    
    while tail:
        match = re.match(CAR_CDR, tail)
        theList.append(match.group(1))
        tail = match.group(2)
        
    return theList

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


def loadService(sid, serviceDir):
    f = open(serviceDir+os.sep+("%d" % sid),"r")
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
    
    parser.add_option("-s", "--services-dir", dest="servicesdir",
        action="store", type="string", default=None,
        help=r'the directory containing %d.py files defining service default descriptors, where %d is a service ID in decimal',
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
        
    (options, args) = parser.parse_args()
    
    if options.servicesdir is None:
        sys.stderr.write("You must specify the services dir (option '-s')\n")
        sys.exit(1)
        
    if options.configfile is None:
        sys.stderr.write("You must specify the global config file (option '-c')\n")
        sys.exit(1)

    return options

if __name__ == "__main__":
    import sys
    options = parseArgs()
        

    if options.infile == "-":
        infile = sys.stdin
    else:
        infile = open(options.infile,"r")
        
    # stage 1 - parse the schedule
    schedule = Schedule()
    schedule.read(infile)
    
    # stage 2 - determine what programmes are in the schedule and read metadata for them
    programmes = {}
    for item in schedule.events:
        progInfoFile = item.programme_info_file
        if not programmes.has_key(progInfoFile):
            programmes[progInfoFile] = Programme(progInfoFile)
    
    # stage 3 - determine what services are in the schedule and read configs for them
    services = {}
    for item in schedule.events:
        serviceId = item.service_id
        if not services.has_key(serviceId):
            services[serviceId] = loadService(serviceId, options.servicesdir)
    
    # stage 4 - read global config - eg. ONID and TSID values
    generalConfig = GeneralConfig(options.configfile)
    
    # stage 5 - construct full descriptors for all events
    schedule.buildDescriptors(services, programmes)
    
    if options.sch_outfile is not None:
        # stage 6 - write out the 'schedule' table sections
        sections = schedule.buildSections(generalConfig.sch_tableIds,
            options.version,
            generalConfig.onid,
            generalConfig.tsid,
            services)
        f=open(options.sch_outfile, "wb")
        f.write("".join(sections))
        f.close()
        
    if options.pf_outfile is not None:
        # stage 7 - determine what goes in the present-following table
        schedule.subsetToPF()
    
        # stage 8 - write out the 'present-following' table sections
        sections = schedule.buildSections(generalConfig.pf_tableIds,
            options.version,
            generalConfig.onid,
            generalConfig.tsid,
            services)
        f=open(options.pf_outfile, "wb")
        f.write("".join(sections))
        f.close()
    