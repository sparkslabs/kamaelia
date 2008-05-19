#!/usr/bin/env python

# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

"""\
==================
Text line splitter
==================

This component takes chunks of text and splits them at line breaks into
individual lines.



Example usage
-------------
A system that connects to a server and receives fragmented text data, but then
displays it a whole line at a time::
	    Pipeline( TCPClient(host=..., port=...),
              chunks_to_lines(),
              ConsoleEcho()
            ).run()
            

            
How does it work?
-----------------

chunks_to_lines buffers all text it receives on its "inbox" inbox. If there is a
line break ("\\n") in the text it has buffered, then it extracts that line of
text, including the line break character and sends it on out of its "outbox"
outbox.

It also removes any "\\r" characters in the text.

If a producerFinished() or shutdownMicroprocess() message is received on this
component's "control" inbox, then it will send it on out of its "signal" outbox
and immediately terminate. It will not flush any whole lines of text that may
still be buffered.
"""

from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished


class chunks_to_lines(component):
   """\
   chunks_to_lines() -> new chunks_to_lines component.
   
   Takes in chunked textual data and splits it at line breaks into individual
   lines.
   """
   
   Inboxes = { "inbox" : "Chunked textual data",
               "control" : "Shutdown signalling",
             }
   Outboxes = { "outbox" : "Individual lines of text",
                "signal" : "Shutdown signalling",
              }

   def main(self):
      """Main loop."""
      gotLine = False
      line = ""
      while 1: 
         
         while self.dataReady("inbox"):
            chunk = self.recv("inbox")
            chunk = chunk.replace("\r", "")
            line = line + chunk
         
         pos = line.find("\n")
         while pos > -1:
            self.send(line[:pos], "outbox")
            line = line[pos+1:] 
            pos = line.find("\n")
         
         if self.shutdown():
             return
         
         self.pause()
         yield 1

   def shutdown(self):
      """\
      Returns True if a shutdownMicroprocess or producerFinished message was received.
      """
      while self.dataReady("control"):
        msg = self.recv("control")
        if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
          self.send(msg,"signal")
          return True
      return False

__kamaelia_components__  = ( chunks_to_lines, )
