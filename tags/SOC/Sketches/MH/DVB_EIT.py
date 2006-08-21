#!/usr/bin/env python

# parse EIT now & next information from DVB-T streams

import sys; sys.path.append("../MPS/DVB/Components/");

from PID import DVB_Multiplex, DVB_Demuxer
from Axon.Component import component
import struct


class PSIPacketReconstructor(component):
    """\
    Takes DVB Transport stream packets for a given PID and reconstructs the
    PSI packets from within the stream.
    
    Will only handle stream from a single PID.
    """
    def main(self):
        buffer = ""
        nextCont = None
        # XXX assuming for the moment that this can only handle one PID at a time
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                
                byte = ord(data[1])
                start_indicator = (byte & 0x40) != 0
                
                byte = ord(data[3])
                adaption   = (byte & 0x30) >> 4
                contcount  = byte & 0x0f

                # check continuity counter is okay (otherwise ignore packet)
                # or that its the start of a new packet and we've not started receiving yet
                if (nextCont == None and start_indicator) or nextCont == contcount:
                    
                    # determine start of payload offset
                    if adaption == 1:
                        payload_start = 4
                    elif adaption == 3:
                        payload_start = 4+1+ord(data[4])    # skip past adaption data
                    else: # adaption == 0 or adaption == 2
                        # ignore if adaption field==0 or no payload
                        continue 
                    
                    # if start of new payload present, flush previous, now complete, packet
                    if start_indicator:
                        prevstart = payload_start
                        payload_start = prevstart + ord(data[prevstart]) + 1
                        buffer = buffer + data[prevstart+1:payload_start]
                        if len(buffer) and nextCont != None:   # don't flush through dregs if this is the first time
                            self.send( buffer, "outbox" )
                        buffer = ""
                    
                    buffer = buffer + data[payload_start:]
                    nextCont = (contcount + 1) & 0xf
                else:
                    # reset for crash relock
                    nextCont = None
                    buffer= ""
            self.pause()
            yield 1



class EITPacketParser(component):
    """\
    Parses EIT packets and extracts NOW & NEXT short event descriptions for
    channels within this transport stream.
    
    (Ignores events belonging to other multiplexes)
    """
    
    Inboxes = { "inbox" : "PES packets",
                "control" : "NOT USED",
              }
                    
    Outboxes = { "outbox" : "Parsed NOW and NEXT EIT events",
                 "signal" : "NOT USED",
               }
                    
    def main(self):
        
        
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                
                msg = {}
                
                # passes CRC test

                s = struct.unpack(">BHHBBBHHBB", data[:14])
                
                table_id       = s[0]
                syntax         = s[1] & 0x8000; 
                section_length = s[1] & 0x0fff
                service_id     = s[2]
                version        = (s[3] >>1) & 0x1f
                current_next   = s[3] & 0x01
                section_num    = s[4]
                last_section   = s[5]
                ts_id          = s[6]
                net_id         = s[7]
                seg_last_sect  = s[8]
                last_table_id  = s[9]
                
                data=data[:3+section_length]       # remove any padding at end of table
                
                if table_id != 0x4e:  # only interested in present/following data for this TS
                    continue
                
                if not syntax:
                    print "wrong syntax"
                    continue
                
                if not current_next: # subtable not yet applicable
                    continue
                
                # which subtable (uniquely identified by table_id, service(channel), TS and network)
                subtable_id = (table_id, service_id, ts_id, net_id)
                
#                print "EIT table_id=",hex(table_id)
#                print subtable_id
#                print section_num,last_section,seg_last_sect
                
                if crc32(data):  # fail on non-zero result
                    print "EIT packet CRC error"
                    continue
                
                msg['service'] = service_id
                msg['transportstream'] = ts_id
                
                # go through events
                pos = 14
                while pos < len(data) - 4: # 4 bytes for final checksum
                    e = struct.unpack(">HHBBBBBBH",data[pos:pos+12])
                    event_id = e[0]
                    date     = parseMJD(e[1])                         # Y, M, D
                    time     = unBCD(e[2]), unBCD(e[3]), unBCD(e[4])  # HH, MM, SS
                    duration = unBCD(e[5]), unBCD(e[6]), unBCD(e[7])  # HH, MM, SS
                    running_status  = (e[8] & 0xe000) >> 13
                    free_CA_mode    = e[8] & 0x1000
                    descriptors_len = e[8] & 0x0fff
                    
                    if running_status in [1,2]:
                        msg['when'] = "NEXT"
                    elif running_status in [3,4]:
                        msg['when'] = "NOW"
                    
                    msg['startdate'] = date
                    msg['starttime'] = time
                    msg['duration'] = duration
                    pos = pos + 12
                    descriptors_end = pos + descriptors_len
                    
                    # go through descriptors
                    while pos < descriptors_end:
                        desc_tag = ord(data[pos])
                        desc_len = ord(data[pos+1])
                        
                        if desc_tag == 0x4d: # only interested in Short Event Descriptor
                            lang = data[pos+2:pos+5]
                            namelen = ord(data[pos+5])
                            name = data[pos+6:pos+6+namelen]
                            textlen = ord(data[pos+6+namelen])
                            text = data[pos+7+namelen:pos+7+namelen+textlen]
                            
                            msg['name'] = name
                            msg['description'] = text
                            
                        pos = pos + 2 + desc_len
                    
                    self.send(msg, "outbox")
                    
                
            self.pause()
            yield 1
                    
                    
                   
