#!/usr/bin/env python
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
========================
Construct DVB PSI tables
========================

PSI table sections in ... MPEG transport stream packets out

not yet tested ... or kamaelia-ised!


"""
from Kamaelia.Support.DVB.CRC import __dvbcrc as doDvbCRC
from CreateDescriptors import serialiseDescriptors, createMJDUTC, createBCDtimeHMS


# max size of an EIT section, minus the crc and the bit before the events list
_EIT_EVENT_SIZE_THRESHOLD = 4096 - 18

class SerialiseEITSection(object):
    """\
    EIT PSI section dictionary structure in ... binary PSI table section out
    """
    def __init__(self):
        super(SerialiseEITSection,self).__init__()
      
    def serialise(self, section, prebuiltEvents=None):
        data = []
        
        if section["current"]:
            currentNextFlag=1
        else:
            currentNextFlag=0
        
        data.append( chr(section["table_id"]) )
        seclen_index = len(data) # note where the section length field will be inserted once we know its value
        data.append( chr((section["service_id"] >> 8) & 0xff) \
                   + chr((section["service_id"]     ) & 0xff) \
                   + chr(((section["version"] & 0x1f) << 1) + currentNextFlag) \
                   + chr(section["section"]) \
                   + chr(section["last_section"]) \
                   + chr((section["transport_stream_id"] >> 8) & 0xff) \
                   + chr((section["transport_stream_id"]     ) & 0xff) \
                   + chr((section["original_network_id"] >> 8) & 0xff) \
                   + chr((section["original_network_id"]     ) & 0xff) \
                   )
        try:
            data.append( chr((section["segment_last_section_number"])) )
        except KeyError:
            data.append( chr((section["last_section"])) )
        try:
            data.append( chr((section["last_table_id"])) )
        except KeyError:
            data.append( chr((section["table_id"])) )
        
        if prebuiltEvents:
            events = prebuiltEvents
        else:
            (events,count) = self.consumeEvents(section["events"])
            assert(len(eventItems) == count)
        
        # add events onto the end of the packet we're building
        data.extend(events)
        
        # calculate total length of section
        sectionLength = reduce(lambda total,nextStr: total+len(nextStr), data, 0)
        sectionLength -= 1  # doesn't include bytes up to and including the section length field itself (which hasn't been inserted yet)
        sectionLength += 4 # lets not forget the CRC
        
        data.insert(seclen_index, chr(0x80 + ((sectionLength >> 8) & 0x0f)) + chr(sectionLength & 0xff))
        
        # now we've assembled everything, calc the CRC, then write the CRC value at the end
        data = "".join(data)
        crcval = doDvbCRC(data)
        crc = chr((crcval >> 24) & 0xff) \
            + chr((crcval >> 16) & 0xff) \
            + chr((crcval >> 8 ) & 0xff) \
            + chr((crcval      ) & 0xff)
        
        return data + crc

    def consumeEvents(self, eventItems):
        
        # now do events
        events = []
        count = 0
        totalSize = 0
        for event in eventItems:
            descriptors = serialiseDescriptors(event["descriptors"])
            # pre-compute size of this event
            thisEventSize = len(descriptors) + 12 # event size = descriptors + beginning bit
            if totalSize + thisEventSize > _EIT_EVENT_SIZE_THRESHOLD:
                # abort as it isn't going to fit
                break
            else:
                totalSize = totalSize + thisEventSize
            
            mjd, utc = createMJDUTC(*event["starttime"])
            dur = createBCDtimeHMS(*event["duration"])
            flags = ((event["running_status"] & 0x7) << 5)
            if event["free_CA_mode"]:
                flags += 0x10
            
            events.append( chr((event["event_id"] >> 8) & 0xff) \
                         + chr((event["event_id"]     ) & 0xff) \
                         + chr((mjd >> 8) & 0xff)  \
                         + chr((mjd     ) & 0xff)  \
                         + chr((utc >> 16) & 0xff) \
                         + chr((utc >> 8 ) & 0xff) \
                         + chr((utc      ) & 0xff) \
                         + chr((dur >> 16) & 0xff) \
                         + chr((dur >> 8 ) & 0xff) \
                         + chr((dur      ) & 0xff) \
                         )
                         
            elen_index = len(events)  # note where flags and descriptor_loop_length will be inserted
            
            # add descriptors
            events.append(descriptors)
            descriptors_loop_length = len(descriptors)
            
            # now we know how long the descriptor loop is, we write the event's length
            events.insert(elen_index,
                chr(flags + ((descriptors_loop_length >> 8) & 0x0f)) \
              + chr(         (descriptors_loop_length     ) & 0xff) \
            )
            count = count + 1

        return events, count  #  the serialised events, plus a count of how many events we consumed
        



class PacketiseTableSections(object):
    """\
    PSI table sections in ... transport stream packets out
    """
    def __init__(self, tsPacketMaker):
        super(PacketiseTableSections,self).__init__()
        self.tsPacketiser = tsPacketMaker
        self.leftOvers = ""
        self.leftOvers_Threshold = 0   # threshold for carrying over the end of one section into a packet that starts a new one
        
    def packetise(self, section):
        tspackets = []
        
        payload = []
        startOffset = 0
        
        if len(self.leftOvers) > 0:
            payload.insert(self.leftOvers)
            startOffset = len(self.leftOvers)
            self.leftOvers = ""

        sStart = 0
        bytesLeft = len(section)
        
        # first packet
        chunkLen = min(bytesLeft, 184-1-startOffset)  # -1 for the pointer_field
        payload.append(section[sStart:sStart+chunkLen])
        tspackets.append( self.tsPacketiser.packetise("".join(payload), True, chr(0xff)) )
        payload = []
        sStart+=chunkLen
        bytesLeft-=chunkLen

        while bytesLeft > 0:
          
            if bytesLeft <= self.leftOvers_Threshold:
                self.leftOvers = section[sStart:]
                break

            # subsequent packets
            chunkLen = min(bytesLeft, 184)  # -1 for the pointer_field
            payload.append(section[sStart:sStart+chunkLen])
            tspackets.append( self.tsPacketiser.packetise("".join(payload), False, chr(0xff)) )
            payload = []
            sStart+=chunkLen
            bytesLeft-=chunkLen

        return tspackets



class MakeTransportStreamPackets(object):
    """\
    Payloads in ... transport stream packets out
    """
    def __init__(self, pid, scrambling=0, priority=False):
        super(MakeTransportStreamPackets,self).__init__()
        self.pid = pid
        self.scrambling = scrambling
        self.priority = priority
        
        self.continuityCounter = 0
      
      
    def packetise(self, payload, startIndicator=False, stuffingByte=chr(0xff)):
        packet = []
    
        pidAndFlags = self.pid & 0x1fff
        if startIndicator:
            pidAndFlags += 0x4000
        if self.priority:
            pidAndFlags += 0x2000
            
        # default to no adaption field (lower 2 bits of upper nibble = "01")
        ctrlFlags = (self.scrambling & 0x3) << 6 + 0x10 + self.continuityCounter  
        
        self.continuityCounter = (self.continuityCounter + 1) % 16
    
        packet.append(chr(0x47))           # start byte
        packet.append(chr((pidAndFlags>>8) & 0xff))
        packet.append(chr((pidAndFlags   ) & 0xff))
        packet.append(chr(ctrlFlags))
    
        if (len(payload) > 184):
            raise "Payload too long to fit in TS packet! "+str(len(payload))
        
        packet.append(payload)
        
        if (len(payload) < 184):
            numStuffingBytes = 184-len(payload)
            packet.append(stuffingByte * numStuffingBytes)
        
        return "".join(packet)
