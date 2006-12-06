#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
=================
RTP Packet Parser
=================

Parses an RTP packet in binary string format and outputs a (seqnum, packet)
tuple containing a sequence number and a dict structure containing the payload
and metadata of the RTP packet.

See RFC 3550 and 3551 for information on the RTP speecification and the meaning
and formats of fields in RTP packets.



Example Usage
-------------

Save the payload from a stream of RTP packets being received from multicast
address 224.168.2.9 on port 1600 down to a file::

    Pipeline( Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
              SimpleDetupler(1),              # discard the source address
              RTPDeframer(),
              RecoverOrder(),                 # uses sequence numbers
              SimpleDetupler(1),              # discard the sequence number
              SimpleDetupler("payload"),
              SimpleFileWriter("received_stream"),
            )



Behaviour
---------

Send to RTPDeframer's "inbox" inbox a binary string of an RTP packet, and the
packet will be parsed, resulting in a (seqnum, packet_contents) tuple being sent
to the "outbox" outbox. It will have this structure:

    ( sequence_number,
      {
        'payloadtype'  : integer payload type
        'payload'      : binary string containing the payload
        'timestamp'    : integer timestamp (32 bit, unsigned)
        'ssrc'         : sync source identifier (32 bit, unsigned)
        'csrcs'        : list of contributing source identifiers, [] if empty
        'extension'    : binary string of any extension data, "" if none
        'marker'       : True if marker bit was set, otherwise False
      }
    )

See RFC 3550 for an explanation of the precise purposes of these fields.
    
If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox. It is immediately sent on out of the "signal" outbox and the
component then immediately terminates.

"""

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished
import struct


class RTPDeframer(component):
    """\
    RTPDeframer() -> new RTPDeframer component.
    
    Deconstructs an RTP packet, outputting (seqnum, dict) tuple where seqnum
    is for recovering the order of packets, and dict contains the fields from
    the RTP packet.
    """

    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False


    def main(self):
        shutdown=False

        while not shutdown:

            while self.dataReady("inbox"):
                packet = self.recv("inbox")
                parsed = self.parsePacket(packet)
                if parsed:
                    self.send(parsed, "outbox")

            shutdown = shutdown or self.shutdown()

            if not shutdown and not self.anyReady():
                self.pause()

            yield 1


    def parsePacket(self, packet):
        e = struct.unpack(">BBHII",packet[:12])
        
        if (e[0]>>6) != 2:       # check version is 2
            return None
        
        # ignore padding bit atm
        
        hasPadding   = e[0] & 0x20
        hasExtension = e[0] & 0x10
        numCSRCs     = e[0] & 0x0f
        hasMarker    = e[1] & 0x80
        payloadType  = e[1] & 0x7f
        seqnum       = e[2]
        timestamp    = e[3]
        ssrc         = e[4]
        
        i=12
        if numCSRCs:
            csrcs = struct.unpack(">"+str(numCSRCs)+"I", packet[i:i+4*csrcs])
            i=i+4*numCSRCs
        else:
            csrcs = []
            
        if hasExtension:
            ehdr, length = struct(">2sH",packet[i:i+4])
            epayload = packet[i+4:i+4+length]
            extension = (ehdr,epayload)
            i=i+4+length
        else:
            extension = None
        
        # now work out how much padding needs stripping, if at all
        end = len(packet)
        if hasPadding:
            amount = ord(packet[-1])
            end = end - amount
            
        payload = packet[i:end]
        
        return ( seqnum,
                 { 'payloadtype' : payloadType,
                   'payload'     : payload,
                   'timestamp'   : timestamp,
                   'ssrc'        : ssrc,
                   'extension'   : extension,
                   'csrcs'       : csrcs,
                   'marker'      : hasMarker,
                 }
               )
               
if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
#    from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
    from Multicast_transceiver import Multicast_transceiver
    from Kamaelia.Protocol.SimpleReliableMulticast import RecoverOrder
    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.Util.Detuple import SimpleDetupler
    from Kamaelia.Util.Console import ConsoleEchoer
    
    Pipeline( Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
              #Multicast_transceiver("0.0.0.0", 1234, "239.255.42.42", 0),  # for live555 testing
              SimpleDetupler(1),
              RTPDeframer(),
              RecoverOrder(),
              SimpleDetupler(1),
              SimpleDetupler("payload"),
              SimpleFileWriter("received.ts"),
#              ConsoleEchoer(),
            ).run()
    
    