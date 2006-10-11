#!/usr/bin/env python

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished
import struct, random, time


class RTPFramer(component):
    """\
    Constructs RTP header and assembles complete RTP packet.

    Pass a dictionary containing these fields (marked with '*' are optional - they have defaults)
        payloadtype  - integer payload type
        payload      - raw payload string
        timestamp    - integer timestamp
        ssrc         - integer sync source id
        extension*   - (2bytes, extension data) or None (default=None)
        padding*     - number of padding bytes (default=0)
        csrcs*       - list of contrib. sync. source ids (default=[])
        marker*      - marker bit flag (default=False)
        
    Does sequence number and randomisation of timestamp itself
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
        timestamp   = content.get('timestamp')
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
    test=2
    
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
        
        
    else:
        raise