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

Code to parse Service Description Tables from a DVB transport stream

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

from Kamaelia.Support.DVB.Descriptors import parseDescriptor
from Kamaelia.Support.DVB.CRC import dvbcrc

SDT_PID = 0x11


def ParseServiceDescriptionTable_ActualTS():
    return ParseServiceDescriptionTable(acceptTables = {0x42:"ACTUAL"})

def ParseServiceDescriptionTable_OtherTS():
    return ParseServiceDescriptionTable(acceptTables = {0x46:"OTHER"})

def ParseServiceDescriptionTable_ActualAndOtherTS():
    return ParseServiceDescriptionTable(acceptTables = {0x42:"ACTUAL",0x46:"OTHER"})

class ParseServiceDescriptionTable(component):
    """
    Parses a Service Description Table.
    
    Receives table sections from PSI packets. Once all sections have been
    gathered; parses the table and outputs a dictionary containing the contents.
    
    Doesn't emit anything again until the version number of the table changes.
    
    Outputs both 'current' and 'next' tables.
    
    Can only handle multiple SDTs with multiple table id's all simultaneously. Those
    table IDs must be registered in the initializer.
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

