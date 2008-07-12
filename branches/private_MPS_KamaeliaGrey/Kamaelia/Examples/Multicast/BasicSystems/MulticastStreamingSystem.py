#!/usr/bin/python
#
# Basic acceptance test harness for the Multicast_sender and receiver
# components.
#

from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Codec.Vorbis import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Detuple import SimpleDetupler

file_to_stream = "../../SupportingMediaFiles/KDE_Startup_2.ogg"

# Server
Pipeline(
    ReadFileAdaptor(file_to_stream, readmode="bitrate", bitrate=400000, chunkrate=50),
    Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
).activate()

# Client
Pipeline(
    Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
    SimpleDetupler(1),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
