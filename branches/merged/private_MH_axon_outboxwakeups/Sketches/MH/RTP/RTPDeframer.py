#!/usr/bin/env python

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished
import struct


class RTPDeframer(component):
    """\
    Deconstructs an RTP packet

    Passes out (seqnum, dict) ... dict is a dictionary containing these fields:

        payloadtype  - integer payload type
        payload      - raw payload string
        timestamp    - integer timestamp
        ssrc         - integer sync source id
        extension    - None or (2byte, extension data)
        csrcs        - list of contrib. sync. source ids (default=[])
        marker       - marker bit flag (default=False)
        
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
    
    