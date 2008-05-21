#!/usr/bin/env python
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===============================================
Parsing Event Information Tables in DVB streams
===============================================

ParseEventInformationTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs a dictionary containing the data in the table.

The Event Information Table carries data about the programmes being broadcast
both now (present-following data) and in the future (schedule data) and is
typically used to drive Electronic Progamme Guides, scheduled recording and
"now and next" information displays.

The purpose of the EIT and details of the fields within in are defined in the
DVB SI specification:

- ETSI EN 300 468 
  "Digital Video Broadcasting (DVB); Specification for Service Information (SI)
  in DVB systems"
  ETSI / EBU (DVB group)

See Kamaelia.Support.DVB.Descriptors for information on how they are parsed.



Example Usage
~~~~~~~~~~~~~

A simple pipeline to receive, parse and display the "now and next" information
for programmes in the current multiplex, from the Event Information Table::

    FREQUENCY = 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    EIT_PID = 0x12
    
    Pipeline( DVB_Multiplex(FREQUENCY, [NIT_PID], feparams),
              DVB_Demuxer({ NIT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseEventInformationTable_Subset(actual_presentFollowing=True),
              PrettifyEventInformationTable(),
              ConsoleEchoer(),
            ).run()

A slight modification to the pipeline, to convert the parsed tables into a
stream of inidividual events::

    Pipeline( DVB_Multiplex(FREQUENCY, [NIT_PID], feparams),
              DVB_Demuxer({ NIT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseEventInformationTable_Subset(actual_presentFollowing=True),
              SimplifyEIT(),
              ConsoleEchoer(),
            ).run()



ParseEventInformationTable / ParseEventInformationTable_Subset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


            
Behaviour
---------

At initialisation, specify what sub tables you want ParseEventInformationTable
to process (others will be ignored). Event information is grouped into sub
tables according to where it is:

* 'Actual' data describes programmes broadcast in the same actual multiplex
  as this data
* 'Other' data describes programmes being broadcast in other multiplexes

...and what timeframe it relates to:
    
* 'present following' data describes the now showing (present) and next
  (following) programme to be shown
* 'schedule' data describes programmes being shown later, typically over the
  next 7 or 8 days.

Initialise ParseEventInformationTable by providing a dictionary mapping table
ids, to be accepted, to (label, is-present-following-flag) pairs. For example,
to accept tables of present-following data for this and other multiplexes::

    ParseEventInformationTable(acceptTables = { 0x4e : ("ACTUAL", True),
                                                0x4f : ("OTHER", False),
                                              }

However it is much simpler to use the ParseEventInformationTable_Subset helper
funciton to create it for you. For example, the same effect as above can be
achieved with::

    ParseEventInformationTable_Subset( actual_presentFollowing = True,
                                       other_presentFollowing  = True,
                                       actual_schedule         = False,
                                       other_schedule          = False,
                                     )

Send reconstructed PSI table 'sections' to the "inbox" inbox. When all sections
of the table have arrived, ParseNetworkInformationTable will parse the table
and send it out of its "outbox" outbox.

If the table is unchanged since last time it was parsed, then it will not be
sent out. Parsed tables are only sent out when they are new or have just
changed.

Note that an EIT table is likely to arrive, and be parsed in lots of separate
fragments. Because of the way the data format is defined, it is impossible for
ParseEventInformationTable to know for certain when it has received everything!

The parsed table is sent out as a dictionary data structure, like this (list of
event descriptors abridged for brevity)::

    {
        'table_id'            : 78,
        'table_type'          : 'EIT',
        'current'             : 1,
        'actual_other'        : 'ACTUAL',
        'is_present_following': True,
        'transport_stream_id' : 4100,
        'original_network_id' : 9018,
        'events': [
            { 'event_id'      : 8735,
              'running_status': 1,
              'free_CA_mode'  : 0,
              'starttime'     : [2006, 12, 22, 11, 0, 0],
              'duration'      : (0, 30, 0),
              'service_id'    : 4164
              'descriptors': [
                  (77, {'type': 'short_event', 'name': 'To Buy or Not to Buy', 'text': 'Series that gives buyers the chance to test-drive a property before they buy it. Sarah Walker and Simon Rimmer are in Birmingham, helping a pair of property professionals. [S]', 'language_code': 'eng'}),
                  (80, {'type': 'component', 'stream_content': 1, 'component_type': 3, 'text': 'Video 1', 'component_tag': 1, 'content,type': ('video', '16:9 aspect ratio without pan vectors, 25 Hz'), 'language_code': '   '}),
                  (80, {'type': 'component', 'stream_content': 2, 'component_type': 3, 'text': 'Audio 2', 'component_tag': 2, 'content,type': ('audio', 'stereo (2 channel)'), 'language_code': 'eng'}),
                  (80, {'type': 'component', 'stream_content': 3, 'component_type': 16, 'text': 'Subtitling 5', 'component_tag': 5, 'content,type': ('DVB subtitles (normal)', 'with no monitor aspect ratio criticality'), 'language_code': '   '}),
                  (80, {'type': 'component', 'stream_content': 4, 'component_type': 1, 'text': 'Data 6', 'component_tag': 6, 'content,type': (4, 1), 'language_code': '   '}),
                  
                  .....
                  
                  (84, {'type': 'content', 'contents': '\xa0 '})
              ],
            }
        ]
    }

The above example is an event for the service BBC ONE, broadcast at 10:06 GMT on
22nd December 2006. It describes a 'present-following' event that doesn't start
until 11:00 GMT. It is therefore describing the 'next' programme that will be
on the channel/service.

If this data is sent on through a PrettifyEventInformationTable component,
then the equivalent output is a string containing this (again, abridged for
brevity)::

    EIT received:
        Table ID                      : 78
        Table is valid for            : CURRENT (valid)
        Actual or Other n/w           : ACTUAL
        Present-Following or Schedule : Present-Following
        Transport stream id           : 4100
        Original network id           : 9018
        Events:
            Service id : 4164
                Running status         : 1 (NOT RUNNING)
                Start datetime (UTC)   : 2006-12-22 11:00:00
                Duration               : 00:30:00 (hh:mm:ss)
                Scrambled?             : NO
                Event descriptors:
                    Descriptor 0x4d : short_event
                        language_code : 'eng'
                        name : 'To Buy or Not to Buy'
                        text : 'Series that gives buyers the chance to test-drive a property before they buy it. Sarah Walker and Simon Rimmer are in Birmingham, helping a pair of property professionals. [S]'
                    Descriptor 0x50 : component
                        component_tag : 1
                        component_type : 3
                        content,type : ('video', '16:9 aspect ratio without pan vectors, 25 Hz')
                        language_code : '   '
                        stream_content : 1
                        text : 'Video 1'
                    Descriptor 0x50 : component
                        component_tag : 2
                        component_type : 3
                        content,type : ('audio', 'stereo (2 channel)')
                        language_code : 'eng'
                        stream_content : 2
                        text : 'Audio 2'
                    Descriptor 0x50 : component
                        component_tag : 5
                        component_type : 16
                        content,type : ('DVB subtitles (normal)', 'with no monitor aspect ratio criticality')
                        language_code : '   '
                        stream_content : 3
                        text : 'Subtitling 5'
                    Descriptor 0x50 : component
                        component_tag : 6
                        component_type : 1
                        content,type : (4, 1)
                        language_code : '   '
                        stream_content : 4
                        text : 'Data 6'

                    .....

                    Descriptor 0x54 : content
                        contents : '\xa0 '

ParseEventInformationTable can collect the sections of, and then parse the
various types of EIT table simultaneously.

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.



SimplifyEIT
~~~~~~~~~~~



Behaviour
---------

Send parsed event information data to the "inbox" inbox, and individual events,
in a simplified form, will be sent out the "outbox" outbox one at a time. For
example::

    {
        'event_id'       : 8735,
        'when'           : 'NEXT',
        'startdate'      : [2006, 12, 22],
        'starttime'      : [11, 0, 0],
        'duration'       : (0, 30, 0),
        'service'        : 4164,
        'transportstream': 4100,
        'language_code'  : 'eng',
        'name'           : 'To Buy or Not to Buy',
        'description'    : 'Series that gives buyers the chance to test-drive a property before they buy it. Sarah Walker and Simon Rimmer are in Birmingham, helping a pair of property professionals. [S]'
    }

The possible values of the 'when' field are:

* "NOW"        -- describes a programme that is happening NOW
* "NEXT"       -- describes a programme that follows the one happening now
* "SCHEDULED"  -- part of a schedule describing programmes happening over the next few days
    
If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

from Kamaelia.Support.DVB.Descriptors import parseDescriptor
from Kamaelia.Support.DVB.CRC import dvbcrc
from Kamaelia.Support.DVB.DateTime import parseMJD, unBCD


EIT_PID = 0x12

def ParseEventInformationTable_Subset( actual_presentFollowing = True,
                                       other_presentFollowing  = False,
                                       actual_schedule         = False,
                                       other_schedule          = False,
                   ):
    """\
    ParseEventInformationTable_Subset([actual_presentFollowing][,other_presentFollowing][,actual_schedule][,other_schedule] ) -> new ParseEventInformationTable component

    Returns a ParseEventInformationTable component, configured to parse the
    table types specified, and ignore all others.
    
    Keyword arguments::

    - actual_presentFollowing  -- If True, parse 'present-following' data for this multiplex (default=True)
    - other_presentFollowing   -- If True, parse 'present-following' data for other multiplexes (default=False)
    - actual_schedule          -- If True, parse 'schedule' data for this multiplex (default=False)
    - other_schedule           -- If True, parse 'schedule' data for other multiplexes (default=False)
    """
    acceptTables = {}
    if actual_presentFollowing:
        acceptTables[0x4e] = ("ACTUAL", True)
    if other_presentFollowing:
        acceptTables[0x4f] = ("OTHER", True)
    if actual_schedule:
        for x in range(0x50,0x60):
            acceptTables[x] = ("ACTUAL", False)
    if other_schedule:
        for x in range(0x60,0x70):
            acceptTables[x] = ("OTHER", False)
    return ParseEventInformationTable(acceptTables = acceptTables)


class ParseEventInformationTable(component):
    """\
    ParseEventInformationTable([acceptTables]) -> new ParseEventInformationTable component.

    Send reconstructed PSI table sections to the "inbox" inbox. When a complete
    table is assembled and parsed, the result is sent out of the "outbox" outbox
    as a dictionary.
    
    Doesn't emit anything again until the version number of the table changes.

    Use ParseEventInformationTable_Subset for simpler initialisation with
    convenient presets.
    
    Keyword arguments::

    - acceptTables  - dict of (table_id,string_description) mappings for tables to be accepted (default={0x4e:("ACTUAL",True)})
    """
    Inboxes = { "inbox" : "DVB PSI Packets from a single PID containing EIT table sections",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Parsed EIT table (only when it changes)",
                 "signal" : "Shutdown signalling",
               }
               
    def __init__(self, acceptTables = None):
        super(ParseEventInformationTable,self).__init__()
        
        if not acceptTables:
            acceptTables = {}
            acceptTables[0x4e] = ("ACTUAL", True)
            acceptTables[0x4f] = ("OTHER", True)
            for x in range(0x50,0x60):
                acceptTables[x] = ("ACTUAL", False)
            for x in range(0x60,0x70):
                acceptTables[x] = ("OTHER", False)
                
        self.acceptTables = acceptTables

    def parseTableSection(self, index, section):
        (table_id, service_id, current_next, transport_stream_id, original_network_id) = index
        msg = { "table_type"          : "EIT",
                "table_id"            : table_id,
                "actual_other"        : self.acceptTables[table_id][0],
                "is_present_following": self.acceptTables[table_id][1],
                "current"             : current_next,
                "transport_stream_id" : transport_stream_id,
                "original_network_id" : original_network_id,
                "events"              : [],
              }
        
        (data,section_length) = section
            
        service_id = (ord(data[3])<<8) + ord(data[4])
            
        i=14
        while i < section_length+3-4:
            e = [ord(data[x]) for x in range(i+0,i+12)]
            
            event = { "service_id" : service_id }
            
            event["event_id"] = (e[0]<<8) + e[1]
            # ( Y,M,D, HH,MM,SS )
            event["starttime"] = list( parseMJD((e[2]<<8) + e[3]) )
            event["starttime"].extend( [unBCD(e[4]), unBCD(e[5]), unBCD(e[6])] )
            event["duration"] = unBCD(e[7]), unBCD(e[8]), unBCD(e[9])
            event["running_status"] = (e[10] >> 5) & 0x07
            event["free_CA_mode"] = e[10] & 0x10
            
            descriptors_length = ((e[10]<<8) + e[11]) & 0x0fff
            event["descriptors"] = []
            i=i+12
            descriptors_end = i + descriptors_length
            while i < descriptors_end:
                descriptor,i = parseDescriptor(i,data)
                event['descriptors'].append(descriptor)
                
            msg["events"].append(event)
        
        return  msg
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False
    
    def main(self):
        # initialise buffers
        # ...for holding table sections (until we get  complete table)
        
        # indexed by (table_id, current_next, transport_stream_id, original_network_id)
        sections_found = {}
        latest_versions = {}
        last_section_numbers = {}
        
        while not self.shutdown():
             
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                
                # extract basic info from this PSI packet - enough to work
                # out what table it is; what section, and the version
                e = [ord(data[i]) for i in range(0,3) ]
                
                table_id = e[0]
                if table_id not in self.acceptTables.keys():
                    continue
                
                syntax = e[1] & 0x80
                if not syntax:
                    continue
                section_length = ((e[1]<<8) + e[2]) & 0x0fff
                
                # now were reasonably certain we've got a correct packet
                # we'll convert the rest of the packet
                e = [ord(data[i]) for i in range(0,12) ]
                
                service_id = (e[3]<<8) + e[4]
                
                version = (e[5] & 0x3e)  # no need to >> 1
                current_next = e[5] & 0x01
                section_number = e[6]
                last_section_number = e[7]

                transport_stream_id = (e[8]<<8) + e[9]
                original_network_id  = (e[10]<<8) + e[11]
                
                index = (table_id, service_id, current_next, transport_stream_id, original_network_id)

                # if version number has changed, flush out all previously fetched tables
                crcpass = False
                if version != latest_versions.get(index,-1):
                    if not dvbcrc(data[:3+section_length]):
                        continue
                    else:
                        crcpass = True
                    latest_versions[index] = version
                    
                    sections_found[index] = [False]*(last_section_number+1)
                
#                 if index[0] == 0x50:
#                     print index, section_number
                if not sections_found[index][section_number]:
                    if crcpass or dvbcrc(data[:3+section_length]):
                        
                        sections_found[index][section_number] = True
                        
                        # because of interesting decisions regarding subtable segments
                        # in the spec (EN 300 468, page 22) we have no way of knowing if
                        # we have received the whole table, so we're just going to parse
                        # each fragment we get and output it (if we've not seen it before)
                        tablesection = self.parseTableSection(index, (data, section_length))
#                       print table['actual_other'], table['pf_schedule']
                        self.send( tablesection, "outbox")
                    else:
                        pass  # ignore data with a bad crc
                        
            self.pause()
            yield 1


class SimplifyEIT(component):
    """\
    SimplifyEIT() -> new SimplifyEIT component.

    Send parsed EIT messages to the "inbox" inbox, and individual, simplified
    events will be sent out the "outbox" outbox.
    """
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False
    
    def main(self):
        while not self.shutdown():
            
            while self.dataReady("inbox"):
                eventset = self.recv("inbox")
                
                for event in eventset['events']:
                    
                    if eventset['is_present_following']: # is now&next information
                        if event['running_status'] in [1,2]:
                            when = "NEXT"
                        elif event['running_status'] in [3,4]:
                            when = "NOW"
                        else:
                            print "pf",event['running_status']
                    else: # is schedule data
                        if event['running_status'] in [0,1,2]:
                            when = "SCHEDULED"
                        elif event['running_status'] in [3,4]:
                            when = "NOW"
                        else:
                            print "sched",event['running_status']
                    
                    name        = ""
                    description = ""
                    language    = ""
                    for dtype, descriptor in event['descriptors']:
                        if dtype == 77:        # descriptor['type'] == "short_event":
                            name = descriptor['name']
                            description = descriptor['text']
                            language    = descriptor['language_code']
                    
                    
                    msg = { 'service'   : event['service_id'],
                            'event_id'  : event['event_id'],
                            'when'      : when,
                            'startdate' : event['starttime'][0:3],
                            'starttime' : event['starttime'][3:6],
                            'duration'  : event['duration'],
                            'transportstream' : eventset['transport_stream_id'],
                            'name'            : name,
                            'description'     : description,
                            'language_code'   : language,
                          }
                    self.send(msg,"outbox")
                
            self.pause()
            yield 1
            

__kamaelia_components__ = ( ParseEventInformationTable,
                            SimplifyEIT, )
__kamaelia_prefabs__    = ( ParseEventInformationTable_Subset, )
            
if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
    from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyEventInformationTable

    from Kamaelia.Device.DVB.NowNext import NowNextProgrammeJunctionDetect
    from Kamaelia.Device.DVB.NowNext import NowNextServiceFilter
    
    import dvb3.frontend
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    demo="Now and next"
#    demo="All schedule info"
    
    if demo == "Now and next":
        Pipeline( DVB_Multiplex(505833330.0/1000000.0, [EIT_PID], feparams),
                  DVB_Demuxer({ EIT_PID:["outbox"]}),
                  ReassemblePSITables(),
                  ParseEventInformationTable_Subset(True,False,False,False), # now and next for this mux only
                  SimplifyEIT(),
                  NowNextProgrammeJunctionDetect(),
                  NowNextServiceFilter(4164),
                  ConsoleEchoer(),
                ).run()
    
    elif demo == "All schedule info":
        Pipeline( DVB_Multiplex(505833330.0/1000000.0, [EIT_PID], feparams),
                  DVB_Demuxer({ EIT_PID:["outbox"]}),
                  ReassemblePSITables(),
                  ParseEventInformationTable_Subset(True,True,True,True), # now and next and schedules for this and other multiplexes
                  PrettifyEventInformationTable(),
                  ConsoleEchoer(),
                ).run()

