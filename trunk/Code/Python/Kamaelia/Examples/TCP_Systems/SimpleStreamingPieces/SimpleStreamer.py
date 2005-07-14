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
import Kamaelia.ReadFileAdaptor
from Kamaelia.SimpleServerComponent import SimpleServer

file_to_stream = "/usr/share/wesnoth/music/wesnoth-1.ogg" #"/home/zathras/Documents/Music/PopularClassics/3/audio_09.ogg"

def AdHocFileProtocolHandler(filename):
    class klass(Kamaelia.ReadFileAdaptor.ReadFileAdaptor):
        def __init__(self,*argv,**argd):
            super(klass,self).__init__(filename, readmode="bitrate", bitrate=400000)
    return klass

class SimpleStreamer(_Axon.Component.component):
   def main(self):
      import random
      clientServerTestPort=1500

      server=SimpleServer(protocol=AdHocFileProtocolHandler(file_to_stream), 
                           port=clientServerTestPort)

      self.addChildren(server)
      yield _Axon.Ipc.newComponent(*(self.children))

      while 1:
         self.pause()
         yield 1

if __name__ == '__main__':
   from Axon.Scheduler import scheduler
   t = SimpleStreamer().activate()
   t.activate()
   scheduler.run.runThreads(slowmo=0)

