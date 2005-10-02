#!/usr/bin/python
#
#
#

from Axon.Component import component

class fanout(component):
   Outboxes = ["outbox", "signal"]
   def __init__(self, boxnames):
      self.Outboxes = list(self.__class__.Outboxes) # Copy the class outboxes into the instance outboxes
      self.Outboxes.extend(boxnames)
      super(fanout, self).__init__()
   def main(self):
      while 1:
         if self.dataReady("inbox"):
            data = self.recv("inbox")
            for boxname in self.Outboxes:
               self.send(data, boxname)
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("shutdown", "signal")
               return
         yield 1
