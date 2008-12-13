#!/usr/bin/env python2.3
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
====================
Console Input/Output
====================

The ConsoleEchoer component outputs whatever it receives to the console.

The ConsoleReader component outputs whatever is typed at the console, a line at
a time.



Example Usage
-------------
Whatever it typed is echoed back, a line at a time::
    pipeline( ConsoleReader(),
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
repr() will be used instead of str().

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
      while 1:
         line = raw_input(self.prompt)
         line = line + self.eol
         self.send(line, "outbox")



class ConsoleEchoer(component):
   """\
   ConsoleEchoer([forwarder][,use_repr]) -> new ConsoleEchoer component.

   A component that outputs anything it is sent to standard output (the
   console).

   Keyword arguments:
   - forwarder  -- incoming data is also forwarded to "outbox" outbox if True (default=False)
   - use_repr   -- use repr() instead of str() if True (default=False)
   """
   Inboxes  = { "inbox"   : "Stuff that will be echoed to standard output",
                "control" : "Shutdown signalling",
              }
   Outboxes = { "outbox" : "Stuff forwarded from 'inbox' inbox (if enabled)",
                "signal" : "Shutdown signalling",
              }

   def __init__(self, forwarder=False, use_repr=False):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(ConsoleEchoer, self).__init__()
      self.forwarder=forwarder
      if use_repr:
          self.serialise = repr
      else:
          self.serialise = str

   def main(self):
      """Main loop body."""
      while not self.shutdown():
          while self.dataReady("inbox"):
              data = self.recv("inbox")
              _sys.stdout.write(self.serialise(data))
              _sys.stdout.flush()
              if self.forwarder:
                  self.send(data, "outbox")
          self.pause()
          yield 1
          
   def shutdown(self):
       while self.dataReady("control"):
           data = self.recv("control")
           if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
               self.send(data,"signal")
               return True
       return 0
            
__kamaelia_components__  = ( ConsoleReader, ConsoleEchoer, )

if __name__ =="__main__":
   print "This module has no system test"

# RELEASE: MH, MPS
