#!/usr/bin/env python

# Code to parse the different table types in a DVB transport stream

# NB: the word 'service' is used here to refer to:
#   * 'service' as defined in "Specification for Service Information (SI) in
#     DVB systems" (ETSI EN 300 468)
#   * 'program' as defined in "Generic coding of moving pictures and associated
#     audio: systems" (ISO/IEC 13818-1) (MPEG Systems standard)

from CRC import dvbcrc

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess



class ParsePAT(component):
    """
    Parses the PAT table.
    
    Receives table sections from PSI packets. Once all sections have been
    gathered; parses the table and outputs a dictionary containing the contents.
    
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
                e = [ord(data[i]) for i in (0,1,2,5,6,7) ]

                table_id = e[0]
                if table_id != 0:
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
                    

if __name__ == "__main__":
    
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
    from Kamaelia.Device.DVB.EIT import PSIPacketReconstructor
    from Kamaelia.Util.Console import ConsoleEchoer
    
    from MakeHumanReadable import MakePATHumanReadable
    
    import dvb3.frontend
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }

    pipeline( DVB_Multiplex(505833330.0/1000000.0, [0], feparams),
              DVB_Demuxer({ 0:["outbox"]}),
              PSIPacketReconstructor(),
              ParsePAT(),
              MakePATHumanReadable(),
              ConsoleEchoer(),
            ).run()
            