#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
This is a simpler server than the SimpleServer component. Specifically it
only allows a single connection to occur at a time. Any data received on that
connection is sent to the component's outbox, and any data received on its
inbox is sent to the connection.
When a connection closes, it sends a producerFinished signal.

TODO:
If there is already a connection, then any new connections are shutdown. It would
be better if they weren't accepted in the first place, but that requires changes to
TCPServer.
"""

import Axon as _Axon
from Kamaelia.Internet.TCPServer import TCPServer
import Kamaelia.IPC as _ki
from Axon.Ipc import producerFinished
from Kamaelia.IPC import serverShutdown

class echo(_Axon.Component.component):
   def main(self):
      while 1:
         if self.dataReady("inbox"):
            self.send(self.recv("inbox"), "outbox")
         yield 1

class SingleServer(_Axon.Component.component):
   Inboxes= { "inbox"    : "Data received on this inbox is sent to the first client who connects",
              "control"  : "Default inbox, not actually listened to",  
              "_oobinfo" : "We receive notification of connection on this inbox"
            }
   Outboxes={ "outbox"      : "Any data received from the first connection accepted is sent to this outbox",
              "signal"      : "When the client disconnects a producerFinished message is sent here", 
              "_CSA_signal" : "Outbox for sending messages to the CSA. Currently unused."
            }
   def __init__(self, port=1601):
      super(SingleServer,self).__init__()
      self.listenport = port
      self.CSA = None
      self.rejectedCSAs = []
      self.myPLS = None

   def main(self):
      self.myPLS = TCPServer(listenport=self.listenport)
      self.link((self.myPLS,"protocolHandlerSignal"),(self,"_oobinfo"))
      self.addChildren(self.myPLS)
      yield _Axon.Ipc.newComponent(self.myPLS)
      while 1:
         self.pause()
         if self.dataReady("_oobinfo"):
            data = self.recv("_oobinfo")
            if isinstance(data,_ki.newCSA):
               yield self.handleNewCSA(data)
            if isinstance(data,_ki.shutdownCSA):# socketShutdown):
               # Socket shutdown and died.
               # Unlink the CSA. A new one might connect!
               theCSA = data.object
               if theCSA in self.rejectedCSAs:
                   self.rejectedCSAs.remove(theCSA)
               else:
                   self.send(producerFinished(self), "signal")
                   self.CSA = None
               self.removeChild(theCSA)
               yield 1
         yield 1

   def stop(self):
       self.send(producerFinished(self), "signal")
       self.CSA._deliver(producerFinished(self),"control")
       self.myPLS._deliver(serverShutdown(self),"control")
       super(SingleServer,self).stop()

   def handleNewCSA(self, data):
      newCSA = data.object
      if self.CSA is None:
         self.CSA = newCSA

         # Wire in the CSA to the outside connectivity points
         self.link((self.CSA,"outbox"),(self,"outbox"), passthrough=2)
         self.link((self,"inbox"),(self.CSA,"inbox"), passthrough=1)
         self.link((self,"_CSA_signal"), (self.CSA, "control"))

      else:
         # We already have a connected socket, so we want to throw this connection away.
         # we'll send it a stop signal, but we still need to add it to the scheduler
         # otherwise itdoesn't get a chance to act on it. We'll add it to a 'rejected'
         # list so we know to clean it up slightly differently when we get told it has
         # shut down
         newCSA._deliver(producerFinished(self),"control")
         self.rejectedCSAs.append(newCSA)

      self.addChildren(newCSA)
      return _Axon.Ipc.newComponent(newCSA)

__kamaelia_components__  = ( SingleServer, echo )


if __name__ == '__main__':
   from Axon.Scheduler import scheduler

   class SimplisticServer(_Axon.Component.component):
      def main(self):
         server = SingleServer(port=1501)
         handler = echo()
         self.link((server, "outbox"), (handler, "inbox"))
         self.link((server, "signal"), (handler, "control"))
         self.link((handler, "outbox"), (server, "inbox"))
         self.link((handler, "signal"), (server, "control"))

         self.addChildren(server, handler)
         yield _Axon.Ipc.newComponent(*(self.children))
         while 1:
            self.pause()
            yield 1

   t = SimplisticServer()
   t.activate()
   scheduler.run.runThreads(slowmo=0)

