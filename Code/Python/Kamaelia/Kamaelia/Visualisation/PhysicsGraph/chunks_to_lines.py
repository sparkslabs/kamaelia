#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
      while not self.shutdown(): 
         
         while self.dataReady("inbox"):
            chunk = self.recv("inbox")
            chunk = chunk.decode("utf8")
            try:
                chunk = chunk.replace("\r", "")
            except:
                print ("BAD CHUNK, Arrrgggh", repr(chunk))
                import time
                time.sleep(3)
                raise

            line = line + chunk
         
         pos = line.find("\n")
         while pos > -1:
            self.send(line[:pos], "outbox")
            line = line[pos+1:] 
            pos = line.find("\n")
         
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
