#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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

FastRestartSingleServer is exactly the same as SingleServer, expect its default is
to set appropriate socket options to allow the server to restart instantly. This isn't
the traditional default because in kamaelia we prefer to follow the defaults of the
OS, rather than local defaults.
"""

import socket
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
   port = 1601
   socketOptions=None
   TCPS=TCPServer
   def __init__(self, **argd):
      super(SingleServer,self).__init__(**argd)
      self.listenport = self.port # avoid complete rewrite, should santise and make consistent.
      self.CSA = None
      self.rejectedCSAs = []
      self.myPLS = None

   def main(self):
      if self.socketOptions is None:
          self.myPLS = (self.TCPS)(listenport=self.port)
      else:
          self.myPLS = (self.TCPS)(listenport=self.port, socketOptions=self.socketOptions)
      
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

class FastRestartSingleServer(SingleServer):
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

__kamaelia_components__  = ( SingleServer, FastRestartSingleServer, echo )


if __name__ == '__main__':
   from Axon.Scheduler import scheduler

   class SimplisticServer(_Axon.Component.component):
      def main(self):
         server = SingleServer(port=1501, socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1))
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

