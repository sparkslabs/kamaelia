#!/usr/bin/python

import time
from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component
from Kamaelia.Chassis.Graphline import Graphline
from Axon.Ipc import ipc

class partialShutdown(ipc):
   # This should be defined elsewhere but for the moment I'll put it here
   # since still testing ideas
   def __init__(self,direction,flush=False):
      self.direction = direction
      self.flush = flush


class ClosingSource(threadedcomponent):
   def main(self):

       tosend= ["hello", "world", "this" ]#, "is","a", "test", "so", "there"]
       t = time.time()
       print time.time()-t
       while tosend != [] or time.time()-t <= 2: # wait for final response(!)
           if tosend != []:
               if time.time()-t >= 1:
                   t = time.time()
                   data = tosend.pop(0)
                   self.send(data, "outbox")
           while self.dataReady("inbox"):
              data = self.recv("inbox")
              print "SOURCE RECV", time.time(), data
       print "Data source expired"
       print "Lets try half closing the connection"
       self.send(partialShutdown("send"), "signal")

class MockNetwork(component):
   def main(self):
      while 1:
         while self.dataReady("inbox"):
            self.send(self.recv())
         while self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, partialShutdown):
                if data.direction = "send" and not self.flush:
                   self.send(partialShutdown("read"), "signal")

class ResponderPinger(threadedcomponent):
   def main(self):
       while 1:
          while self.dataReady("inbox"):
             data = self.recv("inbox")
             print "RECV", time.time(), data
             self.send(data, "outbox")
          while self.dataReady("control"):
             data = self.recv("control")
             if isinstance(data, producerFinished):
                # other end has shut the connection, but the connection is still active
                # so we can continue sending - switch to send only state
                break
       print "Other end of connection closed for sending, but not receiving"

Graphline(
    CLIENTSIDE = ClosingSource(),
    SERVERSIDE = ResponderPinger(),
    linkages = {
        ("CLIENTSIDE", "outbox") : ("SERVERSIDE", "inbox"),
        ("SERVERSIDE", "outbox") : ("CLIENTSIDE", "inbox"),
    }
).run()