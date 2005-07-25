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
#
# TCP Server Socket class
#
# The TCP Server component provides a component for building a TCP based
# network server. You specify a single port number, the system then hunts
# for a selector process, and waits for new connection messages from the
# selector.
#
# When the Server recieves a new connection it performs an accept, and creates
# a connected socket adaptor (CSA) to handle the activity on that connection. This
# CSA is then passed to the TCP Server's protocolHandlerSignal outbox.
# (Internally the CSA is also currently handed over to a selector service to perform
# activity checking)
#
# Inboxes:
#    * DataReady - Data ready on a server socket means the TCP server should
#                    accept a new connection.
#    * _csa_feedback - We recieve feedback from Connected Socket adaptors
#                    on this inbox. Currently this feedback is limited to connection
#                    shutdown messages.
#
# Outboxes:
#    * protocolHandlerSignal - This is used to send a connected socket adaptor
#                    component back to the protocol handler level.
#    * signal - Used to communiate with the selector sending either NewCSA
#                    messages
#
# The client using the TCPServer is then expected to deal with the input/output
# required directly with the CSA. (See SimpleServer component example)
#
# Essentially the steps are:
#    * Create a TCP Server
#    * Wait for CSA messages from the TCP Server
#    * Send what you like to CSA's, ensure you recieve data from the CSAs
#    * Send shutdown messages when done.

import socket, errno, random, Axon, Selector
import Kamaelia.KamaeliaIPC as _ki
from Kamaelia.Internet.ConnectedSocketAdapter import ConnectedSocketAdapter

_component = Axon.Component.component
status = Axon.Ipc.status
wouldblock = Axon.Ipc.wouldblock
import time

class TCPServer(_component):
   Inboxes=["DataReady", "_csa_feedback"]
   Outboxes=["protocolHandlerSignal", "signal","_selectorSignal"]

   def __init__(self,listenport):
      super(TCPServer, self).__init__()
      self.listenport = listenport
      self.listener,junk = self.makeTCPServerPort(listenport, maxlisten=5)

   def makeTCPServerPort(self, suppliedport=None, HOST=None, minrange=2000,maxrange=50000, maxlisten=5):
      if HOST is None: HOST=''
      if suppliedport is None:
         PORT=random.randint(minrange,maxrange) # Built in support for testing
      else:
         PORT=suppliedport

      s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.setblocking(0)
      assert self.debugger.note("PrimaryListenSocket.makeTCPServerPort", 5, "HOST,PORT",":",HOST,":",PORT,":")
      s.bind((HOST,PORT))
      s.listen(maxlisten)
      return s,PORT

   def createConnectedSocket(self, sock):
      tries = 0
      maxretries = 10
      gotsock=False
      newsock, addr = sock.accept()  # <===== THIS IS THE PROBLEM
      gotsock = True
      newsock.setblocking(0)
      CSA = ConnectedSocketAdapter(newsock)
      return CSA

   def closeSocket(self, shutdownMessage):
      theComponent,sock = shutdownMessage.caller, shutdownMessage.message
      sock.close()
      # tell the selector about it shutting down
      self.send(_ki.shutdownCSA(self, (theComponent, theComponent.socket)), "_selectorSignal")
      # tell protocol handlers
      self.send(_ki.shutdownCSA(self, theComponent), "protocolHandlerSignal")# "signal")
      # Delete the child component
      self.removeChild(theComponent)

   def checkForClosedSockets(self):
      if self.dataReady("_csa_feedback"):
         data = self.recv("_csa_feedback")
         if isinstance( data, _ki.socketShutdown):
            self.closeSocket(data)

   def initialiseComponent(self):
      """ What else do we do with a selector?
        * We want it to send us messages when our listen socket is ready.
        * These messages tell us that a new connection is ready, and we should do
          something with it. Anything else? Not yet.
        * Client creates a link from it's own internal linkages to the selector service.
        * Then sends the selector service a message.
        * Basically the same idiom needed here.
      """
      selectorService, newSelector = Selector.selectorComponent.getSelectorService(self.tracker)
      if newSelector:
         self.addChildren(newSelector)
      self.link((self, "_selectorSignal"),selectorService)
      self.send(_ki.newServer(self, (self,self.listener)), "_selectorSignal")
      return Axon.Ipc.newComponent(*(self.children))

   def handleNewConnection(self):
      if self.dataReady("DataReady"):
         data = self.recv("DataReady")
         # If we recieve information on data ready, for a server it means we have a new connection
         # to handle
         try:
            CSA = self.createConnectedSocket(self.listener)
         except socket.error, e:
            (errorno,errmsg) = e
            if errorno != errno.EAGAIN:
               if errorno != errno.EWOULDBLOCK:
                  raise e
         else:
            self.send(_ki.newCSA(self, CSA), "protocolHandlerSignal")
            self.addChildren(CSA)
            self.link((CSA, "FactoryFeedback"),(self,"_csa_feedback"))
            self.send(_ki.newCSA(CSA, (CSA,CSA.socket)), "_selectorSignal")
            return CSA

   def mainBody(self):
      self.pause()
      self.checkForClosedSockets()
      self.handleNewConnection() # Data ready means that we have a connection waiting.
      return status("ready")

if __name__ == '__main__':
   print "Simple integration test moved out to InternetHandlingTests.py"
