#!/usr/bin/env python2.3
"""
=========================================================================

THIS FILE IS RETIRED FOR NOW SINCE IT'S BEEN SUPERCEDED BY THE TCPServer,
CSA, TCPClient, Selector, etc components - to allow better code reuse
between clients and servers

=========================================================================

Internet Connection Abstraction Layer

This layer provides components for running a TCP server, and dealing with
connected sockets. Essentially it boils down to:
   * Create a Primary Listen Socket handler to listen for new connections.
   * Wait for the PLS to send a Connected Socket Adaptor to us - signalling
   a new connection.
   * Plumb a protocol handler into handling the CSA, and wait for shutdown
   messages, and then deallocate.

   For example usage, see:
      * SimpleServerComponent.py, EchoProtocolComponent.py,
      FortuneCookieServer.py

EXTERNAL CONNECTORS
   PRIMARY LISTENER SOCKET
      * inboxes=["DataSend", "control", "_csa_feedback"],
         * DataSend - 'legacy' - not used, deleting soon.
         * control - As yet, unused, will be used to control aspects of the
         connection whilst it is open.
         * _csa_feedback - "Internal" box - the CSA created for a connection
         signals into this inbox that the connection has died, so that the PLS
         can deallocate the socket etc.
      * outboxes=["protocolHandlerSignal", "DataRecieve"])
         * protocolHandlerSignal - largely used to signal the client of the PLS that a new
         connection has been recieved, and this is communicated in a message
         of the form {'newCSA': CSA}
         * DataRecieve - 'legacy' - not used, deleting soon.

   CONNECTED SOCKET ADAPTOR
      * inboxes=DataReady, DataSend, Initialise, control
         * DataReady - this is a private connector, which tells the
         component to read from the socket. It is used by the PLS
         that created this component to tell the CSA that there is
         data ready for reading from the socket.
         * DataSend - a user of this component would expect to connect
         a linkage to this inbox - since this is the inbox whereby recieved
         data is sent to the client as soon as possible.
         * Initialise - not actually used for anything, candidate for removal.
         * control - standard control inbox, the socket will close connection
         when there is nothing left in its DataSend and DataReady boxes if it is
         sent a Axon.Ipc.producerFinished ipc object.
      * outboxes=outbox, FactoryFeedback, signal
         * outbox - Any data recieved from the socket will be made available
         on this outbox.
         * FactoryFeedback - In order to signal to the Primary Listener that the socket
         has died, this outbox is made available for signalling purposes.
         * signal - This performs a similar function, but is intended for use by
         the client of the CSA - ie what ever is actually expecting data from the
         CSA. You should check the signal for a message of the form:
         {'shutdownCSA': CSA} periodically to check whether the client
         has disappeared or not!
"""
import select
import socket
import fcntl
import os
import sys
import time
import exceptions
import random

import Axon
_component = Axon.Component.component
status = Axon.Ipc.status
wouldblock = Axon.Ipc.wouldblock
import socketConstants

# Wise to do for us - wise to do for people importing from us?
from KamaeliaExceptions import *
from KamaeliaIPC import *

from ConnectedSocketAdapter import ConnectedSocketAdapter
import Selector

# PrimaryListenSocket component class
#
# The Primary Listen Socket component provides a component
# for building a TCP based network server. You specify a list of
# port numbers to listen on locally, and this component then  creates
# them, and sits there listening on them. When it recieves a connection,
# it creates a connected socket adaptor component (above), and passes
# this in a message of the form {'newCSA': CSAObject} to its local
# "OOBInfo" outbox.
#
# The client using the PLS is then expected to deal with the input/output
# required directly with the CSA. (See SimpleServer component example)
# External connectors:
#    * inboxes=["DataSend","OOBcontrol", "_csa_feedback"],
#         * DataSend - 'legacy' - not used, deleting soon.
#         * OOBControl - As yet, unused, will be used to control aspects of the
#           connection whilst it is open.
#         * _csa_feedback - "Internal" box - the CSA created for a connection
#           signals into this inbox that the connection has died, so that the PLS
#           can deallocate the socket etc.
#    * outboxes=["OOBInfo", "DataRecieve"])
#         * OOBInfo - largely used to signal the client of the PLS that a new
#           connection has been recieved, and this is communicated in a message
#           of the form {'newCSA': CSA}
#         * DataRecieve - 'legacy' - not used, deleting soon.
#
class PrimaryListenSocket(_component):
   # This should be using a selector as the control mechanism
   Inboxes=["DataReady","DataSend","control", "_csa_feedback", "_socketFeedback"]
   Outboxes=["protocolHandlerSignal", "DataRecieve","signal"]


   def __init__(self,listenports=list()):
      self.__super.__init__()

      self.listenports = listenports
      self.listeners = self.makeListenPorts(listenports)
      self.writers = list()
      self.serversocks = [ sock for sock in self.listeners ]
      self.lookup = {}
      self.postoffice.debugname = "PLSPostman"

   def handleDataReady(self):
      pass
