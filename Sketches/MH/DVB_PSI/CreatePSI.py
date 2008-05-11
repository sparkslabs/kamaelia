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
========================
Construct DVB PSI tables
========================

PSI table sections in ... MPEG transport stream packets out

not yet tested ... or kamaelia-ised!


"""



class SerialiseEIT(object):
    """\
    EIT PSI section dictionary structure in ... binary PSI table section out
    """
    def __init__(self, sectionPacketiser):
        super(SerialiseEIT,self).__init__()
        self.sectionPacketiser = sectionPacketiser
      
    def serialise(self, section):
        pass


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
        payload.insert(section[sStart:sStart+chunkLen)
        print self.tsPacketiser.packetise(payload.join(""), true, chr(0xff))
        sStart+=chunkLen
        bytesLeft-=chunkLen

        while bytesLeft > 0:
          
            if bytesLeft <= self.leftOvers_Threshold:
                self.leftOvers = section[sStart:]
                break

            # subsequent packets
            chunkLen = min(bytesLeft, 184)  # -1 for the pointer_field
            payload.insert(section[sStart:sStart+chunkLen)
            print self.tsPacketiser.packetise(payload.join(""), false, chr(0xff))
            sStart+=chunkLen
            bytesLeft-=chunkLen




class MakeTransportStreamPackets(object):
    """\
    Payloads in ... transport stream packets out
    """
    def __init__(self, pid, scrambling=0, priority=false):
        super(MakeTransportStreamPackets,self).__init__()
        self.pid = pid
        self.scrambling = scrambling
        self.priority = priority
        
        self.continuityCounter = 0
      
      
    def packetise(self, payload, startIndicator=false, stuffingByte=chr(0xff)):
        packet = []
    
        pidAndFlags = self.pid & 0x1fff
        if startIndicator:
            pidAndFlags += 0x4000
        if self.priority:
            pidAndFlags += 0x2000
            
        # default to no adaption field (lower 2 bits of upper nibble = "01")
        ctrlFlags = (self.scrambling & 0x3) << 6 + 0x10 + self.continuityCounter  
        
        self.continuityCounter = (self.continuityCounter + 1) % 16
    
        packet.insert(chr(0x47))           # start byte
        packet.insert(chr((pidAndFlags>>8) & 0xff))
        packet.insert(chr((pidAndFlags   ) & 0xff))
        packet.insert(chr(ctrlFlags))
    
        if (len(payload) > 184):
            raise "Payload too long to fit in TS packet!"
        
        packet.insert(payload)
        
        if (len(payload) < 184):
            numStuffingBytes = 184-len(payload)
            packet.insert(stuffingByte * numStuffingBytes)
        
        return packet.join("")
