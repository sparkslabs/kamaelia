#!/usr/bin/env python2.3
"""
RtpPacker Component
Takes data from a preframer:
   * Creates an RTP Header Object
   * Uses the timestamp & sample count to generate an RTP timestamp

"""
from Axon.Component import component, scheduler

class RtpPacker(component):
   Inboxes=["inbox"]   # List of inbox names if different
   Outboxes=["outbox"] # List of outbox names if different
   #Usescomponents=[] # List of classes used.
   def __init__(self,label,looptimes,selfstart=0):
      self.__super.__init__() # !!!! Must happen, if this method exists

   def initialiseComponent(self):
      return 1

   def mainBody(self):
      return 1

   def closeDownComponent(self):
      "closeDownComponent"
      pass

if __name__ =="__main__":
   # myComponent("A",3,1)
   # myComponent("B",2).activate()
   # scheduler.run.runThreads()
   pass
