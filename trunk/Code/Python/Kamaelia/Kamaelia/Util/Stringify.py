#!/usr/bin/env python2.3
"""
A simple component that takes objects in on its inbox, creates a stringized
version and returns that.

"""
from Axon.Component import component, scheduler
class ToStringComponent(component):
   #Inboxes=["inbox"] List of inbox names if different
   #Outboxes=["outbox"] List of outbox names if different
   #Usescomponents=[] # List of classes used.
   def __init__(self):
      self.__super.__init__() # !!!! Must happen, if this method exists
      self.activate()

   def initialiseComponent(self):
      return 1

   def mainBody(self):
      if self.dataReady("inbox"):
         theData = self.recv("inbox")
         self.send(str(theData), "outbox")
      return 1

   def closeDownComponent(self):
      pass

if __name__ =="__main__":
   myComponent("A",3,1)
   myComponent("B",2).activate()
   scheduler.run.runThreads()
