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
Simple Server class.

Provides a framework for creating generic protocol handlers to
deal with information coming in on a single port (and a single
port only). This however covers a large array of server types.

This code is based on the code used for testing the Internet Connection
abstraction layer.

EXTERNAL CONNECTORS
      * inboxes : ["_oobinfo"]
      * outboxes=None

Strictly speaking _oobinfo isn't an external connector - it's used for plumbing
internal components into the Simple Server. (The PLS sends messages to
the Simple Server - such as "new connection" on this connector)

In practice, this component provides no external connectors for your use.
"""

import Axon as _Axon
from Axon import AxonObject as _AxonObject
import Kamaelia.Internet.TCPServer as _ic
import Kamaelia.KamaeliaIPC as _ki
import time as _time

class simpleServerProtocol(_Axon.Component.component):
   pass

class SimpleServer(_Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
   Inboxes=["_oobinfo"]
   Outboxes=[]
   def __init__(self, protocol=None, port=1601):
      super(SimpleServer, self).__init__()
      if not protocol:
         raise "Need a protocol to handle!"
      self.protocolhandlers = None
      self.protocolClass = protocol
      self.iter = 0
      self.time = _time.time()
      self.listenport = port

   def initialiseComponent(self):
      myPLS = _ic.TCPServer(listenport=self.listenport)
      self.link((myPLS,"protocolHandlerSignal"),(self,"_oobinfo"))
      self.addChildren(myPLS)
      return _Axon.Ipc.newComponent(myPLS)

   def mainBody(self):
      self.pause()
      result = self.checkOOBInfo()
      if result:
         return result
      if ((_time.time() - self.time) > 1):
         self.time = _time.time()

      self.iter = self.iter +1
      return 1

   def handleNewCSA(self, data):
      CSA = data.object
      pHandler = self.protocolClass()

      pHandlerShutdownOutbox= self.addOutbox("protocolHandlerShutdownSignal")
      assert self.debugger.note("SimpleServer.handleNewCSA",5,"Allocated shutdown signal box", pHandlerShutdownOutbox)

      self.trackResourceInformation(CSA, [], [pHandlerShutdownOutbox], pHandler)
      assert self.debugger.note("SimpleServer.handleNewCSA",5, "tracking resource")

      self.addChildren(CSA,pHandler)

      self.link((CSA,"outbox"),(pHandler,"inbox"))
      self.link((pHandler,"outbox"),(CSA,"DataSend"))

      self.link((CSA,"signal"),(self,"_oobinfo"))
      self.link((self,pHandlerShutdownOutbox), (pHandler, "control"))

      if "signal" in pHandler.Outboxes:
         self.link((pHandler,"signal"),(CSA, "control"))
         _Axon.Foo = CSA

      return _Axon.Ipc.newComponent(CSA,pHandler)

   def handleClosedCSA(self,data):
      assert self.debugger.note("SimpleServer.handleClosedCSA",1,"handling Closed CSA", data)
      CSA = data.caller
      bundle=self.retrieveTrackedResourceInformation(CSA)
      inboxes,outboxes,pHandler = bundle
      self.send(_ki.socketShutdown(),outboxes[0])
      assert self.debugger.note("SimpleServer.handleClosedCSA",1,"Removing ", CSA.name, pHandler.name, outboxes[0])
      self.removeChild(CSA)
      self.removeChild(pHandler)
      self.deleteOutbox(outboxes[0])
      self.ceaseTrackingResource(CSA)
      assert self.debugger.note("SimpleServer.handleClosedCSA",5, "GRRR... ARRRGG")

   def checkOOBInfo(self):
      if self.dataReady("_oobinfo"):
         data = self.recv("_oobinfo")
         if isinstance(data,_ki.newCSA):
            return self.handleNewCSA(data)
         if isinstance(data,_ki.socketShutdown):
            assert self.debugger.note("SimpleServer.checkOOBInfo", 1, "SimpleServer : Client closed itself down")
            self.handleClosedCSA(data)

if __name__ == '__main__':

   from Axon.Scheduler import scheduler
   class SimpleServerTestProtocol(simpleServerProtocol):
      def __init__(self):
         super(SimpleServerTestProtocol, self).__init__()
         assert self.debugger.note("SimpleServerTestProtocol.__init__",1, "Starting test protocol")

      def mainBody(self):
         if self.dataReady("inbox"):
            data = self.recv("inbox")
            print "Got data", data
            assert self.debugger.note("SimpleServerTestProtocol.mainBody",1, "NetServ : We were sent data - ")
            assert self.debugger.note("SimpleServerTestProtocol.mainBody",1, "We should probably do something with it now? :-)")
            assert self.debugger.note("SimpleServerTestProtocol.mainBody",1, "I know, let's sling it straight back at them :-)")
            self.send(data,"outbox")
         if self.dataReady("control"):
            data = self.recv("control")
            return 0
         return 1

      def closeDownComponent(self):
         assert self.debugger.note("SimpleServerTestProtocol.closeDownComponent",1, "Closing down test protcol")

   SimpleServer(protocol=SimpleServerTestProtocol).activate()
   scheduler.run.runThreads(slowmo=0)
