#!/usr/bin/env python
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

Code to parse Event Information Tables from a DVB transport stream

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
    """
    Parses a EIT table.
    
    Receives table sections from PSI packets. Once all sections have been
    gathered; parses the table and outputs a dictionary containing the contents.
    
    Doesn't emit anything again until the version number of the table changes.
    
    Outputs both 'current' and 'next' tables.
    
    Can handle multiple EITs with multiple table id's all simultaneously. Those
    table IDs must be registered in the initializer. Use
    ParseEventInformationTable_Subset for convenient presets.
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
                e = [ord(data[i]) for i in range(0,12) ]
                
                table_id = e[0]
                if table_id not in self.acceptTables.keys():
                    continue
                
                syntax = e[1] & 0x80
                if not syntax:
                    continue
                service_id = (e[3]<<8) + e[4]
                
                section_length = ((e[1]<<8) + e[2]) & 0x0fff
                
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
    Component that simplifies EIT data, converting the table to simpler EIT
    event messages.
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
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
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

