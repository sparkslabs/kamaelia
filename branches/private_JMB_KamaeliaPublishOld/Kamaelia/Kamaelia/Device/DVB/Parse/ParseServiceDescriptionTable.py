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
Parsing Service Description Tables in DVB streams
=================================================

ParseServiceDescriptionTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs a dictionary containing the data in the table.

The purpose of the SDT and details of the fields within in are defined in the
DVB SI specification, including the possible 'descriptor' fields that feature in
the table:

- ETSI EN 300 468 
  "Digital Video Broadcasting (DVB); Specification for Service Information (SI)
  in DVB systems"
  ETSI / EBU (DVB group)

See Kamaelia.Support.DVB.Descriptors for information on how they are parsed.



Example Usage
~~~~~~~~~~~~~

A simple pipeline to receive, parse and display the Service Description Table
applying to the transport stream (MUX) being received ("actual TS")::

    FREQUENCY = 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    SID_Actual_PID = 0x11
    
    Pipeline( DVB_Multiplex(FREQUENCY, [SID_Actual_PID], feparams),
              DVB_Demuxer({ SID_Actual_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseServiceDescriptionTable_ActualTS(),
              PrettifyServiceDescriptionTable(),
              ConsoleEchoer(),
            ).run()

A simple pipeline to receive and parse the Service Description Table then
convert it to a simple list mapping service names to service ids::

    Pipeline( DVB_Multiplex(FREQUENCY, [SID_Actual_PID], feparams),
              DVB_Demuxer({ SID_Actual_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseServiceDescriptionTable_ActualTS(),
              SDT_to_SimpleServiceList(),
              ConsoleEchoer(),
            ).run()



ParseServiceDescriptionTable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Behaviour
---------

At initialisation, specify whether you want ParseServiceDescriptionTables to
parse 'actual' or 'other' tables (or both). 'Actual' tables describe services
within the actual transport stream the table is it. 'Other' tables describe
services carried in other transport streams - ie. broadcast in a different MUX
in the same network. For example::

    ParseServiceDescriptionTable(acceptTables = {0x42:"ACTUAL",0x46:"OTHER"})

There are shorthands available for the various combinations::

    ParseServiceDescriptionTable_ActualTS()
    ParseServiceDescriptionTable_OtherTS()
    ParseServiceDescriptionTable_ActualAndOtherTS():

Send reconstructed PSI table 'sections' to the "inbox" inbox. When all sections
of the table have arrived, ParseServiceDescriptionTable will parse the table and
send it out of its "outbox" outbox.

If the table is unchanged since last time it was parsed, then it will not be
sent out. Parsed tables are only sent out when they are new or have just
changed.

The parsed table is sent out as a dictionary data structure, similar to this
(the 'streams' list here is abridged for brevity)::

    {
        'actual_other'        : 'ACTUAL',
        'table_type'          : 'SDT',
        'current'             : 1,
        'original_network_id' : 9018,
        'table_id'            : 66,
        'services': {
            4228: { 'running_status'       : 4,
                    'free_CA_mode'         : 0,
                    'eit_present_following': 1,
                    'eit_schedule'         : 2,
                    'descriptors': [
                        ( 72, { 'type': 'service',
                                'service_name': 'BBC TWO',
                                'service_type': 'digital television service',
                                'service_provider_name': 'BBC'
                              } ),
                        (115, { 'type': 'UNKNOWN',
                                'contents': 'fp.bbc.co.uk'
                              } )
                    ] },
            4164: { 'running_status'       : 4,
                    'free_CA_mode'         : 0,
                    'eit_present_following': 1,
                    'eit_schedule'         : 2,
                    'descriptors': [
                        ( 72, { 'type': 'service',
                                'service_name': 'BBC ONE',
                                'service_type': 'digital television service',
                                'service_provider_name': 'BBC'
                              } ),
                        (115, { 'type': 'UNKNOWN',
                                'contents': 'fp.bbc.co.uk'
                              } )
                    ] },

            .....

            4671: { 'running_status': 4,
                    'free_CA_mode'         : 0,
                    'eit_present_following': 1,
                    'eit_schedule'         : 2,
                    'descriptors': [
                        ( 72, { 'type': 'service',
                                'service_name': 'CBBC Channel',
                                'service_type': 'digital television service',
                                'service_provider_name': 'BBC'
                              } ),
                        (115, { 'type': 'UNKNOWN',
                                'contents': 'fp.bbc.co.uk'
                              } )
                    ] }
            },
        'transport_stream_id': 4100
    }
    
This table contains information about the services within the transport stream.
It lists the services (channels) including their names. types, and the fact that
there is now & next data (eit_present_following) and Electronic Programme Guide
(eit_schedule) data available for each of them.

This is part of an instantaneous snapshot of the SDT broadcast from Crystal
Palace MUX 1 (505.8MHz) in the UK on 21th Dec 2006.

If this data is sent on through a PrettifyServiceDescriptionTable component,
then the equivalent output is a string containing the following (again, abridged
here for brevity)::

    Table ID           : 66
    Table is valid for : CURRENT (valid)
    Actual or Other n/w: ACTUAL
    Transport stream id: 4100
    Original network id: 9018
    Services:
        Service id : 4228
            EIT present_following? : YES
            EIT schedule?          : YES
            Running status         : 4 (RUNNING)
            Scrambled?             : NO
            Service descriptors:
                Descriptor 0x48 : service
                    service_name : 'BBC TWO'
                    service_provider_name : 'BBC'
                    service_type : 'digital television service'
                Descriptor 0x73 : UNKNOWN
                    contents : 'fp.bbc.co.uk'
        Service id : 4164
            EIT present_following? : YES
            EIT schedule?          : YES
            Running status         : 4 (RUNNING)
            Scrambled?             : NO
            Service descriptors:
                Descriptor 0x48 : service
                    service_name : 'BBC ONE'
                    service_provider_name : 'BBC'
                    service_type : 'digital television service'
                Descriptor 0x73 : UNKNOWN
                    contents : 'fp.bbc.co.uk'

        .....

        Service id : 4671
            EIT present_following? : YES
            EIT schedule?          : YES
            Running status         : 4 (RUNNING)
            Scrambled?             : NO
            Service descriptors:
                Descriptor 0x48 : service
                    service_name : 'CBBC Channel'
                    service_provider_name : 'BBC'
                    service_type : 'digital television service'
                Descriptor 0x73 : UNKNOWN
                    contents : 'fp.bbc.co.uk'

ParseServiceDescriptionTable can collect the sections of, and then parse, both
'current' and 'next' tables simultaneously.

See the "DVB SI" specifications for information on the purposes of the
descriptor fields that appear in various parts of this table.

See Kamaelia.Support.DVB.Descriptors for information on how each is parsed.

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.



How does it work?
-----------------

ParseServiceDescriptionTable logs all the table sections it receives, until it
determines it has the complete set; then it parses them.

If the version number field in any table section changes, then the log is
cleared, and the component starts collecting the sections again from scratch.



SDT_to_SimpleServiceList
~~~~~~~~~~~~~~~~~~~~~~~~



Behaviour
---------

Send parsed service description tables to this component's "inbox" inbox and
a dictionary mapping service names to service ids will be sent out the "outbox"
outbox. For example::

    { 'BBCi'        : 4479,
      'BBC ONE'     : 4164,
      'BBC TWO'     : 4228,
      'CBBC Channel': 4671,
      'BBC NEWS 24' : 4415,
      'BBC THREE'   : 4351
    }

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

from Kamaelia.Support.DVB.Descriptors import parseDescriptor
from Kamaelia.Support.DVB.CRC import dvbcrc

SDT_PID = 0x11


def ParseServiceDescriptionTable_ActualTS():
    """\
    ParseServiceDescriptionTable_ActualTS() -> new ParseServiceDescriptionTable component.

    Instantiates a ParseServiceDescriptionTable component configured to parse
    'ACTUAL TS' tables only (table id 0x42)
    """
    return ParseServiceDescriptionTable(acceptTables = {0x42:"ACTUAL"})



def ParseServiceDescriptionTable_OtherTS():
    """\
    ParseServiceDescriptionTable_OtherTS() -> new ParseServiceDescriptionTable component.

    Instantiates a ParseServiceDescriptionTable component configured to parse
    'OTHER TS' tables only (table id 0x46)
    """
    return ParseServiceDescriptionTable(acceptTables = {0x46:"OTHER"})



def ParseServiceDescriptionTable_ActualAndOtherTS():
    """\
    ParseServiceDescriptionTable_ActualAndOtherTS() -> new ParseServiceDescriptionTable component.

    Instantiates a ParseServiceDescriptionTable component configured to parse
    both 'ACTUAL' and 'OTHER TS' tables (table ids 0x42 and 0x46)
    """
    return ParseServiceDescriptionTable(acceptTables = {0x42:"ACTUAL",0x46:"OTHER"})



class ParseServiceDescriptionTable(component):
    """\
    ParseServiceDescriptionTable([acceptTables]) -> new ParseServiceDescriptionTable component.

    Send reconstructed PSI table sections to the "inbox" inbox. When a complete
    table is assembled and parsed, the result is sent out of the "outbox" outbox
    as a dictionary.
    
    Doesn't emit anything again until the version number of the table changes.
    
    Keyword arguments::

    - acceptTables  - dict of (table_id,string_description) mappings for tables to be accepted (default={0x42:"ACTUAL",0x46:"OTHER"})
    """
    Inboxes = { "inbox" : "DVB PSI Packets from a single PID containing SDT table sections",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Parsed PMT table (only when it changes)",
                 "signal" : "Shutdown signalling",
               }
               
    def __init__(self, acceptTables = {0x42:"ACTUAL",0x46:"OTHER"}):
        super(ParseServiceDescriptionTable,self).__init__()
        self.acceptTables = acceptTables

    def parseTable(self, index, sections):
        (table_id, current_next, transport_stream_id, original_network_id) = index
        
        msg = { "table_type"          : "SDT",
                "table_id"            : table_id,
                "actual_other"        : self.acceptTables[table_id],
                "current"             : current_next,
                "transport_stream_id" : transport_stream_id,
                "original_network_id" : original_network_id,
              }
        services = {}
        
        for (data,section_length) in sections:
            
            i=11
            while i < section_length+3-4:
                service_id = (ord(data[i])<<8) + ord(data[i+1])
                service = {}
                
                lo = ord(data[i+2])
                service['eit_schedule']          = lo & 0x02
                service['eit_present_following'] = lo & 0x01
                hi = ord(data[i+3])
                service['running_status']        = hi >> 5
                service['free_CA_mode']          = hi & 0x10
                
                descriptors_length = ((hi<<8) + ord(data[i+4])) & 0x0fff
                i = i + 5
                descriptors_end = i + descriptors_length
                service['descriptors'] = []
                while i < descriptors_end:
                    descriptor,i = parseDescriptor(i,data)
                    service['descriptors'].append(descriptor)
                    
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
        
        # indexed by (table_id, current_next, transport_stream_id, original_network_id)
        sections = {}
        latest_versions = {}
        last_section_numbers = {}
        missing_sections_count = {}
        
        while not self.shutdown():
             
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                
                # extract basic info from this PSI packet - enough to work
                # out what table it is; what section, and the version
                e = [ord(data[i]) for i in (0,1,2,3,4,5,6,7,8,9) ]

                table_id = e[0]
                if table_id not in self.acceptTables.keys():
                    continue
                
                syntax = e[1] & 0x80
                if not syntax:
                    continue
                
                section_length = ((e[1]<<8) + e[2]) & 0x0fff
                
                version = (e[5] &0x3e)  # no need to >> 1
                current_next = e[5] & 0x01
                section_number = e[6]
                last_section_number = e[7]

                transport_stream_id = (e[3]<<8) + e[4]
                original_network_id  = (e[8]<<8) + e[9]
                
                index = (table_id, current_next, transport_stream_id, original_network_id)

                # if version number has changed, flush out all previously fetched tables
                crcpass = False
                if version != latest_versions.get(index,-1):
                    if not dvbcrc(data[:3+section_length]):
                        continue
                    else:
                        crcpass = True
                    latest_versions[index] = version
                    
                    sections[index] = [None]*(last_section_number+1)
                    missing_sections_count[index] = last_section_number+1
                
                if sections[index][section_number] == None:
                    if crcpass or dvbcrc(data[:3+section_length]):
                        
                        sections[index][section_number] = (data, section_length)
                        missing_sections_count[index] -= 1
                        
                        # see if we have all sections of the table
                        # if we do, send the whole bundle onwards
                        if missing_sections_count[index] == 0:
                            table = self.parseTable(index, sections[index])
                            self.send( table, "outbox")
                        
            self.pause()
            yield 1


class SDT_to_SimpleServiceList(component):
    """\
    SDT_to_SimpleServiceList() -> new SDT_to_SimpleServiceList component.

    Converts parsed Service Description Tables to a simplified list of services.
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
                sdt = self.recv("inbox")
                s =dict([(service['descriptors'][0][1]['service_name'],sid) for (sid,service) in sdt['services'].items()])
                self.send(s,"outbox")
            self.pause()
            yield 1

            
__kamaelia_components__ = ( ParseServiceDescriptionTable,
                            SDT_to_SimpleServiceList )
__kamaelia_prefabs__    = ( ParseServiceDescriptionTable_ActualTS,
                            ParseServiceDescriptionTable_OtherTS,
                            ParseServiceDescriptionTable_ActualAndOtherTS, )


if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
    from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyServiceDescriptionTable
    
    import dvb3.frontend
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    Pipeline( DVB_Multiplex(505833330.0/1000000.0, [SDT_PID], feparams),
              DVB_Demuxer({ SDT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseServiceDescriptionTable_ActualAndOtherTS(),
              PrettifyServiceDescriptionTable(),
              ConsoleEchoer(),
            ).run()

