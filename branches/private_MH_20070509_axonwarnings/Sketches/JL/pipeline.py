from Kamaelia.Chassis.Pipeline import Pipeline

from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Protocol.SimpleReliableMulticast import SRM_Sender
from Kamaelia.Protocol.Packetise import MaxSizePacketiser
from Kamaelia.File.Reading import RateControlledFileReader

path = "/home/jlei/Kamaelia/files/finite.mp3"
ip="224.0.0.1"

Pipeline( RateControlledFileReader(path,readmode="bytes",rate=128000/8),
          SRM_Sender(),
          MaxSizePacketiser(),
          Multicast_transceiver("0.0.0.0", 0, ip, 1600),
        ).run()

#This comment added is useless. And even more useless 
