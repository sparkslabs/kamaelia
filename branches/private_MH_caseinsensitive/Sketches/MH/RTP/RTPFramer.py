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
====================
RTP Packet Generator
====================

Send a dict specifying what needs to go into the RTP packet and RTPFramer will
output it as a RTP frame.

This component simply formats the data into the RTP packet format. It does not
understand the specifics of each payload type. You must determine for yourself
the correct values for each field (eg. payload type, timestamps, CSRCS, etc).

See RFC 3550 and 3551 for information on the RTP speecification and the meaning
and formats of fields in RTP packets.



Example Usage
-------------

Read MPEG Transport Stream packets (188 bytes each) from a file in groups of 7
at a time (to fill an RTP packet) and send them in RTP packets over multicast to
224.168.2.9 on port 1600::

    SSRCID = random.randint(0,(2**32) - 1)        # unique ID for this source
    
    Pipeline( RateControlledFileReader("transportstream",chunksize=7*188),
              PureTransformer(lambda recvData:
                  {
                      'payloadtype' : 33,             # type 33 for MPEG 2 TS
                      'payload'     : recvData,
                      'timestamp'   : time.time() * 90000,
                      'ssrc'        : SSRCID,
                  }
              ),
              RTPFramer(),
              Multicast_Transceiver(("0.0.0.0", 0, "224.168.2.9", 1600)

Timestamps for MPEG TS in RTP are integers at 90KHz resolution (hence the
x90000 scaling factor). A random value is chosen for the unique source
identifier (ssrc).



Behaviour
---------

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

if 1:
        class GroupTSPackets(component):
            def main(self):
                p=[]
                while 1:
                    while self.dataReady("inbox"):
                        p.append(self.recv("inbox"))
                        if len(p)==7:
                            self.send( "".join(p), "outbox")
                            p=[]
                    self.pause()
                    yield 1
        
        class PrepForRTP(component):
            def main(self):
                starttime = time.time()
                ssrc = random.randint(0,(2**32) - 1)
                while 1:
                    while self.dataReady("inbox"):
                        payload=self.recv("inbox")
                        timestamp = (time.time() - starttime) * 90000
                        packet = {
                            'payloadtype' : 33,   # MPEG 2 TS
                            'payload'     : payload,
                            'timestamp'   : int(timestamp),
                            'ssrc'        : ssrc,
                            }
                        self.send(packet, "outbox")
                        
                    self.pause()
                    yield 1
        


if __name__ == "__main__":
    test=3
    
    if test==1:
        from Axon.ThreadedComponent import threadedcomponent
        import time
        
        class FakeRTPSource(threadedcomponent):
            # send dummy MPEG2 TS packets, 90kHz timestamp clock
            def main(self):
                starttime = time.time()
                ssrc = random.randint(0,(2**32) - 1)
                while 1:
                    time.sleep(0.05)
                    timestamp = (time.time() - starttime) * 90000
                    packet = {
                        'payloadtype' : 33,   # MPEG 2 TS
                        'payload'     : ("\x47" + "\x00" * 187) * 2,
                        'timestamp'   : int(timestamp),
                        'ssrc'        : ssrc,
                        }
                    self.send(packet, "outbox")
        
        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
        
        Pipeline( FakeRTPSource(),
                  RTPFramer(),
                  Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600)
                ).run()
    
    elif test==2:
        from Kamaelia.Chassis.Pipeline import Pipeline
        #from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
        from Multicast_transceiver import Multicast_transceiver
        from Kamaelia.File.Reading import RateControlledFileReader
        import sys; sys.path.append("../DVB_Remuxing/")
        from ExtractPCR import AlignTSPackets
        import time,random
        
        from Kamaelia.Device.DVB.Core import DVB_Multiplex
        
        import dvb3.frontend
        
        FREQUENCY = 505.833330
        FE_PARAMS = { "inversion" : dvb3.frontend.INVERSION_AUTO,
                    "constellation" : dvb3.frontend.QAM_16,
                    "coderate_HP" : dvb3.frontend.FEC_3_4,
                    "coderate_LP" : dvb3.frontend.FEC_3_4,
                    }
                    
        Pipeline( DVB_Multiplex(FREQUENCY, [600,601], FE_PARAMS),
                  AlignTSPackets(),
                  GroupTSPackets(),
                  PrepForRTP(),
                  RTPFramer(),
                  Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600)
                ).run()

    elif test==3:
        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.Util.DataSource import DataSource
        from Kamaelia.Util.PureTransformer import PureTransformer
        from Kamaelia.Util.Detuple import SimpleDetupler
        from Kamaelia.Util.Console import ConsoleEchoer
        from RTPDeframer import RTPDeframer
        import time,random

        SSRCID = random.randint(0,(2**32) - 1)

        Pipeline( DataSource([ "Hello world!\n",
                               "The quick brown fox\n",
                               "Jumps over the lazy dog\n",
                               "Lorem ipsum dolor sit amet\n",
                               "...\n",
                               "And this is\n",
                               "the end!\n",
                             ]),
                  PureTransformer(lambda payload:
                            {
                            'payloadtype' : 99,
                            'payload'     : payload,
                            'timestamp'   : time.time() * 90000,
                            'ssrc'        : SSRCID,
                            }
                        ),
                  RTPFramer(),
                  RTPDeframer(),
                  SimpleDetupler(1),
                  SimpleDetupler("payload"),
                  ConsoleEchoer(),
              ).run()
        
    else:
        raise