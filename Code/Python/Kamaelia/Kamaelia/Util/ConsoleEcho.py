#!/usr/bin/env python2.3
"""
Console Echoer Component. Optionally passes the data it recieves through to
it's outbox - making it useful for inline (or end of line) debugging.

"""
from Axon.Component import component, scheduler
import sys as _sys
class consoleEchoer(component):
   Inboxes=["inbox","control"]
   Outboxes=["outbox"]

   def __init__(self, forwarder=False):
      self.__super.__init__()# !!!! Must happen, if this method exists
      self.forwarder=forwarder

   def mainBody(self):
      if self.dataReady("inbox"):
         data = self.recv("inbox")
         _sys.stdout.write(data)
         _sys.stdout.flush()
         if self.forwarder:
            self.send(data, "outbox")
            return 1
         return 2
      if self.dataReady("control"):
         data = self.recv("control")
         if data == "shutdown":
            return 0
      return 3

if __name__ =="__main__":
   print "This module has no system test"
#   myComponent("A",3,1)
#   myComponent("B",2).activate()
#   scheduler.run.runThreads()
