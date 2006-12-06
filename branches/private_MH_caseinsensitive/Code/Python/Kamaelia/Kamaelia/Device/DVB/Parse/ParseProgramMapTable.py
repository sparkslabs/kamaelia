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

Code to parse Program Map Tables from a DVB transport stream

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

from Kamaelia.Support.DVB.Descriptors import parseDescriptor
from Kamaelia.Support.DVB.CRC import dvbcrc

class ParseProgramMapTable(component):
    """
    Parses a Program Map Table.
    
    Receives table sections from PSI packets. Once all sections have been
    gathered; parses the table and outputs a dictionary containing the contents.
    
    Doesn't emit anything again until the version number of the table changes.
    
    Outputs both 'current' and 'next' tables.
    
    Can only handle one PMT at a time ... you can't feed it mutiple PMTs from
    multiple PIDs.
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

