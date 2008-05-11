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
=================================================
Parsing Program Map Tables in DVB streams
=================================================

ParseProgramMapTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs a dictionary containing the data in the table.

The purpose of the PMT and details of the fields within in are defined in the
MPEG systems specification:

- ISO/IEC 13818-1 (aka "MPEG: Systems")
  "GENERIC CODING OF MOVING PICTURES AND ASSOCIATED AUDIO: SYSTEMS" 
  ISO / Motion Picture Experts Group

The possible 'descriptor' fields that feature in the table are explained in the
DVB SI specification:

- ETSI EN 300 468 
  "Digital Video Broadcasting (DVB); Specification for Service Information (SI)
  in DVB systems"
  ETSI / EBU (DVB group)

See Kamaelia.Support.DVB.Descriptors for information on how they are parsed.



Example Usage
-------------

A simple pipeline to receive, parse and display a particular Program Map Table
in a multiplex, carried in packets with packet id 4228::

    FREQUENCY = 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    PMT_PID = 4228
    
    Pipeline( DVB_Multiplex(FREQUENCY, [PMT_PID], feparams),
              DVB_Demuxer({ PMT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseProgramMapTable(),
              PrettifyProgramMapTable(),
              ConsoleEchoer(),
            ).run()



Behaviour
---------

Send reconstructed PSI table 'sections' to the "inbox" inbox. When all sections
of the table have arrived, ParseProgramMapTable will parse the table and send it
out of its "outbox" outbox.

If the table is unchanged since last time it was parsed, then it will not be
sent out. Parsed tables are only sent out when they are new or have just
changed.

The parsed table is sent out as a dictionary data structure, similar to this
(the 'streams' list here is abridged for brevity)::

    {
        'table_id' : 2,
        'table_type' : 'PMT',
        'current'  : 1,
        'services' : {
            4228: { 'video_pid'   : 610,
                    'audio_pid'   : 611,
                    'descriptors' : [],
                    'pcr_pid'     : 610,
                    'streams'     : [
                        { 'pid'         : 610,
                          'type'        : 2,
                          'descriptors' : [
                              ( 82, { 'type' : 'stream_identifier', 'component_tag' : 1 } )
                          ]
                        },
                        { 'pid'         : 611,
                          'type'        : 3,
                          'descriptors' : [
                              ( 10, { 'type' : 'ISO_639', 'entries' : [ { 'audio_type': '', 'language_code': 'eng' } ] } ),
                              ( 82, { 'type' : 'stream_identifier', 'component_tag' : 2 } )
                          ]
                        },
    
                        .....
    
                        { 'pid'        : 1010,
                          'type'       : 11,
                          'descriptors': [
                              ( 82, { 'type' : 'stream_identifier', 'component_tag' : 112 } )
                          ]
                        }
                    ]
                }
        }
    }

This table contains information about one service (with service id 4228), and
describes many streams in that service. ParseProgramMapTable has identified
that packets with packet id 610 and 611 probably contain the primary video and
audio making up this service.

This is part of an instantaneous snapshot of a PMT broadcast from Crystal Palace
MUX 1 (505.8MHz) in the UK on 20th Dec 2006.

If this data is sent on through a PrettifyProgramMapTable component, then the
equivalent output is a string containing the following (again, abridged here for
brevity)::

    PMT received:
        Table ID           : 2
        Table is valid for : CURRENT (valid)
        Services:
            Service id : 4228
            Program Clock Reference in PID : 610
            Service Descriptors:
                <<NONE>>
            Streams in service:
                Type : 2
                    PID  : 610
                    Stream Descriptors:
                        Descriptor 0x52 : stream_identifier
                            component_tag : 1
                Type : 3
                    PID  : 611
                    Stream Descriptors:
                        Descriptor 0xa : ISO_639
                            entries : [{'audio_type': '', 'language_code': 'eng'}]
                        Descriptor 0x52 : stream_identifier
                            component_tag : 2

                .....

                Type : 11
                    PID  : 1010
                    Stream Descriptors:
                        Descriptor 0x52 : stream_identifier
                            component_tag : 112

ParseProgramMapTable can collect the sections of, and then parse, both
'current' and 'next' tables simultaneously.

See the "MPEG Systems" and "DVB SI" specifications for information on the
purposes of the descriptor fields that appear in various parts of this table.

See Kamaelia.Support.DVB.Descriptors for information on how each is parsed.

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.



How does it work?
-----------------

ParseProgramMapTable logs all the table sections it receives, until it
determines it has the complete set; then it parses them.

If the version number field in any table section changes, then the log is
cleared, and the component starts collecting the sections again from scratch.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

from Kamaelia.Support.DVB.Descriptors import parseDescriptor
from Kamaelia.Support.DVB.CRC import dvbcrc

class ParseProgramMapTable(component):
    """
    ParseProgramMapTable() -> new ParseProgramMapTable component.

    Send reconstructed PSI table sections to the "inbox" inbox. When a complete
    table is assembled and parsed, the result is sent out of the "outbox" outbox
    as a dictionary.
    
    Doesn't emit anything again until the version number of the table changes.
    
    Outputs both 'current' and 'next' tables.
    """
    Inboxes = { "inbox" : "DVB PSI Packets from a single PID containing PMT table sections",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Parsed PMT table (only when it changes)",
                 "signal" : "Shutdown signalling",
               }

    def parseTable(self, table_id, current_next, sections):
        
        msg = { "table_type"        : "PMT",
                "table_id"          : table_id,
                "current"           : current_next,
              }
        services = {}
        
        for (data,section_length) in sections:
            service_id = (ord(data[3])<<8) + ord(data[4])
            service = {}
            
            service['pcr_pid'] = ( (ord(data[8])<<8) + ord(data[9]) ) & 0x1fff
            
            prog_info_length = ( (ord(data[10])<<8) + ord(data[11]) ) & 0x0fff
            i=12
            prog_info_end = i+prog_info_length
            service['descriptors'] = []
            while i < prog_info_end:
                print i,prog_info_end, len(data)
                descriptor,i = parseDescriptor(i,data)
                service['descriptors'].append(descriptor)
                
            service['streams'] = []
            while i < section_length+3-4:
                stream = {}
                stream['type'] = ord(data[i])
                stream['pid'] = ( (ord(data[i+1])<<8) + ord(data[i+2]) ) & 0x1fff
                
                es_info_length = ( (ord(data[i+3])<<8) + ord(data[i+4]) ) & 0x0fff
                i=i+5
                es_info_end = i+es_info_length
                stream['descriptors'] = []
                while i < es_info_end:
                    descriptor,i = parseDescriptor(i,data)
                    stream['descriptors'].append(descriptor)
                    
                service['streams'].append(stream)
                
                # a little bit of simplification here:
                if   stream['type'] in [3,4] and 'audio_pid' not in service:
                    service['audio_pid'] = stream['pid']
                elif stream['type'] in [1,2] and 'video_pid' not in service:
                    service['video_pid'] = stream['pid']
            
            services[service_id] = service
        msg['services'] = services
        
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
        # two sets of each buffer - one for 'next' and 'current' respectively
        sections = [ [],[] ]
        latest_versions = [-1,-1]
        last_section_numbers = [0,0]
        missing_sections_count = [0,0]
        
        while not self.shutdown():
             
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                
                # extract basic info from this PSI packet - enough to work
                # out what table it is; what section, and the version
                e = [ord(data[i]) for i in (0,1,2,5,6,7) ]

                table_id = e[0]
                if table_id != 2:
                    continue
                
                syntax = e[1] & 0x80
                if not syntax:
                    continue
                
                section_length = ((e[1]<<8) + e[2]) & 0x0fff
                
                version = (e[3] &0x3e)  # no need to >> 1
                current_next = e[3] & 0x01
                section_number = e[4]
                last_section_number = e[5]

                # if version number has changed, flush out all previously fetched tables
                crcpass = False
                if version != latest_versions[current_next]:
                    if not dvbcrc(data[:3+section_length]):
                        continue
                    else:
                        crcpass = True
                    latest_versions[current_next] = version
                    
                    sections[current_next] = [None]*(last_section_number+1)
                    missing_sections_count[current_next] = last_section_number+1
                
                if sections[current_next][section_number] == None:
                    if crcpass or dvbcrc(data[:3+section_length]):
                        
                        sections[current_next][section_number] = (data, section_length)
                        missing_sections_count[current_next] -= 1
                        
                        # see if we have all sections of the table
                        # if we do, send the whole bundle onwards
                        if missing_sections_count[current_next] == 0:
                            table = self.parseTable(table_id, current_next, sections[current_next])
                            self.send( table, "outbox")
                        
            self.pause()
            yield 1

__kamaelia_components__ = ( ParseProgramMapTable, )

if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
    from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyProgramMapTable
    
    import dvb3.frontend
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }

    PMT_PID = 4228    # "BBC TWO" on Crystal Palace transmitter in UK

    Pipeline( DVB_Multiplex(505833330.0/1000000.0, [PMT_PID], feparams),
              DVB_Demuxer({ PMT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseProgramMapTable(),
              PrettifyProgramMapTable(),
              ConsoleEchoer(),
            ).run()

