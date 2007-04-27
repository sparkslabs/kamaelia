#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
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
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
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
        pipeline(Introspector(), TCPClient("127.0.0.1",1501)).activate()
   
   server     = SimpleServer( protocol = filereader, port = SERVERPORT ).run()

