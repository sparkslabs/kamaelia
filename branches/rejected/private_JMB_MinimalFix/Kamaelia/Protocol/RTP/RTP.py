#!/usr/bin/env python
#
# (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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
================================
RTP Packet Framing and Deframing
================================

Send a dict specifying what needs to go into the RTP packet and RTPFramer will
output it as a RTP frame.

RTPDeframer parses an RTP packet in binary string format and outputs a
(seqnum, packet) tuple containing a sequence number and a dict structure
containing the payload and metadata of the RTP packet. The format is the same as
that used by RTPFramer.

These components simply format the data into the RTP packet format or take it
back out again. They do not understand the specifics of each payload type.
You must determine for yourself the correct values for each field (eg. payload
type, timestamps, CSRCS, etc).

See `RFC 3550`_ and `RFC 3551`_ for information on the RTP speecification and
the meaning and formats of fields in RTP packets.

.. _`RFC 3550`: http://tools.ietf.org/html/rfc3550
.. _`RFC 3551`: http://tools.ietf.org/html/rfc3551



Example Usage
-------------

Read MPEG Transport Stream packets (188 bytes each) from a file in groups of 7
at a time (to fill an RTP packet) and send them in RTP packets over multicast to
224.168.2.9 on port 1600::

    class PrePackage(Axon.Component.component):
        def main(self):
            SSRCID = random.randint(0,(2**32) - 1)      # random unique ID for this source
            while 1:
                while self.dataReady("inbox"):
                    recvData = self.recv("inbox")
                    self.send(
                      { 'payloadtype' : 33,             # type 33 for MPEG 2 TS
                        'payload'     : recvData,
                        'timestamp'   : time.time() * 90000,
                        'ssrc'        : SSRCID,
                      },
                      "outbox")
                yield 1
                
    
    Pipeline( RateControlledFileReader("transportstream",chunksize=7*188),
              PrePackage(),
              RTPFramer(),
              Multicast_Transceiver(("0.0.0.0", 0, "224.168.2.9", 1600)

Timestamps for MPEG TS in RTP are integers at 90KHz resolution (hence the
x90000 scaling factor). A random value is chosen for the unique source
identifier (ssrc).

Save the payload from a stream of RTP packets being received from multicast
address 224.168.2.9 on port 1600 down to a file::

    Pipeline( Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
              SimpleDetupler(1),                      # discard the source address
              RTPDeframer(),
              RecoverOrder(bufsize=64, modulo=65536), # reorder packets
              SimpleDetupler(1),                      # discard the sequence number
              SimpleDetupler("payload"),
              SimpleFileWriter("received_stream"),
            )



RTPFramer behaviour
-------------------

Send to RTPFramer's "inbox" inbox a dictionary. It must contain these fields::

    {
        'payloadtype' : integer payload type
        'payload'     : binary string containing the payload
        'timestamp'   : integer timestamp (32 bit, unsigned)
        'ssrc'        : sync source identifier (32 bit, unsigned)

...and these fields are optional::

        'csrcs'        : list of contributing source identifiers (default = [])
        'bytespadding' : number of bytes of padding to be added to the payload (default=0)
        'extension'    : binary string of any extension data (default = "")
        'marker'       : True to set the marker bit, otherwise False (default=False)
    }

RTPFramer automatically adds a randomised offset to the timestamp, and generates
the RTP packet sequence numbers, as required in the specification (RFC 3550).

RTPFramer constructs an RTP packet matching the fields specified and sends it
as a binary string out of the "outbox" outbox.

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox. It is immediately sent on out of the "signal" outbox and the
component then immediately terminates.



RTPDeframer Behaviour
---------------------

Send to RTPDeframer's "inbox" inbox a binary string of an RTP packet, and the
packet will be parsed, resulting in a (seqnum, packet_contents) tuple being sent
to the "outbox" outbox. It will have this structure::

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
import struct, random, time


class RTPFramer(component):
    """\
    RTPFramer() -> new RTPFramer component.
    
    Creates a complete RTP packet based on a dict structure describing the
    packet.
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

        # initialise random seqnum
        # XXX Ought to comply with RFC1750 (for security) - not sure if this method does
        self.seqnum = random.randint(0,(2**16) - 1)
        self.timestamp_offset = random.randint(0,(2**32) - 1)  # we'll add this to timestamps

        while not shutdown:

            while self.dataReady("inbox"):
                content = self.recv("inbox")
                self.send( self.constructPacket(content), "outbox")

            shutdown = shutdown or self.shutdown()

            if not shutdown and not self.anyReady():
                self.pause()

            yield 1

    def constructPacket(self, content):
        packet = []
        
        padding     = content.get('bytespadding',0)   # number of padding bytes required
        extension   = content.get('extension',None)   # binary string extension data, or empty string
        csrcs       = content.get('csrcs',[])         # list of contributing source ids
        payloadtype = content['payloadtype']
        marker      = content.get('marker', False)
        ssrc        = content.get('ssrc')
        timestamp   = int(content.get('timestamp'))
        payload     = content.get('payload')
        

        byte = 0x80
        if padding > 0: byte=byte + 0x20
        if extension:   byte=byte + 0x10
        assert(len(csrcs)<16)
        byte=byte + len(csrcs)
        
        packet.append( chr(byte) )

        byte = payloadtype & 0x7f
        if marker:
            byte = byte + 0x80

        packet.append( chr(byte) )

        packet.append( struct.pack(">H", self.seqnum) )
        self.seqnum = (self.seqnum + 1) & 0xffff

        packet.append( struct.pack(">I",(timestamp + self.timestamp_offset) & 0xffffffffL) )
        packet.append( struct.pack(">I",ssrc & 0xffffffffL) )

        for csrc in csrcs:
            packet.append( struct.pack(">I",csrc & 0xffffffffL) )

        if extension:
            ehdr, epayload = extension
            packet.append( ehdr[0:2] )  # 2 bytes
            packet.append( struct.pack(">H", len(epayload)) )
            packet.append( epayload )
        
        packet.append(payload)

        # pad with zeros, terminated with length of padding, eg. 0x00 0x00 0x03
        if padding > 0:
            packet.append( "\0"*(padding-1) + chr(padding) ) 

        # combine the packet elements together and send
        packet="".join(packet)
        return packet


        
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


__kamaelia_components__ = ( RTPFramer, RTPDeframer, )

