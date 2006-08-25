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
"""\
=================
TCP Socket Server
=================

A building block for creating a TCP based network server. It accepts incoming
connection requests and sets up a component to handle the socket which it then
passes on.

This component does not handle the instantiation of components to handle an
accepted connection request. Another component is needed that responds to this
component and actually does something with the newly established connection.
If you require a more complete implementation that does this, see
Kamaelia.Internet.SingleServer or Kamaelia.Chassis.ConnectedServer.



Example Usage
-------------

See Kamaelia.Internet.SingleServer or Kamaelia.Chassis.ConnectedServer for examples of how
this component can be used.

The process of using a TCPServer component can be summarised as:
- Create a TCP Server
- Wait for newCSA messages from the TCP Server's "protocolHandlerSignal" outbox
- Send what you like to CSA's, ensure you recieve data from the CSAs
- Send producerFinished to the CSA to shut it down.


How does it work?
-----------------

This component creates a listener socket, bound to the specified port, and
registers itself and the socket with a selectorComponent so it is notified of
incoming connections. The selectorComponent is obtained by calling
selectorComponent.getSelectorService(...) to look it up with the local
Coordinating Assistant Tracker (CAT).

When the it recieves a new connection it performs an accept, and creates
a ConnectedSocketAdapter (CSA) to handle the activity on that connection.

The CSA is passed in a newCSA(self,CSA) message to TCPServer's
"protocolHandlerSignal" outbox.

The CSA is also registered with the selector service by sending it a
newCSA(self,(CSA,sock)) message, to ensure the CSA is notified of incoming data
on its socket.

The client component(s) using the TCPServer should handle the newly created CSA
passed to it in whatever way it sees fit.

If a socketShutdown message is received on the "_feedbackFromCSA" inbox, then a
shutdownCSA(self, CSA) message is sent to TCPServer's "protocolHandlerSignal"
outbox to notify the client component that the connection has closed.

Also, a shutdownCSA(self, (CSA, sock)) message is sent to the selector service
to deregister the CSA from receiving notifications.

This component does not terminate.
"""

import socket, errno, random, Axon
import Kamaelia.KamaeliaIPC as _ki
from Kamaelia.Internet.ConnectedSocketAdapter import ConnectedSocketAdapter

import time
from Kamaelia.Internet.Selector import Selector

from Kamaelia.KamaeliaIPC import newReader, newWriter
from Kamaelia.KamaeliaIPC import removeReader, removeWriter


class TCPServer(Axon.Component.component):
   """\
   TCPServer(listenport) -> TCPServer component listening on the specified port.

   Creates a TCPServer component that accepts all connection requests on the
   specified port.
   """
   
   Inboxes  = { "DataReady"     : "status('data ready') messages indicating new connection waiting to be accepted",
                "_feedbackFromCSA" : "for feedback from ConnectedSocketAdapter (shutdown messages)",
                "newconnection" : "We expected to recieve a message here when a new connection is ready",
              }
   Outboxes = { "protocolHandlerSignal" : "For passing on newly created ConnectedSocketAdapter components",
                "signal"                : "NOT USED",
                "_selectorSignal"       : "For registering newly created ConnectedSocketAdapter components with a selector service",
              }

   def __init__(self,listenport, socketOptions=None):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(TCPServer, self).__init__()
      self.listenport = listenport
      self.socketOptions = socketOptions
      self.listener,junk = self.makeTCPServerPort(listenport, maxlisten=5)

   def makeTCPServerPort(self, suppliedport=None, HOST=None, minrange=2000,maxrange=50000, maxlisten=5):
      """\
      Returns (socket,port) - a bound TCP listener socket and the port number it is listening on.

      If suppliedPort is not specified, then a random port is chosen between
      minrange and maxrange inclusive.

      maxlisten is the max number of pending requests the server will allow (queue up).
      """
      if HOST is None: HOST=''
      if suppliedport is None:
         PORT=random.randint(minrange,maxrange) # Built in support for testing
      else:
         PORT=suppliedport

      s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      if self.socketOptions is not None:
          s.setsockopt(*self.socketOptions)
      s.setblocking(0)
      assert self.debugger.note("PrimaryListenSocket.makeTCPServerPort", 5, "HOST,PORT",":",HOST,":",PORT,":")
      s.bind((HOST,PORT))
      s.listen(maxlisten)
      return s,PORT

   def createConnectedSocket(self, sock):
      """\
      Accepts the connection request on the specified socket and returns a
      ConnectedSocketAdapter component for it.
      """
      tries = 0
      maxretries = 10
      gotsock=False
      newsock, addr = sock.accept()  # <===== THIS IS THE PROBLEM
      self.send(newReader(self, ((self, "newconnection"), self.listener)), "_selectorSignal")

      gotsock = True
      newsock.setblocking(0)
