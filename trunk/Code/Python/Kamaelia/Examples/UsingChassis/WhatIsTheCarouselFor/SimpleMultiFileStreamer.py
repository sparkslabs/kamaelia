#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# -------------------------------------------------------------------------
#
# Simple multi-file ogg vorbis streaming system
#
# based on Kamaelia/Examples/example2
# use Kamaelia/Examples/example2/Simple[r]StreamingClient.py to receive
#

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Chassis.Prefab import JoinChooserToCarousel
from Kamaelia.File.Reading import FixedRateControlledReusableFileReader
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Chooser import ForwardIteratingChooser # InfiniteChooser import InfiniteChooser

#shortfile = "/opt/kde3/share/apps/khangman/sounds/new_game.ogg"
shortfile = "/opt/kde3/share/sounds/KDE_Startup_2.ogg"

FILES_TO_STREAM = [ shortfile, shortfile, shortfile ]# [  file_to_stream, file_to_stream2 ]
BITRATE         = 800000 # 38000
CHUNKSIZEBYTES  = 512
SERVERPORT      = 1500


def MultiFileReaderProtocol(filenames, bitrate, chunksizebytes):

    def protocolFactory(*argv, **argd):
        return JoinChooserToCarousel(
            ForwardIteratingChooser(filenames),
            FixedRateControlledReusableFileReader(readmode="bytes",
                                               rate=bitrate/8,
                                               chunksize=chunksizebytes)
          )
    return protocolFactory



if __name__ == '__main__':

   filereader = MultiFileReaderProtocol( FILES_TO_STREAM, BITRATE, CHUNKSIZEBYTES)


   if 0:
        from Kamaelia.Internet.TCPClient import TCPClient
        from Kamaelia.Util.Introspector import Introspector
        Pipeline(Introspector(), TCPClient("127.0.0.1",1501)).activate()
   
   server     = SimpleServer( protocol = filereader, port = SERVERPORT ).run()

