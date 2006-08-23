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
"""
==============================
Simple Fortune Cookie Protocol
==============================

Simple fortune cookie protocol handler, that emits a fortune cookie (at 40
characters/second) then disconnects.



Example Usage
-------------
::
    >>> SimpleServer(protocol=FortuneCookieProtocol, port=1500).run()

On a *nix client::
    > telnet <server ip> 1500
    Trying <server ip>...
    Connected to <server ip>...
    "I love Saturday morning cartoons, what classic humour!  This is what
    entertainment is all about ... Idiots, explosives and falling anvils."
                    -- Calvin and Hobbes, Bill Watterson
    Connection closed by foreign host.
    >



How does it work?
-----------------

The component gets it's data from the command "fortune -a" - the normal unix
command which dumps out a random fortune cookie - read via a ReadFileAdaptor,
reading from the command pipe at a constant bit rate. The ReadFileAdaptor is
wired up so that data is passed through to the FortuneCookieProtocol's "outbox"
outbox.

At the end of the cookie, the FortuneCookieProtocol component terminates,
closing the connection (it receives and passes on the producerFinished message
generated by the ReadFileAdapter component).
"""


import sys

from Axon.Component import component
from Axon.Ipc import newComponent
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor

class FortuneCookieProtocol(component):
   """\
   FortuneCookieProtocol([debug]) -> new FortuneCookieProtocol component.

   A protocol that spits out a random fortune cookie, then terminates.

   Keyword arguments:
   - debug  -- Debugging output control (default=0)
   """
   
   def __init__(self, debug=0):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(FortuneCookieProtocol, self).__init__()

      self.debug = debug

   def initialiseComponent(self):
      """\
      Initialises component. Sets up a ReadFileAdapter to read the result of
      running 'fortune'.
      """
      myDataSource = ReadFileAdaptor(command="fortune -a",readmode="bitrate", bitrate=320, chunkrate=40)
      assert self.debugger.note("FortuneCookieProtocol.main", 1, self.name, "File Opened...")

      self.link(source=(myDataSource,"outbox"), sink=(self,"outbox"), passthrough=2)
      self.link((myDataSource,"signal"), sink=(self,"control"))
      assert self.debugger.note("FortuneCookieProtocol.main", 1, self.name, "Linked in")

      self.addChildren(myDataSource)
      assert self.debugger.note("FortuneCookieProtocol.main", 1, self.name, "Added Child", myDataSource)
      return newComponent(  myDataSource  )

   
   def mainBody(self):
      """\
      Main body.

      All the interesting work has been done by linking the file reader's output
      to our output.  Messages sent to control are unchecked and the first
      message causes the component to exit.
      """
      self.pause()
      while self.dataReady("control"):
         data = self.recv("control")
         self.send(data,"signal")
         return 0
      assert self.debugger.note("FortuneCookieProtocol.main", 10, self.name, "Main Loop")
      return 1

__kamaelia_components__  = ( FortuneCookieProtocol, )

   
if __name__ == '__main__':
   from Kamaelia.SimpleServerComponent import SimpleServer
   
   SimpleServer(protocol=FortuneCookieProtocol, port=1500).run()
