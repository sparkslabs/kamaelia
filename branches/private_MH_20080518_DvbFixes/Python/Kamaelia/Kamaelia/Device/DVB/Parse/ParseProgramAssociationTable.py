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
Parsing Program Association Tables in DVB streams
=================================================

ParseProgramAssociationTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs a dictionary containing the data in the table.

The purpose of the PAT and details of the fields within in are defined in the
MPEG systems specification:

- ISO/IEC 13818-1 (aka "MPEG: Systems")
  "GENERIC CODING OF MOVING PICTURES AND ASSOCIATED AUDIO: SYSTEMS" 
  ISO / Motion Picture Experts Group



Example Usage
-------------

A simple pipeline to receive, parse and display the Program Association Table in
a multiplex::

    FREQUENCY = 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    PAT_PID = 0x0
    
    Pipeline( DVB_Multiplex(FREQUENCY, [PAT_PID], feparams),
              DVB_Demuxer({ PAT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseProgramAssociationTable(),
              PrettifyProgramAssociationTable(),
              ConsoleEchoer(),
            ).run()
    


Behaviour
---------

Send reconstructed PSI table 'sections' to the "inbox" inbox. When all sections
of the table have arrived, ParseProgramAssociationTable will parse the table
and send it out of its "outbox" outbox.

If the table is unchanged since last time it was parsed, then it will not be
sent out. Parsed tables are only sent out when they are new or have just
changed.

The parsed table is sent out as a dictionary data structure, like this::

    {
        'table_id'         : 0
        'table_type'       : 'PAT',
        'current'          : 1,
        'NIT_PID'          : 16,
        'transport_streams': { 4100: { 4228: 4228,
                                       4351: 4351,
                                       4479: 4479,
                                       4164: 4164,
                                       4415: 4415,
                                       4671: 4671
                                     }
                             },
    }

This is an instantaneous snapshot of the PAT for Crystal Palace MUX 1
transmission (505.8MHz) in the UK on 20th Dec 2006. If this data is sent on
through a PrettifyProgramAssociationTable component, then the equivalent output
is a string containing this::

        PAT received:
        Table ID           : 0
        Table is valid for : CURRENT (valid)
        NIT is in PID      : 16
        For transport stream id : 4100
            For service 4228 : PMT is in PID 4228
            For service 4351 : PMT is in PID 4351
            For service 4479 : PMT is in PID 4479
            For service 4164 : PMT is in PID 4164
            For service 4415 : PMT is in PID 4415
            For service 4671 : PMT is in PID 4671

ParseProgramAssociationTable can collect the sections of, and then parse, both
'current' and 'next' tables simultaneously.

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.



How does it work?
-----------------

ParseProgramAssociationTable logs all the table sections it receives, until it
determines it has the complete set; then it parses them.

If the version number field in any table section changes, then the log is
cleared, and the component starts collecting the sections again from scratch.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

from Kamaelia.Support.DVB.Descriptors import parseDescriptor
from Kamaelia.Support.DVB.CRC import dvbcrc

PAT_PID = 0x00


class ParseProgramAssociationTable(component):
    """
    ParseProgramAssociationTable() -> new ParseProgramAssociationTable component.

    Send reconstructed PSI table sections to the "inbox" inbox. When a complete
    table is assembled and parsed, the result is sent out of the "outbox" outbox
    as a dictionary.
    
    Doesn't emit anything again until the version number of the table changes.
    
    Outputs both 'current' and 'next' tables.
    """
    Inboxes = { "inbox" : "DVB PSI Packets containing PAT table sections",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Parsed PAT table (only when it changes)",
                 "signal" : "Shutdown signalling",
               }
    
    def parseTable(self, table_id, current_next, sections):
        
        msg = { "table_type"        : "PAT",
                "table_id"          : table_id,
                "current"           : current_next,
              }
        streams = {}
        
        for (data,section_length) in sections:
            
            transportstream_id = (ord(data[3])<<8) + ord(data[4])
            try:
                services = streams[transportstream_id]
            except KeyError:
                services = {}
            lo = ord(data[5])
            
            i=8
            section_end = section_length+3-4
            while i < section_end:
                service_id = (ord(data[i])<<8) + ord(data[i+1])
                pid = (ord(data[i+2])<<8) + ord(data[i+3])
                pid = pid & 0x1fff
                if service_id==0:
                    msg['NIT_PID'] = pid
                else:
                    services[service_id] = pid
                i+=4
                
            # append to any existing records for this transportstream_id
            # (or start a new list)
            streams[transportstream_id] = services
    
        msg['transport_streams'] = streams
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
                e = [ord(data[i]) for i in (0,1,2) ]

                table_id = e[0]
                if table_id != 0:
                    continue
                
                syntax = e[1] & 0x80
                if not syntax:
                    continue
                
                section_length = ((e[1]<<8) + e[2]) & 0x0fff
                
                # now were reasonably certain we've got a correct packet
                # we'll convert the rest of the packet
                e = [ord(data[i]) for i in (0,1,2,5,6,7) ]
                
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
                    

__kamaelia_components__ = ( ParseProgramAssociationTable, )

if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
    from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyProgramAssociationTable
    
    import dvb3.frontend
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }

    Pipeline( DVB_Multiplex(505833330.0/1000000.0, [PAT_PID], feparams),
              DVB_Demuxer({ PAT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseProgramAssociationTable(),
              PrettifyProgramAssociationTable(),
              ConsoleEchoer(),
            ).run()
            