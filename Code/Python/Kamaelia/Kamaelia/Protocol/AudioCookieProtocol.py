#!/usr/bin/env python2.3
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
"""
Simple Audio based fortune cookie server

To listen to the sounds, on a linux box do this:

netcat <server ip> 1501 | aplay -

API Needs:

1) We don't/can't recieve notification from the ReadFileAdaptor that the
   file has been closed.
2) We can't actually tell the CSA to close itself down either...

EXTERNAL CONNECTORS
      * inboxes : inboxes=["datain","inbox"]
      * outboxes=["outbox"]

Copies everything from Datain & inbox to outbox.

Actually gets it's data from the command "afortune.pl" - which dumps out the
bytes of a random wav wav via a ReadFile Adaptor, reading from it at a constant
bit rate.
"""

import sys

from Axon.Component import component, scheduler, linkage, newComponent
from ReadFileAdaptor import ReadFileAdaptor
from SimpleServerComponent import SimpleServer

class AudioCookieProtocol(component):
   def __init__(self,filename="Ulysses", debug=0):
      self.__super.__init__()
      self.filename=filename
      self.debug = debug

   def initialiseComponent(self):
      myDataSource = ReadFileAdaptor(command="./afortune.pl",
                              readmode="bitrate",
                              bitrate=95200, chunkrate=25)
      assert self.debugger.note("AudioCookieProtocol.initialiseComponent", 1, "Initialising AudioCookieProtocol protocol handler ", self.name)
      self.link(	source=(myDataSource,"outbox"),
               sink=(self,"outbox"),
               passthrough=2)
      self.addChildren(myDataSource)

      return newComponent(  myDataSource  )

   def mainBody(self):
      """All the interesting work has been done by linking the file reader's output
      to our output"""
      return 1

if __name__ == '__main__':
   SimpleServer(protocol=AudioCookieProtocol, port=1500).activate()
   scheduler.run.runThreads(slowmo=0)
