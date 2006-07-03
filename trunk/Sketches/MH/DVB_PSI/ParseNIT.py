#!/usr/bin/env python

# Code to parse the different table types in a DVB transport stream

from CRC import dvbcrc

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess
from Descriptors import parseDescriptor

def ParseNIT_ActualNetwork():
    return ParseNIT(acceptTables = {0x40:"ACTUAL"})

def ParseNIT_OtherNetwork():
    return ParseNIT(acceptTables = {0x41:"OTHER"})

def ParseNIT_ActualAndOtherNetwork():
    return ParseNIT(acceptTables = {0x40:"ACTUAL",0x41:"OTHER"})


class ParseNIT(component):
    """
    Parses a NIT table.
    
    Receives table sections from PSI packets. Once all sections have been
    gathered; parses the table and outputs a dictionary containing the contents.
    
    Doesn't emit anything again until the version number of the table changes.
    
    Outputs both 'current' and 'next' tables.
    
    Can only handle multiple NITs with multiple table id's all simultaneously. Those
    table IDs must be registered in the initializer.
    """
    Inboxes = { "inbox" : "DVB PSI Packets from a single PID containing NIT table sections",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Parsed NIT (only when it changes)",
                 "signal" : "Shutdown signalling",
               }
               
    def __init__(self, acceptTables = {0x40:"ACTUAL",0x41:"OTHER"}):
        super(ParseNIT,self).__init__()
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
                e = [ord(data[i]) for i in (0,1,2,3,4,5,6,7) ]

                table_id = e[0]
                if table_id not in self.acceptTables.keys():
                    continue
                
                syntax = e[1] & 0x80
                if not syntax:
                    continue
                
                section_length = ((e[1]<<8) + e[2]) & 0x0fff
                
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


if __name__ == "__main__":
    
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.EIT import PSIPacketReconstructor
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Util.Graphline import Graphline
    
    from MakeHumanReadable import MakeNITHumanReadable
    
    import dvb3.frontend
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    pipeline( DVB_Multiplex(505833330.0/1000000.0, [0x10], feparams),
              DVB_Demuxer({ 0x10:["outbox"]}),
              PSIPacketReconstructor(),
              ParseNIT_ActualNetwork(),
              MakeNITHumanReadable(),
              ConsoleEchoer(),
            ).run()