#      if self.dataReady("DataReady"):
#      #
#         data = self.recv("DataReady")
#         if (isinstance(data, status)):
#            socketdata = None
#            try:
#               socketdata = _saferecv(self.socket, 1024) ### Receiving may die horribly
#            except connectionDiedReceiving, cd:
#               raise cd # rethrow
#            except Exception, e: # Unexpected error that might cause crash. Do we want to really crash & burn?
#               if crashAndBurn["receivingDataFailed"]:
#                  raise e
#            if (socketdata):
#               self.send(socketdata, "outbox")

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
# This is what we want to do.

      return s,PORT

   def makeListenPorts(self,listenports, HOST=""):
      listeners = list()
      for port in listenports:
         s, port = self.makeTCPServerPort(port,HOST, maxlisten=5)
         listeners.append(s)
      return listeners

   def __str__(self):
      result = "PrimaryListenSocket [[[ " + _component.__str__(self) + " ]]]"
      return result

   def createConnectedSocket(self, sock):
      newsock, addr = sock.accept()
      newsock.setblocking(0)
      self.listeners.append(newsock)
      CSA = ConnectedSocketAdapter(newsock)
      self.lookup[id(newsock)] = CSA
      return CSA

   def closeSocket(self, shutdownMessage):
      theComponent,sock = shutdownMessage.caller, shutdownMessage.message
      sock.close()
      self.listeners.remove(sock)
      self.removeChild(theComponent)
      del self.lookup[id(sock)]

   def checkForClosedSockets(self):
      if self.dataReady("_csa_feedback"):
         data = self.recv("_csa_feedback")
         if isinstance( data, socketShutdown):
            self.closeSocket(data)

   def initialiseComponent(self):
      selectorService, newSelector = Selector.selectorComponent.getSelectorService(self.tracker)
      if newSelector:
         self.addChildren(newSelector)

         """ What else do we do with a selector?
        * We want it to send us messages when our listen socket is ready.
        * These messages tell us that a new connection is ready, and we should do
          something with it. Anything else? Not yet.

        * Client creates a link from it's own internal linkages to the selector service.
        * Then sends the selector service a message.
        * Basically the same idiom needed here.
         """
      self.link((self, "signal"),selectorService)
      print "This?"
#      self.send(newServer(self, (self,sock)), "signal")

      return Axon.Ipc.newComponent(*(self.children))

   #
   # This is largely the selector code.
   #
   def mainBody(self):
      self.checkForClosedSockets()
      readables, writeables, excepts = select.select(self.listeners, self.writers, [],0)
      if excepts or writeables or readables:
        for sock in readables:
           if sock in self.serversocks:
               CSA = self.createConnectedSocket(sock)
               # Here we send the message back to the protocol handler
               # We also want to send it to the selector.
               # This single messge breaks this
               # Solution: change signal - change is limited to SimplerServer
               # Let''s change that first
               self.send(newCSA(self, CSA), "protocolHandlerSignal")
               self.addChildren(CSA)
               self.link((CSA, "FactoryFeedback"),(self,"_csa_feedback"))
               return 1
           else:
               CSA = self.lookup[id(sock)]
               try:
                  CSA._deliver(status("data ready"),"DataReady")
               except:
                  t = time.time()
                  sock.close()
                  self.listeners.remove(sock)
                  del self.lookup[id(sock)]
      return status("ready")

if __name__ == '__main__':
   print "Simple integration test moved out to InternetHandlingTests.py"
