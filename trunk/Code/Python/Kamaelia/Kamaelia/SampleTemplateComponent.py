#!/usr/bin/env python2.3
"""
Sample Template Component.
Use this as the basis for your components!

"""
from Axon.Component import component, scheduler
class myComponent(component):
   #Inboxes=["inbox","control"] List of inbox names if different
   #Outboxes=["outbox","signal"] List of outbox names if different
   #Usescomponents=[] # List of classes used.
   def __init__(self,label,looptimes,selfstart=0):
      self.__super.__init__() # !!!! Must happen, if this method exists
      self.looptimes = looptimes
      self.label = label
      if selfstart:
         self.activate()

   def initialiseComponent(self):
      print "DEBUG:", self.label, "initialiseComponent"
      return 1

   def mainBody(self):
      print "DEBUG: ",self.label, "Now in the main loop"
      self.looptimes = self.looptimes -1
      return self.looptimes

   def closeDownComponent(self):
      print "DEBUG: ",self.label,"closeDownComponent"

if __name__ =="__main__":
   myComponent("A",3,1)
   myComponent("B",2).activate()
   scheduler.run.runThreads()
