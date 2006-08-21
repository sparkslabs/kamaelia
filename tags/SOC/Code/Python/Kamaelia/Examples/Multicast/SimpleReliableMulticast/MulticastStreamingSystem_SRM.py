#!/usr/bin/python
#
# This is a modification to the multicast streaming system that uses the
# SimpleReliableMulticast protocol, to add a thin skein of reliability over
# multicast. Passes basic lab tests, but needs real world testing to be
# certain.
#

from Axon.Component import component
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.Protocol.SimpleReliableMulticast import SRM_Sender, SRM_Receiver
from Kamaelia.Protocol.Packetise import MaxSizePacketiser
from Kamaelia.Util.Detuple import SimpleDetupler

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg"

#
# Server with simple added reliabilty protocol
# 
pipeline(
    ReadFileAdaptor(file_to_stream, readmode="bitrate", bitrate=400000, chunkrate=50),
    SRM_Sender(),
    MaxSizePacketiser(), # Ensure chunks small enough for multicasting!
    Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
).activate()

#
# Client with simple added reliability protocol
#
pipeline(
    Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
    SimpleDetupler(1),
    SRM_Receiver(),
    SimpleDetupler(1),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
