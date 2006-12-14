#!/usr/bin/env python
from Kamaelia.Chassis.Pipeline import Pipeline
#from Multicast_transceiver import Multicast_transceiver
from Multicast_transceiver_threaded import Multicast_transceiver
#from Kamaelia.Protocol.SimpleReliableMulticast import RecoverOrder
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Util.Detuple import SimpleDetupler
from Kamaelia.Util.Console import ConsoleEchoer
import sys; sys.path.append("../DVB_Remuxing/")
from ExtractPCR import AlignTSPackets
from RTPFramer import RTPFramer, GroupTSPackets, PrepForRTP
from RTPDeframer import RTPDeframer
from Kamaelia.Util.Backplane import Backplane, SubscribeTo, PublishTo

from Axon.Component import component

from SDP import GetRTPAddressFromSDP
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Chassis.Graphline import Graphline

from RecoverOrder import RecoverOrder

from SoftDemux import DVB_SoftDemuxer

pidfilter = {}
for i in range(0,0x2000):
    pidfilter[i] = ["outbox"]

class DetectGap(component):
    def main(self):
        while not self.dataReady("inbox"):
            self.pause()
            yield 1
        data = self.recv("inbox")
        self.send(data,"outbox")
        next = (data[0]+1)&0xffff
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                if data[0] != next:
                    print "Gap size %d going to %d\n" % (data[0]-next,data[0])
                next=(data[0]+1)&0xffff
                self.send(data,"outbox")
            self.pause()
            yield 1

#sdp_url = "http://support.bbc.co.uk/multicast/sdp/bbcone-avc.sdp"
sdp_url = "http://support.bbc.co.uk/multicast/sdp/bbcone-mpeg2.sdp"

Pipeline( 
          Graphline(
              SDP = GetRTPAddressFromSDP(sdp_url),
              GET = Carousel(lambda (host,port): Multicast_transceiver("0.0.0.0",port,host,0)),
              linkages = {
                  ("SDP","outbox") : ("GET","next"),
                  ("GET","outbox") : ("","outbox"),
                  ("GET","signal") : ("","signal"),
              }
          ),
#          SimpleDetupler(1),
          RTPDeframer(),
          RecoverOrder(bufsize=64, modulo=65536),
          DetectGap(),
          SimpleDetupler(1),
          SimpleDetupler("payload"),
#          AlignTSPackets(),
          DVB_SoftDemuxer(pidfilter),
#          PublishTo("TS PACKETS"),
#        ).activate()
#        
#Pipeline( SubscribeTo("TS PACKETS"),
          GroupTSPackets(),
          PrepForRTP(),
          RTPFramer(),
          Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600)
#        ).activate()
        ).run()
        
#Backplane("TS PACKETS").run()

