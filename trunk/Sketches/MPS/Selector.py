#!/usr/bin/python
#
import socket
import select
import Axon
from Axon.Ipc import status
import Axon.CoordinatingAssistantTracker as cat
from Kamaelia.KamaeliaIPC import shutdownCSA

class selectorComponent(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
   Inboxes = {
   }
   Outboxes = {
   }
   def __init__(self):
      super(selectorComponent, self).__init__()
      self.readers = []
      self.writers = []
      self.exceptions = []

   def handleNotify(self):
       M = self.recv("notify")
       if shutdownCSA(M):
           find and remove
       else
           managingComponent, selectable = M.payload
           wire in managingComponent
           add reference
           if M.canRead():
               self.readers.append(selectable)
           if M.canWrite(M)
               self.writers.append(selectable)
           if M.doesExcept(M)
               self.exceptions.append(selectable)
 
   def main(self):
       while 1:
          self.handleNotify()
          self.checkForClosedSockets()
          try:
              readables, writeables, excepts = select.select(self.readers, self.writers, self.exceptions,0)
              for sock in readables:
                  passBackResult = self.handleReadableSocket(sock)
                  if passBackResult:
                      yield passBackResult

              for sock in writeables:
                  passBackResult = self.handleWriteableSocket(sock)
                  if passBackResult:
                      yield passBackResult

              for sock in excepts:
                  passBackResult = self.handleExceptionSocket(sock)
                  if passBackResult:
                      yield passBackResult


          except socket.error,e:
              if e[0] is not 9:
                  raise e
          yield status("ready")

#
# The signatures of the things being rewritten.
#

class selectorComponent(AdaptiveCommsComponent):
   """\
   selectorComponent() -> new selectorComponent component

   Use selectorComponent.getSelectorService(...) in preference as it returns an
   existing instance, or automatically creates a new one.
   """
   
   Inboxes  = { "inbox"   : "NOT USED",
                "control" : "NOT USED",
                "notify"  : "newCSA(...) and shutdownCSA(...) notifications",
              }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "NOT USED",
              }
              
   requiredInboxes=["DataReady"]    # required inboxes on target component
   requiredOutboxes=["signal"]      # required outboxes on target component
   

def getSelectorService(tracker=None):
   """\
      Returns any live selector registered with the specified (or default) tracker,
      or creates one for the system to use.

      (Identical to selectorComponent.getSelectorService(...)
   """

__kamaelia_components__  = ( selectorComponent, )



if __name__ =="__main__":
   #_tests()
   x=selectorComponent()
   x.getSelectorService()
   x.validComponentInput((x,"str"))

