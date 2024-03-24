#!/usr/bin/python
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
"""
====================
Console Input/Output
====================

The ConsoleEchoer component outputs whatever it receives to the console.

The ConsoleReader component outputs whatever is typed at the console, a line at
a time.



Example Usage
-------------

Whatever it typed is echoed back, a line at a time::

    Pipeline( ConsoleReader(),
              ConsoleEchoer()
            ).run()



How does it work?
-----------------

ConsoleReader is a threaded component. It provides a 'prompt' at which you can
type. Your input is taken, a line a a time, and output to its "outbox" outbox,
with the specified end-of-line character(s) suffixed onto it.

The ConsoleReader component ignores any input on its "inbox" and "control"
inboxes. It does not output anything from its "signal" outbox.

The ConsoleReader component does not terminate.

The ConsoleEchoer component receives data on its "inbox" inbox. Anything it
receives this way is displayed on standard output. All items are passed through
the str() builtin function to convert them to strings suitable for display.

However, if the 'use_repr' argument is set to True during initialization, then
repr() will be used instead of str(). Similarly if a "tag" is provided it's
prepended before the data.

If the 'forwarder' argument is set to True during initialisation, then whatever
is received is not only displayed, but also set on to the "outbox" outbox
(unchanged).

If a producerFinished or shutdownMicroprocess message is received on the
ConsoleEchoer component's "control" inbox, then it is sent on to the "signal"
outbox and the component then terminates.
"""

from Axon.Component import component, scheduler
from Axon.Ipc import producerFinished, shutdownMicroprocess
import sys as _sys

from Axon.ThreadedComponent import threadedcomponent

class ConsoleReader(threadedcomponent):
   """\
   ConsoleReader([prompt][,eol]) -> new ConsoleReader component.

   Component that provides a console for typing in stuff. Each line is output
   from the "outbox" outbox one at a time.
   
   Keyword arguments:
   
   - prompt  -- Command prompt (default=">>> ")
   - eol     -- End of line character(s) to put on end of every line outputted (default is newline)
   """
   
   Inboxes  = { "inbox"   : "NOT USED",
                "control" : "NOT USED",
              }
   Outboxes = { "outbox" : "Lines that were typed at the console",
                "signal" : "NOT USED",
              }
   
   def __init__(self, prompt=">>> ",eol="\n"):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(ConsoleReader, self).__init__()
      self.prompt = prompt
      self.eol = eol

   def main(self):
      """Main thread loop."""
      while not self.shutdown():       # XXXX: NOTE We check self.shutdown *AFTER* waiting for input, meaning
         line = input(self.prompt)     # XXXX: NOTE the last line *will* be read. This is probably good
         line = line + self.eol        # XXXX: NOTE  motivation at some point for moving away from using
         self.send(line, "outbox")     # XXXX: NOTE  input.

   def shutdown(self):
       while self.dataReady("control"):
           data = self.recv("control")
           if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
               self.send(data,"signal")
               return True
       return 0


class ConsoleEchoer(component):
   """\
   ConsoleEchoer([forwarder][,use_repr][,tag]) -> new ConsoleEchoer component.

   A component that outputs anything it is sent to standard output (the
   console).

   Keyword arguments:
   
   - forwarder  -- incoming data is also forwarded to "outbox" outbox if True (default=False)
   - use_repr   -- use repr() instead of str() if True (default=False)
   - tag -- Pre-pend this text tag before the data to emit
   """
   Inboxes  = { "inbox"   : "Stuff that will be echoed to standard output",
                "control" : "Shutdown signalling",
              }
   Outboxes = { "outbox" : "Stuff forwarded from 'inbox' inbox (if enabled)",
                "signal" : "Shutdown signalling",
              }

   def __init__(self, forwarder=False, use_repr=False, tag=""):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(ConsoleEchoer, self).__init__()
      self.forwarder=forwarder
      if use_repr:
          self.serialise = repr
      else:
          self.serialise = str
      self.tag = tag

   def main(self):
      """Main loop body."""
      shutdown = False
      while not shutdown:
          for data in self.Inbox("inbox"):
              _sys.stdout.write(self.tag + self.serialise(data))
              _sys.stdout.flush()
              if self.forwarder:
                  self.send(data, "outbox")
          if self.dataReady("control"):
              shutdown = True
          else:
              self.pause()
          yield 1

      for msg in self.Inbox("control"):
          self.send(msg, "signal")
            
__kamaelia_components__  = ( ConsoleReader, ConsoleEchoer, )

if __name__ =="__main__":
   print ("This module has no system test")

# RELEASE: MH, MPS
