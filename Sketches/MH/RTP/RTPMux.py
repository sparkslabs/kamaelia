#!/usr/bin/env python
from Kamaelia.Chassis.Pipeline import Pipeline
from Multicast_transceiver import Multicast_transceiver
from Kamaelia.Protocol.SimpleReliableMulticast import RecoverOrder
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Util.Detuple import SimpleDetupler
from Kamaelia.Util.Console import ConsoleEchoer
import sys; sys.path.append("../DVB_Remuxing/")
from ExtractPCR import AlignTSPackets
from RTPFramer import RTPFramer, GroupTSPackets, PrepForRTP
from RTPDeframer import RTPDeframer
from Kamaelia.Util.Backplane import Backplane, SubscribeTo, PublishTo

from Axon.Component import component


Pipeline( Multicast_transceiver("0.0.0.0", 5150, "233.122.227.151", 0),
##          SimpleDetupler(1),
          RTPDeframer(),
          RecoverOrder(),
          SimpleDetupler(1),
          SimpleDetupler("payload"),
          AlignTSPackets(),
          PublishTo("TS PACKETS"),
        ).activate()
        
Pipeline( SubscribeTo("TS PACKETS"),
          GroupTSPackets(),
          PrepForRTP(),
          RTPFramer(),
          Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600)
        ).activate()
        
Backplane("TS PACKETS").run()

# multicast relay only: 15.5%
# repackaging rtp, excluding splitting up the TS packets: 42.5%
# including splitting and regrouping the TS packets: peaks 72%
