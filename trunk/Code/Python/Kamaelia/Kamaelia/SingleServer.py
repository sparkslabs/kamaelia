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
only allows a single connection to occur. Any data received on that
connection is sent to the component's outbox, and any data received on its
inbox is sent to the connection.
"""

import Axon as _Axon
from Kamaelia.Internet.TCPServer import TCPServer
import Kamaelia.KamaeliaIPC as _ki
from Axon.Ipc import producerFinished

class echo(_Axon.Component.component):
   def main(self):
      while 1:
         if self.dataReady("inbox"):
            self.send(self.recv("inbox"), "outbox")
         yield 1

class SingleServer(_Axon.Component.component):
   Inboxes=["inbox","control", "_oobinfo"]
   Outboxes=["outbox", "signal", "_CSA_signal"]
   def __init__(self, port=1601):
      self.__super.__init__()
      self.listenport = port
      self.CSA = None

   def main(self):
      myPLS = TCPServer(listenport=self.listenport)
      self.link((myPLS,"protocolHandlerSignal"),(self,"_oobinfo"))
      self.addChildren(myPLS)
      yield _Axon.Ipc.newComponent(myPLS)
      while 1:
         self.pause()
         if self.dataReady("_oobinfo"):
            data = self.recv("_oobinfo")
            if isinstance(data,_ki.newCSA):
               yield self.handleNewCSA(data)
            if isinstance(data,_ki.socketShutdown):
               # Socket shutdown and died.
               # This means we should keel over again.
               self.send(producerFinished(self), "signal")
               yield 0
               return
         yield 1

   def handleNewCSA(self, data):
      if self.CSA is None:
         self.CSA = data.object

         # Wire in the CSA to the outside connectivity points
         self.link((self.CSA,"outbox"),(self,"outbox"), passthrough=2)
         self.link((self,"inbox"),(self.CSA,"DataSend"), passthrough=1)

         self.link((self.CSA,"signal"),(self,"_oobinfo"))
         self.link((self,"_CSA_signal"), (self.CSA, "control"))

         self.addChildren(self.CSA)
         return _Axon.Ipc.newComponent(self.CSA)

      else:
         # We already have a connected socket, so we want to throw this connection away.
         print "Already have connection"
         CSA = data.object
         CSA._deliver(producerFinished(self),"control")
         return 1

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

