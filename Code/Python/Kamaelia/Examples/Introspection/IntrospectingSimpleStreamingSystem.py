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
# Simple Ogg Vorbis audio streaming system
#

from Kamaelia.SimpleServerComponent import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient
import Kamaelia.ReadFileAdaptor
from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.Util.Introspector import Introspector

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg"
clientServerTestPort = 1501

def AdHocFileProtocolHandler(filename):
    class klass(Kamaelia.ReadFileAdaptor.ReadFileAdaptor):
        def __init__(self,*argv,**argd):
            super(klass,self).__init__(filename, readmode="bitrate", bitrate=400000)
    return klass

# Start the server
SimpleServer(protocol=AdHocFileProtocolHandler(file_to_stream), 
             port=clientServerTestPort).activate()

# Start the client
pipeline(
      TCPClient("127.0.0.1",clientServerTestPort),
      VorbisDecode(),
      AOAudioPlaybackAdaptor(),
).activate()

# Start the introspector and connect to a local visualiser
pipeline(
    Introspector(),
    TCPClient("127.0.0.1", 1500),
).run()
