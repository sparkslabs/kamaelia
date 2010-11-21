#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This is a modification to the multicast streaming system that uses the
# SimpleReliableMulticast protocol, to add a thin skein of reliability over
# multicast. Passes basic lab tests, but needs real world testing to be
# certain.
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from Axon.Component import component
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Codec.Vorbis import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Protocol.SimpleReliableMulticast import SRM_Sender, SRM_Receiver
from Kamaelia.Protocol.Packetise import MaxSizePacketiser
from Kamaelia.Util.Detuple import SimpleDetupler

file_to_stream = "../../SupportingMediaFiles/KDE_Startup_2.ogg"

#
# Server with simple added reliabilty protocol
# 
Pipeline(
    ReadFileAdaptor(file_to_stream, readmode="bitrate", bitrate=400000, chunkrate=50),
    SRM_Sender(),
    MaxSizePacketiser(), # Ensure chunks small enough for multicasting!
    Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
).activate()

#
# Client with simple added reliability protocol
#
Pipeline(
    Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
    SimpleDetupler(1),
    SRM_Receiver(),
    SimpleDetupler(1),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
