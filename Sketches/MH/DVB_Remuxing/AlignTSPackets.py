#!/usr/bin/env python

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess

DVB_PACKET_SIZE = 188
DVB_RESYNC = "\x47"

class AlignTSPackets(component):
    
#    def errorIndicatorSet(self, packet):  return ord(packet[1]) & 0x80
#    def scrambledPacket(self, packet):    return ord(packet[3]) & 0xc0

    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                self.shuttingdown=True
        return self.shuttingdown
    
    def main(self):
        buffer  = ""
        buffers = []
        self.shuttingdown=False
        while (not self.shutdown()) or self.dataReady("inbox"):
            yield 1
            if not self.dataReady("inbox"):
               self.pause()
               yield 1
               continue
            else:
                while self.dataReady("inbox"):
                    buffers.append(self.recv("inbox"))
            while len(buffers)>0:
                if len(buffer) == 0:
                    buffer = buffers.pop(0)
                else:
                    buffer += buffers.pop(0)
    
                while len(buffer) >= DVB_PACKET_SIZE:
                      i = buffer.find(DVB_RESYNC)
                      if i == -1: # if not found
                          "we have a dud"
                          buffer = ""
                          continue
                      if i>0:
#                          print "X"
                          # if found remove all bytes preceeding that point in the buffers
                          # And try again
                          buffer = buffer[i:]
                          continue
                      # packet is the first 188 bytes in the buffer now
                      packet, buffer = buffer[:DVB_PACKET_SIZE], buffer[DVB_PACKET_SIZE:]
    
#                      if self.errorIndicatorSet(packet): continue
#                      if self.scrambledPacket(packet):   continue
    
                      self.send(packet, "outbox")


if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.Comparator import Comparator
    from Kamaelia.Util.TestResult import TestResult
    from Kamaelia.Util.Console import ConsoleEchoer
    import random

    def pad(packets,minpadding,maxpadding):
        return [ " " * random.randrange(minpadding,maxpadding+1) + packet for packet in packets]
    
    def fragment(packets,minsize,maxsize):
        fragments = []
        tmp = ""
        reqd = random.randrange(minsize,maxsize+1)
        for packet in packets:
            tmp=tmp+packet
            while len(tmp) >= reqd:
                fragments.append(tmp[:reqd])
                tmp=tmp[reqd:]
                reqd = random.randrange(minsize,maxsize+1)
        if tmp:
            fragments.append(tmp)
        return fragments
            

    packets = [ (DVB_RESYNC + ("%08d" % i) + " "*179) for i in range(0,100) ]
    mushed = fragment(pad(packets,0,1000),2,588)

    Graphline(
       ONTEST = Pipeline(
                    DataSource(mushed),
                    AlignTSPackets(),
                    ),
       SRC2   = DataSource(packets),
       CMP    = Comparator(),
       VALID  = ConsoleEchoer(),
       linkages = {
           ("ONTEST", "outbox") : ("CMP", "inA"),
           ("SRC2", "outbox") : ("CMP", "inB"),
           ("CMP", "outbox") : ("VALID","inbox"),
           }
       ).run()
       