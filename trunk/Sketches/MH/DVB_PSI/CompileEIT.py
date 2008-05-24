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
import ConfigParser


class ScheduleEvent(object):
    
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


class ParseSchedule(object):
    def __init__(self):
        super(ParseSchedule,self).__init__()
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
            
            
def default_components(service_id):
    if serviceId == 1000 or True:
        return [
            ( 0x50, { "type"     : "component",
                "component_tag"  : 1,
                "stream_content" : 1,  # video
                "component_type" : 3,  # 16:9 aspect ratio without pan vectors, 25 Hz
                "language_code"  : 'und',
                "text"           : ''
                    } ),
            ( 0x50, { "type"     : "component",
                "component_tag"  : 2,
                "stream_content" : 2,  # audio
                "component_type" : 3,  # stereio (2 channel)
                "language_code"  : 'eng',
                "text"           : ''
                    } ),
        ]
            
            

def parseInt(string):
    HEX = re.compile("^\s*0x[0-9a-f]+\s*$", re.I)
    DEC = re.compile("^\s*\d+\s*$", re.I)
        
    if re.match(DEC,string):
        return int(string, 10)
    elif re.match(HEX,string):
        return int(string, 16)
    else:
        return int(string)

class Programme(object):
    def __init__(self, programme_file):
        super(Programme,self).__init__()
        self.descriptors = []
        self.load(programme_file)
        
    def load(self,filename):
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        
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
        
        print self.descriptors
        
    def addShortEventDescriptor(self):
        self.descriptors.append( (0x4d, { "type" : "short_event",
            "language_code" : 'eng',
            "name"          : self.title,
            "text"          : self.description,
            } ) )
            

    def addContentTypeDescriptor(self):
        print self.content_type
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



if __name__ == "__main__":
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="infile",
        action="store", type="string", default="-",
        help="read schedule from the specified file, or stdin if '-' or not specified",
        metavar="FILE")

    (options, args) = parser.parse_args()

    import sys
    if options.infile == "-":
        infile = sys.stdin
    else:
        infile = open(options.infile,"r")
        
    # stage 1 - parse the schedule
    parser = ParseSchedule()
    parser.read(infile)
    #print parser.events
    
    # stage 2 - determine what programmes are in the schedule and read metadata for them
    prog=Programme("test_programme")
    from CreateDescriptors import serialiseDescriptors
    print repr(serialiseDescriptors(prog.descriptors))
    
    # stage 3 - determine what services are in the schedule and read configs for them
    
    # stage 4 - read global config - eg. ONID and TSID values
    
    # stage 5 - construct full descriptors for all events
    
    # stage 6 - write out the 'schedule' table sections
    
    # stage 7 - determine what goes in the present-following table
    
    # stage 8 - write out the 'present-following' table sections
    
    