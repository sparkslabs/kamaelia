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
Console Echoer Component. Optionally passes the data it recieves through to
it's outbox - making it useful for inline (or end of line) debugging.

"""
from Axon.Component import component, scheduler
from Axon.Ipc import producerFinished, shutdownMicroprocess
import sys as _sys

from Axon.ThreadedComponent import threadedcomponent

class ConsoleReader(threadedcomponent):
   def __init__(self, prompt=">>> ",eol="\n"):
      super(ConsoleReader, self).__init__()
      self.prompt = prompt
      self.eol = eol

   def run(self):
      while 1:
         line = raw_input(self.prompt)
         line = line + self.eol
         self.outqueues["outbox"].put(line)

class consoleEchoer(component):
   Inboxes=["inbox","control"]
   Outboxes=["outbox","signal"]

   def __init__(self, forwarder=False, use_repr=False):
      super(consoleEchoer, self).__init__()# !!!! Must happen, if this method exists
      self.forwarder=forwarder
      if use_repr:
          self.serialise = repr
      else:
          self.serialise = str

   def mainBody(self):
      if self.dataReady("inbox"):
         data = self.recv("inbox")
         _sys.stdout.write(self.serialise(data))
         _sys.stdout.flush()
         if self.forwarder:
            self.send(data, "outbox")
            return 1
         return 2
      if self.dataReady("control"):
         data = self.recv("control")
         if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
            return 0
      return 3

if __name__ =="__main__":
   print "This module has no system test"
#   myComponent("A",3,1)
#   myComponent("B",2).activate()
#   scheduler.run.runThreads()
