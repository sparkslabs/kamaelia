#!/usr/bin/env python2.3
"""
Echo Protocol Component

Based on the test code for the ICA & Simple Server.
Simply copies it's input to it's output.

EXTERNAL CONNECTORS
      * inboxes : ["inbox"]
      * outboxes=["outbox"])
   Data recieved on "inbox" is copied to "outbox"
"""

from Axon.Component import component, scheduler

class EchoProtocol(component):
   import time
   allEchoers = []
   def __init__(self):
      self.__super.__init__() # Accept default in/outboxes
      EchoProtocol.allEchoers.append(self)

   def mainBody(self):
      self.pause()
      if self.dataReady("inbox"):
         data = self.recv("inbox")
         #print "NetServ : We were sent data - "
         #print "We should probably do something with it now? :-)"
         #print "I know, let's sling it straight back at them :-)"
         self.send(data,"outbox")
      return 1

if __name__ == '__main__':
   from SimpleServerComponent import SimpleServer

   SimpleServer(protocol=EchoProtocol, port=1501).activate()
   scheduler.run.runThreads(slowmo=0)