###      
      CSA = ConnectedSocketAdapter(newsock,self.selectorService)
      return newsock, CSA

   def closeSocket(self, shutdownMessage):
      """\
      Respond to a socketShutdown message by closing the socket.

      Sends a removeReader and removeWriter message to the selectorComponent.
      Sends a shutdownCSA(self, theCSA) message to "protocolHandlerSignal" outbox.
      """
      theComponent,sock = shutdownMessage.caller, shutdownMessage.message
      sock.close()
      
      # tell the selector about it shutting down
      
      self.send(removeReader(theComponent, theComponent.socket), "_selectorSignal")            
      self.send(removeWriter(theComponent, theComponent.socket), "_selectorSignal")

      # tell protocol handlers
      self.send(_ki.shutdownCSA(self, theComponent), "protocolHandlerSignal")# "signal")
      # Delete the child component
      self.removeChild(theComponent)

   def anyClosedSockets(self):
      """Check "_feedbackFromCSA" inbox for socketShutdown messages, and close sockets in response."""
      closedSomeSockets=False
      while self.dataReady("_feedbackFromCSA"):
         data = self.recv("_feedbackFromCSA")
         if isinstance( data, _ki.socketShutdown):
            self.closeSocket(data)
         closedSomeSockets=True
      return closedSomeSockets

   def handleNewConnection(self):
      """\
      Handle notifications from the selector service of new connection requests.

      Accepts and sets up new connections, wiring them up and passing them on via
      the "protocolHandlerSignal" outbox.
      """
      while self.dataReady("newconnection"):
         data = self.recv("newconnection")
         # If we recieve information on data ready, for a server it means we have a new connection
         # to handle
         try:
            newsock, CSA = self.createConnectedSocket(self.listener)
         except socket.error, e:
            (errorno,errmsg) = e
            if errorno != errno.EAGAIN:
               if errorno != errno.EWOULDBLOCK:
                  raise e
         else:
             pass

             self.send(_ki.newCSA(self, CSA), "protocolHandlerSignal")
             self.send(newReader(CSA, ((CSA, "ReadReady"), newsock)), "_selectorSignal")            
             self.send(newWriter(CSA, ((CSA, "SendReady"), newsock)), "_selectorSignal")            
             self.addChildren(CSA)
             self.link((CSA, "CreatorFeedback"),(self,"_feedbackFromCSA"))
#             return CSA

   def main(self):
       selectorService, selectorShutdownService, newSelector = Selector.getSelectorServices(self.tracker)
       if newSelector:
           newSelector.activate()
       self.link((self, "_selectorSignal"),selectorService)
       self.selectorService = selectorService
       self.send(newReader(self, ((self, "newconnection"), self.listener)), "_selectorSignal")
       yield 1
       while 1:
           self.pause()
           if self.anyClosedSockets():
               for i in xrange(10):
                  yield 1
           self.handleNewConnection() # Data ready means that we have a connection waiting.
           yield 1

__kamaelia_components__  = ( TCPServer, )

if __name__ == '__main__':
   print "Simple integration test moved out to InternetHandlingTests.py"