def crc32(data):
    poly = 0x4c11db7
    crc = 0xffffffff
    for byte in data:
        byte = ord(byte)
        for bit in range(7,-1,-1):  # MSB to LSB
            z32 = crc>>31    # top bit
            crc = crc << 1
            if ((byte>>bit)&1) ^ z32:
                crc = crc ^ poly
            crc = crc & 0xffffffff
    return crc


def parseMJD(MJD):
    """Parse 16 bit unsigned int containing Modified Julian Date, as per DVB-SI spec
    returning year,month,day"""
    YY = int( (MJD - 15078.2) / 365.25 )
    MM = int( (MJD - 14956.1 - int(YY*365.25) ) / 30.6001 )
    D  = MJD - 14956 - int(YY*365.25) - int(MM * 30.6001)
    
    K=0
    if MM == 14 or MM == 15:
        K=1
    
    return (1900 + YY+K), (MM-1-K*12), D
    
def unBCD(byte):
    return (byte>>4)*10 + (byte & 0xf)


class NowNextChanges(component):
    """\
    Simple attempt to filter DVB now and next info for multiple services,
    such that we only send output when the data changes.
    """
    def main(self):
        current = {}
        
        while 1:
            while self.dataReady("inbox"):
                event = self.recv("inbox")
                
                # only interested in 'now' events, not 'next' events
                if event['when'] != "NOW":
                   continue
                
                uid = event['service'], event['transportstream']
                
                if current.get(uid,None) != event:
                    current[uid] = event
                    self.send(current[uid],"outbox")
            self.pause()
            yield 1
                    

class NowNextServiceFilter(component):
    """\
    Filters now/next event data for only specified services.
    """
    def __init__(self, *services):
        super(NowNextServiceFilter,self).__init__()
        self.services = services
        
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                event = self.recv("inbox")
                if event['service'] in self.services:
                    self.send(event,"outbox")
            self.pause()
            yield 1

class TimeAndDatePacketParser(component):
    """\
    Parses "Time and Date" packets.
    """
    
    Inboxes = { "inbox" : "PES packets",
                "control" : "NOT USED",
              }
                    
    Outboxes = { "outbox" : "Parsed date and time",
                 "signal" : "NOT USED",
               }
                    
    def main(self):
        
        
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                
                msg = {}
                
                s = struct.unpack(">BHHBBB", data[:8])
                
                table_id       = s[0]
                syntax         = s[1] & 0x8000; 
                section_length = s[1] & 0x0fff
                
                data=data[:3+section_length]       # remove any padding at end of table
                
                if table_id != 0x70:  # only interested Date & Time packets
                    continue
                
                if syntax:
                    print "wrong syntax"
                    continue
                
                date     = parseMJD(s[2])                         # Y, M, D
                time     = unBCD(s[3]), unBCD(s[4]), unBCD(s[5])  # HH, MM, SS
                
                msg['date'] = date
                msg['time'] = time
                self.send(msg, "outbox")
            
            self.pause()
            yield 1


if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Util.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleEchoer

    Graphline(
#        SOURCE=ReadFileAdaptor("/home/matteh/eit.ts"),
        SOURCE=DVB_Multiplex(505833330.0/1000000.0, [18,20]),
        DEMUX=DVB_Demuxer({ "18": "_EIT_", "20":"_DATETIME_" }),
        EIT = pipeline( PSIPacketReconstructor(),
                        EITPacketParser(),
                        NowNextServiceFilter(4164, 4228),   # BBC ONE & BBC TWO
                        NowNextChanges(),
                        ConsoleEchoer(),
                      ),
        DATETIME = pipeline( PSIPacketReconstructor(),
                             TimeAndDatePacketParser(),
                             ConsoleEchoer(),
                           ),
        linkages={ ("SOURCE", "outbox"):("DEMUX","inbox"),
                   ("DEMUX", "_EIT_"): ("EIT", "inbox"),
                   ("DEMUX", "_DATETIME_"): ("DATETIME", "inbox"),
                 }
        ).run()
