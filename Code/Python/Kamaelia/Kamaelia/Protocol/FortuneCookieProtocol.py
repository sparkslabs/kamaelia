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
"""Simple fortune cookie protocol handler.

If run directly runs a simple 'fortune cookie protocol 'server.

Set it running, then telnet to the server on the port the server is listening on!
Specifically port 1500

EXTERNAL CONNECTORS
      * inboxes : inboxes=["datain","inbox"]
      * outboxes=["outbox"]

Copies everything from Datain & inbox to outbox.

Actually gets it's data from the command "fortune -a" - the normal unix command
which dumps out a random fortune cookie read via a ReadFile Adaptor, reading
from the command pipe at a constan bit rate.

"""

import sys

from Axon.Component import component, scheduler, linkage, newComponent
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.SimpleServerComponent import SimpleServer

class FortuneCookieProtocol(component):
   def __init__(self,filename="Ulysses", debug=0):
      self.__super.__init__()

      self.filename=filename
      self.debug = debug

   def initialiseComponent(self):
      myDataSource = ReadFileAdaptor(command="fortune -a",readmode="bitrate", bitrate=320, chunkrate=40)
      assert self.debugger.note("FortuneCookieProtocol.main", 1, self.name, "File Opened...")

      self.link(source=(myDataSource,"outbox"), sink=(self,"outbox"), passthrough=2)
      self.link((myDataSource,"signal"), sink=(self,"control"))
      assert self.debugger.note("FortuneCookieProtocol.main", 1, self.name, "Linked in")

      self.addChildren(myDataSource)
      assert self.debugger.note("FortuneCookieProtocol.main", 1, self.name, "Added Child", myDataSource)
      return newComponent(  myDataSource  )

   def mainBody(self):
      """All the interesting work has been done by linking the file reader's output
      to our output"""
      self.pause()
      if self.dataReady("control"):
         data = self.recv("control")
         self.send(data,"signal")
         print "FCP: SIGNAL PROPOGATED Upwards, Exiting protocol Handler"
         return 0
      assert self.debugger.note("FortuneCookieProtocol.main", 10, self.name, "Main Loop")
      return 1

   def closeDownComponent(self):
      print "FCP: Shutting down fortune cookies"

if __name__ == '__main__':
   SimpleServer(protocol=FortuneCookieProtocol, port=1501).activate()
   # HelloServer(debug = 1).activate()
   scheduler.run.runThreads(slowmo=0)
