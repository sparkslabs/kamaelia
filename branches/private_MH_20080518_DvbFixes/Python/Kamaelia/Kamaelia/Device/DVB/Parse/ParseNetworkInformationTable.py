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
Parsing Network Information Tables in DVB streams
=================================================

ParseNetworkInformationTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs a dictionary containing the data in the table.

The purpose of the NIT and details of the fields within in are defined in the
DVB SI specification:

- ETSI EN 300 468 
  "Digital Video Broadcasting (DVB); Specification for Service Information (SI)
  in DVB systems"
  ETSI / EBU (DVB group)

See Kamaelia.Support.DVB.Descriptors for information on how they are parsed.



Example Usage
-------------

A simple pipeline to receive, parse and display the Network Information Table in
a multiplex::

    FREQUENCY = 505.833330
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    NIT_PID = 0x10
    
    Pipeline( DVB_Multiplex(FREQUENCY, [NIT_PID], feparams),
              DVB_Demuxer({ NIT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseNetworkInformationTable_ActualNetwork(),
              PrettifyNetworkInformationTable(),
              ConsoleEchoer(),
            ).run()



Behaviour
---------

At initialisation, specify whether you want ParseNetworkInformationTable to
parse 'actual' or 'other' tables (or both). 'Actual' tables describe transport
streams/multiplexes within the same actual networks that this table has been
broadcast in. 'Other' tables describe transport streams/multiplexes being
broadcast for other networks. For example: 'freeview' is a network in the UK
that broadcasts several multiplexes.

For example::

    ParseNetworkInformationTable(acceptTables = {0x40:"ACTUAL",0x41:"OTHER"})

There are shorthands available for the various combinations::

    ParseNetworkInformationTable_ActualNetwork()
    ParseNetworkInformationTable_OtherNetwork()
    ParseNetworkInformationTable_ActualAndOtherNetwork():

Send reconstructed PSI table 'sections' to the "inbox" inbox. When all sections
of the table have arrived, ParseNetworkInformationTable will parse the table
and send it out of its "outbox" outbox.

If the table is unchanged since last time it was parsed, then it will not be
sent out. Parsed tables are only sent out when they are new or have just
changed.

The parsed table is sent out as a dictionary data structure, like this (list of
transport streams abridged for marginally better brevity)::

    {
        'table_id'    : 64,
        'table_type'  : 'NIT',
        'current'     : 1,
        'actual_other': 'ACTUAL',
        'network_id'  : 12293,
        'descriptors': [ (64, {'type': 'network_name', 'network_name': 'Crystal Palace'} ) ]
        'transport_streams': [
            { 'transport_stream_id': 4100,
              'descriptors': [
                  ( 65, { 'type': 'service_list'
                          'services': [
                              {'service_type': ('digital television service',), 'service_id': 4164},
                              {'service_type': ('digital television service',), 'service_id': 4228},
                              {'service_type': ('digital television service',), 'service_id': 4351},
                              {'service_type': ('digital television service',), 'service_id': 4415},
                              {'service_type': ('digital television service',), 'service_id': 4479},
                              {'service_type': ('digital television service',), 'service_id': 4671}
                          ],
                        } ),
                  ( 90, { 'other_frequencies': 1,
                          'params': { 'inversion': 2,
                                      'transmission_mode': 0,
                                      'hierarchy_information': 0,
                                      'code_rate_LP': 3,
                                      'guard_interval': 0,
                                      'bandwidth': 0,
                                      'frequency': 505833330,
                                      'constellation': 1,
                                      'code_rate_HP': 3
                                    },
                          'type': 'terrestrial_delivery_system'
                        } ),
                  ( 98, { 'type': 'frequency_list',
                          'frequencies': [697833330, 690166670, 554000000]
                        } ),
                  ( 95, { 'type': 'private_data_specifier',
                          'private_data_specifier': 9018
                        } ),
                  (131, { 'type': 'logical_channel',
                          'mappings': { 4228: 2, 4351: 7, 4479: 105, 4164: 1, 4415: 80, 4671: 70 }
                        } )
              ],
              'original_network_id': 9018
            },

           .....

            { 'transport_stream_id': 24576,
              'descriptors': [
                  ( 65, { 'services': [
                              {'service_type': ('digital television service',), 'service_id': 25664},
                              {'service_type': ('digital television service',), 'service_id': 25728},
                              {'service_type': ('digital television service',), 'service_id': 25792},
                              {'service_type': ('digital television service',), 'service_id': 25856},
                              {'service_type': ('digital television service',), 'service_id': 25920},
                              {'service_type': ('digital radio sound service',), 'service_id': 26176},
                              {'service_type': ('digital radio sound service',), 'service_id': 26240},
                              {'service_type': ('digital radio sound service',), 'service_id': 26304},
                              {'service_type': ('digital radio sound service',), 'service_id': 26368},
                              {'service_type': ('digital radio sound service',), 'service_id': 26432},
                              {'service_type': ('digital radio sound service',), 'service_id': 26496},
                              {'service_type': ('digital radio sound service',), 'service_id': 26560},
                              {'service_type': ('digital radio sound service',), 'service_id': 26624},
                              {'service_type': ('digital radio sound service',), 'service_id': 26688},
                              {'service_type': ('data broadcast service',), 'service_id': 27008},
                              {'service_type': ('digital television service',), 'service_id': 27072},
                              {'service_type': ('digital television service',), 'service_id': 27136}
                          ],
                          'type': 'service_list'
                        } ),
                  ( 90, { 'other_frequencies': 1,
                          'params': { 'inversion': 2,
                                      'transmission_mode': 0,
                                      'hierarchy_information': 0,
                                      'code_rate_LP': 3,
                                      'guard_interval': 0,
                                      'bandwidth': 0,
                                      'frequency': 537833330,
                                      'constellation': 1,
                                      'code_rate_HP': 3
                                    },
                          'type': 'terrestrial_delivery_system'
                        } ),
                  ( 98, { 'frequencies': [738000000, 826000000, 834000000],
                          'type': 'frequency_list'
                        } ),
                  ( 95, { 'type': 'private_data_specifier',
                          'private_data_specifier': 9018
                        } ),
                  (131, { 'type': 'logical_channel',
                          'mappings': { 25664: 18,  25728: 21,  26496: 710, 26432: 717,
                                        26560: 711, 26624: 715, 26688: 716, 25792: 19,
                                        25856: 20,  25920: 22,  27008: 300, 27072: 31,
                                        27136: 29,  26176: 713, 26240: 712, 26304: 722,
                                        26368: 718
                                      }
                        } )
              ],
              'original_network_id': 9018
            }
          ],
    }
            
This is an instantaneous snapshot of the NIT for Crystal Palace MUX 1
transmission (505.8MHz) in the UK on 21th Dec 2006. It describes the each of
the transport streams being broadcast, including how to tune to them (frequency
and other parameters) and an overview of the services in each. It also describes
the mapping of channel numbers on the user's remote control, to service ids.

If this data is sent on through a PrettifyNetworkInformationTable component,
then the equivalent output is a string containing this (again, abridged for
brevity)::

    NIT received:
        Table ID           : 64
        Table is valid for : CURRENT (valid)
        Actual or Other n/w: ACTUAL
        Network ID         : 12293
        Network descriptors:
        Network Descriptors:
            Descriptor 0x40 : network_name
                network_name : 'Crystal Palace'
        Transport Stream:
            transport stream id : 4100
            original network id : 9018
            Transport Stream Descriptors:
                Descriptor 0x41 : service_list
                    services : [   {'service_type': ('digital television service',), 'service_id': 4164},
                                   {'service_type': ('digital television service',), 'service_id': 4228},
                                   {'service_type': ('digital television service',), 'service_id': 4351},
                                   {'service_type': ('digital television service',), 'service_id': 4415},
                                   {'service_type': ('digital television service',), 'service_id': 4479},
                                   {'service_type': ('digital television service',), 'service_id': 4671}]
                Descriptor 0x5a : terrestrial_delivery_system
                    other_frequencies : 1
                    params : {   'bandwidth': 0,
                                 'code_rate_HP': 3,
                                 'code_rate_LP': 3,
                                 'constellation': 1,
                                 'frequency': 505833330,
                                 'guard_interval': 0,
                                 'hierarchy_information': 0,
                                 'inversion': 2,
                                 'transmission_mode': 0}
                Descriptor 0x62 : frequency_list
                    frequencies : [697833330, 690166670, 554000000]
                Descriptor 0x5f : private_data_specifier
                    private_data_specifier : 9018
                Descriptor 0x83 : logical_channel
                    mappings : {4228: 2, 4351: 7, 4479: 105, 4164: 1, 4415: 80, 4671: 70}
    
        .....
    
        Transport Stream:
            transport stream id : 24576
            original network id : 9018
            Transport Stream Descriptors:
                Descriptor 0x41 : service_list
                    services : [   {'service_type': ('digital television service',), 'service_id': 25664},
                                   {'service_type': ('digital television service',), 'service_id': 25728},
                                   {'service_type': ('digital television service',), 'service_id': 25792},
                                   {'service_type': ('digital television service',), 'service_id': 25856},
                                   {'service_type': ('digital television service',), 'service_id': 25920},
                                   {'service_type': ('digital radio sound service',), 'service_id': 26176},
                                   {'service_type': ('digital radio sound service',), 'service_id': 26240},
                                   {'service_type': ('digital radio sound service',), 'service_id': 26304},
                                   {'service_type': ('digital radio sound service',), 'service_id': 26368},
                                   {'service_type': ('digital radio sound service',), 'service_id': 26432},
                                   {'service_type': ('digital radio sound service',), 'service_id': 26496},
                                   {'service_type': ('digital radio sound service',), 'service_id': 26560},
                                   {'service_type': ('digital radio sound service',), 'service_id': 26624},
                                   {'service_type': ('digital radio sound service',), 'service_id': 26688},
                                   {'service_type': ('data broadcast service',), 'service_id': 27008},
                                   {'service_type': ('digital television service',), 'service_id': 27072},
                                   {'service_type': ('digital television service',), 'service_id': 27136}]
                Descriptor 0x5a : terrestrial_delivery_system
                    other_frequencies : 1
                    params : {   'bandwidth': 0,
                                 'code_rate_HP': 3,
                                 'code_rate_LP': 3,
                                 'constellation': 1,
                                 'frequency': 537833330,
                                 'guard_interval': 0,
                                 'hierarchy_information': 0,
                                 'inversion': 2,
                                 'transmission_mode': 0}
                Descriptor 0x62 : frequency_list
                    frequencies : [738000000, 826000000, 834000000]
                Descriptor 0x5f : private_data_specifier
                    private_data_specifier : 9018
                Descriptor 0x83 : logical_channel
                    mappings : {   25664: 18,
                                   25728: 21,
                                   25792: 19,
                                   25856: 20,
                                   25920: 22,
                                   26176: 713,
                                   26240: 712,
                                   26304: 722,
                                   26368: 718,
                                   26432: 717,
                                   26496: 710,
                                   26560: 711,
                                   26624: 715,
                                   26688: 716,
                                   27008: 300,
                                   27072: 31,
                                   27136: 29}

ParseNetworkInformationTable can collect the sections of, and then parse, both
'current' and 'next' tables simultaneously.

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it will immediately be sent on out of the "signal" outbox
and the component will then immediately terminate.



How does it work?
-----------------

ParseNetworkInformationTable logs all the table sections it receives, until it
determines it has the complete set; then it parses them.

If the version number field in any table section changes, then the log is
cleared, and the component starts collecting the sections again from scratch.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

from Kamaelia.Support.DVB.Descriptors import parseDescriptor
from Kamaelia.Support.DVB.CRC import dvbcrc

NIT_PID = 0x10

def ParseNetworkInformationTable_ActualNetwork():
    """\
    ParseNetworkInformationTable_ActualNetwork() -> new ParseNetworkInformationTable component.

    Instantiates a ParseNetworkInformationTable component configured to parse
    'ACTUAL' Network tables only (table id 0x40)
    """
    return ParseNetworkInformationTable(acceptTables = {0x40:"ACTUAL"})

def ParseNetworkInformationTable_OtherNetwork():
    """\
    ParseNetworkInformationTable_OtherNetwork() -> new ParseNetworkInformationTable component.

    Instantiates a ParseNetworkInformationTable component configured to parse
    'OTHER' Netowrk tables only (table id 0x41)
    """
    return ParseNetworkInformationTable(acceptTables = {0x41:"OTHER"})

def ParseNetworkInformationTable_ActualAndOtherNetwork():
    """\
    ParseNetworkInformationTable_ActualAndOtherNetwork() -> new ParseNetworkInformationTable component.

    Instantiates a ParseNetworkInformationTable component configured to parse
    both 'ACTUAL' and 'OTHER' Network tables (table ids 0x40 and 0x41)
    """
    return ParseNetworkInformationTable(acceptTables = {0x40:"ACTUAL",0x41:"OTHER"})


class ParseNetworkInformationTable(component):
    """\
    ParseNetworkInformationTable([acceptTables]) -> new ParseNetworkInformationTable component.

    Send reconstructed PSI table sections to the "inbox" inbox. When a complete
    table is assembled and parsed, the result is sent out of the "outbox" outbox
    as a dictionary.
    
    Doesn't emit anything again until the version number of the table changes.
    
    Keyword arguments::

    - acceptTables  - dict of (table_id,string_description) mappings for tables to be accepted (default={0x40:"ACTUAL",0x41:"OTHER"})
    """
    Inboxes = { "inbox" : "DVB PSI Packets from a single PID containing NIT table sections",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Parsed NIT (only when it changes)",
                 "signal" : "Shutdown signalling",
               }
               
    def __init__(self, acceptTables = {0x40:"ACTUAL",0x41:"OTHER"}):
        super(ParseNetworkInformationTable,self).__init__()
        self.acceptTables = acceptTables

    def parseTable(self, index, sections):
        (table_id, current_next, network_id) = index
        
        msg = { "table_type"   : "NIT",
                "table_id"     : table_id,
                "actual_other" : self.acceptTables[table_id],
                "current"      : current_next,
                "network_id"   : network_id,
              }
        services = {}
        
        tss = []
        for (data,section_length) in sections:
            
            network_descriptors_length = ((ord(data[8])<<8) + ord(data[9])) & 0x0fff
            i=10
            network_descriptors_end = i+network_descriptors_length
            msg['descriptors'] = []
            while i < network_descriptors_end:
                descriptor, i = parseDescriptor(i,data)
                msg['descriptors'].append(descriptor)
            
            ts_loop_length = ((ord(data[i])<<8) + ord(data[i+1])) & 0x0fff
            i=i+2
            ts_loop_end = i+ts_loop_length
            while i < ts_loop_end:
                ts = {}
                ts['transport_stream_id'] = (ord(data[i])<<8) + ord(data[i+1])
                ts['original_network_id'] = (ord(data[i+2])<<8) + ord(data[i+3])
                
                transport_descriptors_length = ((ord(data[i+4])<<8) + ord(data[i+5])) & 0x0fff
                i=i+6
                transport_descriptors_end = i+transport_descriptors_length
                ts['descriptors'] = []
                while i < transport_descriptors_end:
                    descriptor,i = parseDescriptor(i,data)
                    ts['descriptors'].append(descriptor)
                tss.append(ts)
                
        msg['transport_streams'] = tss
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
                e = [ord(data[i]) for i in (0,1,2) ]

                table_id = e[0]
                if table_id not in self.acceptTables.keys():
                    continue
                
                syntax = e[1] & 0x80
                if not syntax:
                    continue
                
                section_length = ((e[1]<<8) + e[2]) & 0x0fff
                
                # now were reasonably certain we've got a correct packet
                # we'll convert the rest of the packet
                e = [ord(data[i]) for i in (0,1,2,3,4,5,6,7) ]
                
                network_id = (e[3]<<8) + e[4]
                version = (e[5] &0x3e)  # no need to >> 1
                current_next = e[5] & 0x01
                section_number = e[6]
                last_section_number = e[7]
                
                index = (table_id, current_next, network_id)

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


__kamaelia_components__ = ( ParseNetworkInformationTable, )
__kamaelia_prefabs__    = ( ParseNetworkInformationTable_ActualNetwork,
                            ParseNetworkInformationTable_OtherNetwork,
                            ParseNetworkInformationTable_ActualAndOtherNetwork, )

if __name__ == "__main__":
    
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITables
    from Kamaelia.Device.DVB.Parse.PrettifyTables import PrettifyNetworkInformationTable
    
    import dvb3.frontend
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    Pipeline( DVB_Multiplex(505833330.0/1000000.0, [NIT_PID], feparams),
              DVB_Demuxer({ NIT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseNetworkInformationTable_ActualNetwork(),
              ConsoleEchoer(forwarder=True),
              PrettifyNetworkInformationTable(),
              ConsoleEchoer(),
            ).run()

