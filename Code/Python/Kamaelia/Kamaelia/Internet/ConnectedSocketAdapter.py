# ConnectedSocketAdapter Component Class
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
==========================
Talking to network sockets
==========================

A Connected Socket Adapter (CSA) component talks to a network server socket.
Data is sent to and received from the socket via this component's inboxes and
outboxes. A CSA is effectively a wrapper for a socket.

Most components should not need to create CSAs themselves. Instead, use
components such as TCPClient to make an outgoing connection, or TCPServer or
SimpleServer to be a server that responds to incoming connections.



Example Usage
-------------
See source code for TCPClient to see how Connected Socket Adapters can be used.


See also
--------
- TCPClient     -- for making a connection to a server
- TCPServer     -- 
- SimpleServer  -- a prefab chassis for building a server


How does it work?
-----------------
A CSA is usually created either by a component such as TCPClient that wants to
establish a connection to a server; or by a primary listener socket - a
component acting as a server - listening for incoming connections from clients.

The socket should be set up and passed to the constructor to make the CSA.

Incoming data, read by the CSA, is sent out of its "outbox" outbox as strings
containing the received binary data. Send data by sending it, as strings, to
the "DataSend" outbox.

The CSA expects to be wired to a component that will notify it when new data
has arrived at its socket (by sending an Axon.Ipc.status message to its
"DataReady" inbox. This is to allow the CSA to sleep rather than busy-wait or
blocking when waiting for new data to arrive. Typically this is the Selector
component.

This component will terminate (and close its socket) if it receives a
producerFinished message on its "control" inbox.

When this component terminates, it sends a socketShutdown(socket) message out of
its "FactoryFeedback" outbox and a shutdownCSA((selfCSA,self.socket)) message
out of its "signal" outbox.

The message sent to "FactoryFeedback" is to notify the original creator that
the socket is now closed and that this component should be unwired.

The message sent to the "signal" outbox serves to notify any other component
involved - such as the one feeding notifications to the "DataReady" inbox (eg.
the Selector component).
"""


import socket, time
import errno

import Axon
from Axon.Component import component
from Axon.Ipc import wouldblock, status, producerFinished
from Kamaelia.KamaeliaIPC import socketShutdown,newCSA,shutdownCSA
from Kamaelia.KamaeliaExceptions import *
import traceback

whinge = { "socketSendingFailure": True, "socketRecievingFailure": True }
crashAndBurn = { "uncheckedSocketShutdown" : True,
                            "receivingDataFailed" : True,
                            "sendingDataFailed" : True }

def _safesend(sock, data,selffile = None):
   """Internal only function, used for sending data, and handling EAGAIN style
   retry scenarios gracefully"""
   try:
      bytes_sent = sock.send(data)
      return bytes_sent
   except socket.error, socket.msg:
      (errorno, errmsg) = socket.msg.args
      if not (errorno == errno.EAGAIN or  errorno == errno.EWOULDBLOCK):
         raise socket.msg        # then rethrow the error.
      return 0                                                                        # Otherwise return 0 for failure on sending
   except exceptions.TypeError, ex:
      if whinge["socketSendingFailure"]:
         print "CSA: Exception sending on socket: ", ex, "(no automatic conversion to string occurs)."
      raise ex

def _saferecv(sock, size=1024):
   """Internal only function, used for recieving data, and handling EAGAIN style
   retry scenarios gracefully"""
   data = None;
   try:
      data = sock.recv(size)
      if not data: # This implies the connection has barfed.
         raise connectionDiedReceiving(sock,size)
   except socket.error, socket.msg:
      (errorno, errmsg) = socket.msg.args
      if not (errorno == errno.EAGAIN or errorno == errno.EWOULDBLOCK):
         #"Recieving an error other than EAGAIN or EWOULDBLOCK when reading is a genuine error we don't handle"
         raise socket.msg # rethrow
   return data

class ConnectedSocketAdapter(component):
   """\
   ConnectedSocketAdapter(socket) -> new CSA component wrapping specified socket

   Component for communicating with a socket. Send to its "DataSend" inbox to
   send data, and receive data from its "outbox" outbox.

   "DataReady" inbox must be wired to something that will notify it when new
   data has arrived at the socket.
   """
       
   Inboxes  = { "DataReady"  : "Notify this CSA that there is incoming data ready on the socket",
                "DataSend"   : "Data for this CSA to send through the socket (Axon.Ipc.status message)",
                "Initialise" : "NOT USED",
                "control"    : "Shutdown on producerFinished message (incoming & outgoing data is flushed first)",
              }
   Outboxes = { "outbox"          : "Data received from the socket",
                "FactoryFeedback" : "Signals socketShutdown (this socket has closed)",
                "signal"          : "Signals shutdownCSA (this CSA is shutting down)",
              }

   def __init__(self, listensocket):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(ConnectedSocketAdapter, self).__init__()
      self.time = time.time()
      self.socket = listensocket
      self.resend_queue = []
      self.file = None

   def handleDataReady(self):
      """Handle situation when has been notified that there is data waiting to be read from the socket."""
      if self.dataReady("DataReady"):
         data = self.recv("DataReady")
         if (isinstance(data, status)):
            socketdata = None
            try:
               socketdata = _saferecv(self.socket, 1024) ### Receiving may die horribly
            except connectionDiedReceiving, cd:
               raise cd # rethrow
            except Exception, e: # Unexpected error that might cause crash. Do we want to really crash & burn?
               if crashAndBurn["receivingDataFailed"]:
                  raise e
            if (socketdata):
               self.send(socketdata, "outbox")

   def handleDataSend(self):
       """Check for and send data to the socket"""
       try:
          if self.dataReady("DataSend"):
             data = self.recv("DataSend")
             self.resend_queue.append(data)
          if len(self.resend_queue)>0:
             data = self.resend_queue[0]
             try:
                bytes_sent = _safesend(self.socket, data, self.file) ### Sending may fail....
                if bytes_sent:
                    if bytes_sent == len(data):
                        del self.resend_queue[0]
                    else:
                        self.resend_queue[0] = data[bytes_sent:]
             except Exception, e: # If it does, and we get an exception the connection is unstable or closed
                if crashAndBurn["sendingDataFailed"]:
                   raise connectionDiedReceiving(e)
                raise connectionClosedown(e)
          return 1        # Since we got here, client is still around, so return true.
       except:
          print "TRACEBACK INSIDE CONNECTED SOCKET ADAPTOR"
          traceback.print_exc()

   def handleControl(self):
      """Check for producerFinished message and shutdown in response"""
      #if self is Axon.Foo:
      #      print "CSA: CONTROL", self.dataReady("control"),
      #      print "CSA: DATASEND", self.dataReady("DataSend"),
      #      print "CSA: DATAREADY", self.dataReady("DataReady")
      #if not (self.dataReady("DataSend") or self.dataReady("DataReady")):
      if self.dataReady("control"):
          data = self.recv("control")
          if isinstance(data, producerFinished):
              #print "Raising shutdown: ConnectedSocketAdapter recieved producerFinished Message", self,data
              raise connectionServerShutdown()

   def mainBody(self):
      """Main loop."""
      self.pause()
      try:
         self.handleDataReady()
         self.handleDataSend()
         self.handleControl()
         return wouldblock(self)
      except connectionDied, cd: # Client went away or socket error
         self.send(socketShutdown(self,self.socket), "FactoryFeedback")
#         self.send(socketShutdown(self), "signal")
         self.send(shutdownCSA(self, (self,self.socket)), "signal")
         return 0
      except connectionServerShutdown, cd: # Client went away or socket error
         self.send(socketShutdown(self,self.socket), "FactoryFeedback")
#         self.send(socketShutdown(self), "signal")
         self.send(shutdownCSA(self, (self,self.socket)), "signal")
         return 0
      except Exception, ex: # Some other exception
         self.send(socketShutdown(self,self.socket), "FactoryFeedback")
#         self.send(socketShutdown(self), "signal")
         self.send(shutdownCSA(self, (self,self.socket)), "signal")
         if crashAndBurn["uncheckedSocketShutdown"]:
            raise ex
         return 0

__kamaelia_components__  = ( ConnectedSocketAdapter, )
