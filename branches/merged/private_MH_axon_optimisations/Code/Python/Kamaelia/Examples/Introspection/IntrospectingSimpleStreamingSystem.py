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

import Axon as _Axon
from Kamaelia.SimpleServerComponent import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient
import Kamaelia.ReadFileAdaptor
from Kamaelia.vorbisDecodeComponent import VorbisDecode, AOAudioPlaybackAdaptor

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg"

import sys ; sys.path.append("../../../../../Sketches/Layout")
from Kamaelia.Util.Introspector import *

def AdHocFileProtocolHandler(filename):
    class klass(Kamaelia.ReadFileAdaptor.ReadFileAdaptor):
        def __init__(self,*argv,**argd):
            super(klass,self).__init__(filename, readmode="bitrate", bitrate=400000)
    return klass

class SimpleStreamingSystem(_Axon.Component.component):
   def main(self):
      import random
      clientServerTestPort=1501

      server=SimpleServer(protocol=AdHocFileProtocolHandler(file_to_stream), 
                           port=clientServerTestPort)
      client=TCPClient("127.0.0.1",clientServerTestPort)
      decoder = VorbisDecode()
      player = AOAudioPlaybackAdaptor()

      self.link((client,"outbox"), (decoder,"inbox"))
      self.link((client,"signal"), (decoder,"control"))
      self.link((decoder,"outbox"), (player,"inbox"))
      self.link((decoder,"signal"), (player, "control") )

      introspector = Introspector()
      iclient = TCPClient("127.0.0.1", 1500)
      self.link((introspector,"outbox"), (iclient,"inbox"))
      
      self.addChildren(server, decoder, player, client)
      self.addChildren(introspector, iclient)
      yield _Axon.Ipc.newComponent(*(self.children))

      while 1:
         self.pause()
         yield 1

if __name__ == '__main__':
   from Axon.Scheduler import scheduler
   t = SimpleStreamingSystem()
   t.activate()
   scheduler.run.runThreads(slowmo=0)

