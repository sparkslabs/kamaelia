# ConnectedSocketAdapter Component Class
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
the "inbox" outbox.

The CSA expects to be wired to a component that will notify it when new data
has arrived at its socket (by sending an Axon.Ipc.status message to its
"ReadReady" inbox. This is to allow the CSA to sleep rather than busy-wait or
blocking when waiting for new data to arrive. Typically this is the Selector
component.

This component will terminate (and close its socket) if it receives a
producerFinished message on its "control" inbox.

When this component terminates, it sends a socketShutdown(socket) message out of
its "CreatorFeedback" outbox and a shutdownCSA((selfCSA,self.socket)) message
out of its "signal" outbox.

The message sent to "CreatorFeedback" is to notify the original creator that
the socket is now closed and that this component should be unwired.

The message sent to the "signal" outbox serves to notify any other component
involved - such as the one feeding notifications to the "ReadReady" inbox (eg.
the Selector component).
"""


import socket, time
import errno

import Axon
from Axon.Component import component
from Axon.Ipc import wouldblock, status, producerFinished, shutdownMicroprocess
from Kamaelia.IPC import socketShutdown,newCSA,shutdownCSA
from Kamaelia.IPC import removeReader, removeWriter
from Kamaelia.IPC import newReader, newWriter, removeReader, removeWriter

from Kamaelia.KamaeliaExceptions import *
import traceback
import pprint

whinge = { "socketSendingFailure": True, "socketRecievingFailure": True }
crashAndBurn = { "uncheckedSocketShutdown" : True,
                            "receivingDataFailed" : True,
                            "sendingDataFailed" : True }

class SSLSocket(object):
   def __init__(self, sock):
      self.sslobj = socket.ssl(sock)
      # we keep a handle to the real socket 
      # so that we can perform some operations on it
      self.sock = sock
      
   def fileno(self):
      return self.sock.fileno()
   
   def setblocking(self, state):
      self.sock.setblocking(state)
      
   def recv(self, size=1024):
      try:
         return self.sslobj.read(size)
      except socket.sslerror, e:
         # We allow those errors to go through
         if e.args[0] not in [socket.SSL_ERROR_WANT_READ, 
                              socket.SSL_ERROR_WANT_WRITE]:
            raise
         return ''

   def send(self, data):
      try:
         return self.sslobj.write(data)
      except socket.sslerror, e:
         # We allow those errors to go through
         if e.args[0] not in [socket.SSL_ERROR_WANT_READ, 
                              socket.SSL_ERROR_WANT_WRITE]:
            raise
         return 0


class ConnectedSocketAdapter(component):
   """\
   ConnectedSocketAdapter(socket) -> new CSA component wrapping specified socket

   Component for communicating with a socket. Send to its "inbox" inbox to
   send data, and receive data from its "outbox" outbox.

   "ReadReady" inbox must be wired to something that will notify it when new
   data has arrived at the socket.
   """
       
   Inboxes  = { "inbox"   : "Data for this CSA to send through the socket (Axon.Ipc.status message)",
                "control"    : "Shutdown on producerFinished message (incoming & outgoing data is flushed first)",
                "ReadReady"  : "Notify this CSA that there is incoming data ready on the socket",
                "SendReady" : "Notify this CSA that the socket is ready to send",
                "makessl": "Notify this CSA that the socket should be wrapped into SSL",
              }
   Outboxes = { "outbox"          : "Data received from the socket",
                "CreatorFeedback" : "Expected to be connected to some form of signal input on the CSA's creator. Signals socketShutdown (this socket has closed)",
                "signal"          : "Signals shutdownCSA (this CSA is shutting down)",
                "_selectorSignal" : "For communication to the selector",
                "sslready": "Notifies components that the socket is now wrapped into SSL",
              }

   def __init__(self, listensocket, selectorService, crashOnBadDataToSend=False, noisyErrors = True):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(ConnectedSocketAdapter, self).__init__()
      self.socket = listensocket
      self.data_to_send = ""
      self.crashOnBadDataToSend = crashOnBadDataToSend
      self.noisyErrors = noisyErrors
      self.selectorService = selectorService
      self.howDied = False
      self.isSSL = False
      self.couldnt_send = None
   
   def handleControl(self):
      """Check for producerFinished message and shutdown in response"""
      if self.dataReady("control"):
          data = self.recv("control")
          if isinstance(data, producerFinished):
#              print "Raising shutdown: ConnectedSocketAdapter recieved producerFinished Message", self,data
              self.connectionRECVLive = False
              self.connectionSENDLive = False
              self.howDied = "producer finished"
          elif isinstance(data, shutdownMicroprocess):
#              print "Raising shutdown: ConnectedSocketAdapter recieved shutdownMicroprocess Message", self,data
              self.connectionRECVLive = False
              self.connectionSENDLive = False
              self.howDied = "shutdown microprocess"
          else:
              pass # unrecognised message
   

   def passOnShutdown(self):
        self.send(socketShutdown(self,[self.socket,self.howDied]), "CreatorFeedback")
        self.send(shutdownCSA(self, (self,self.socket)), "signal")

   def finalize(self):
       # Some of these are going to crash initially when stop is called
#       print "I AM CALLED"
       self.socket.shutdown(2)
       self.socket.close()
       self.passOnShutdown()
       if (self.socket is not None):
           self.send(removeReader(self, self.socket), "_selectorSignal")
           self.send(removeWriter(self, self.socket), "_selectorSignal")

   def _safesend(self, sock, data):
       """Internal only function, used for sending data, and handling EAGAIN style
       retry scenarios gracefully"""
       bytes_sent = 0
       try:
          bytes_sent = sock.send(data)
          return bytes_sent

       except socket.error, socket.msg:
          (errorno, errmsg) = socket.msg.args
          if not (errorno == errno.EAGAIN or  errorno == errno.EWOULDBLOCK):
             self.connectionSENDLive = False
             self.howDied = socket.msg

       except TypeError, ex:

          if self.noisyErrors:
             print "CSA: Exception sending on socket: ", ex, "(no automatic conversion to string occurs)."
          if self.crashOnBadDataToSend:
              raise ex
       self.sending = False
       if self.connectionSENDLive:
           self.send(newWriter(self, ((self, "SendReady"), sock)), "_selectorSignal")
       return bytes_sent
   
   def flushSendQueue(self):
       while ( len(self.data_to_send) != 0 ) or self.dataReady("inbox") :
           if len(self.data_to_send) == 0:
               # Can't get here unless self.dataReady("inbox")
               self.data_to_send = self.recv("inbox")
           bytes_sent = self._safesend(self.socket, self.data_to_send)
           self.data_to_send = self.data_to_send[bytes_sent:]
           if bytes_sent == 0:
               break # failed to send right now, resend later

   def _saferecv(self, sock, size=32768):
       """Internal only function, used for recieving data, and handling EAGAIN style
       retry scenarios gracefully"""
       try:
          data = sock.recv(size)
          if data:
              self.failcount = 0
              return data
          # In case of a SSL object we may read no data although
          # the connection per se is still up
          # We therefore don't treat such possibility as an error
          elif not self.isSSL: # This implies the connection has closed for some reason
                 self.connectionRECVLive = False

       except socket.error, socket.msg:
          (errorno, errmsg) = socket.msg.args
          if not (errorno == errno.EAGAIN or errorno == errno.EWOULDBLOCK):
              # "Recieving an error other than EAGAIN or EWOULDBLOCK when reading is a genuine error we don't handle"
              self.connectionRECVLive = False
              self.howDied = socket.msg
       self.receiving = False
       if self.connectionRECVLive:
           self.send(newReader(self, ((self, "ReadReady"), sock)), "_selectorSignal")
       return None  # Explicit rather than implicit.

   def handleReceive(self):
       successful = True
       while successful and self.connectionRECVLive: ### Fixme - probably want maximum iterations here
         if self.couldnt_send is not None:
             try:
                 self.send(self.couldnt_send, "outbox")
                 self.couldnt_send = None
             except Axon.AxonExceptions.noSpaceInBox:
                 return

         socketdata = self._saferecv(self.socket, 32768) ### Receiving may die horribly         
         if (socketdata):
             try:
                 self.send(socketdata, "outbox")
             except Axon.AxonExceptions.noSpaceInBox:
                 self.couldnt_send = socketdata
                 successful = False
             else:
                 successful = True
         else:
             successful = False

   def checkSocketStatus(self):
       if self.dataReady("ReadReady"):
           self.receiving = True
           self.recv("ReadReady")

       if self.dataReady("SendReady"):
           self.sending = True
           self.recv("SendReady")

   def canDoSomething(self):
       if self.sending and ( (len(self.data_to_send) > 0) or self.dataReady("inbox") ):
           return True
       if self.receiving:
           return True
       if self.anyReady():
           return True
       return False

   def main(self):
#       print "self.selectorService", self, self.selectorService
       self.link((self, "_selectorSignal"), self.selectorService)
       # self.selectorService ...
       self.sending = True
       self.receiving = True
       self.connectionRECVLive = True
       self.connectionRECVLive = True
       self.connectionSENDLive = True
       while self.connectionRECVLive and self.connectionSENDLive: # Note, this means half close == close
          yield 1
          if self.dataReady("makessl"):
             self.recv('makessl')

             self.send(removeReader(self, self.socket), "_selectorSignal")
             self.send(removeWriter(self, self.socket), "_selectorSignal")

             # We need to block to allow the handshake to complete
             self.socket.setblocking(True)
             self.socket = SSLSocket(self.socket)
             self.isSSL = True
             self.socket.setblocking(False)

             self.send(newReader(self, ((self, "ReadReady"), self.socket)), "_selectorSignal")
             self.send(newWriter(self, ((self, "SendReady"), self.socket)), "_selectorSignal")

             self.send('', 'sslready')
             yield 1

          self.checkSocketStatus() # To be written
          self.handleControl()     # Check for producerFinished message in "control" and shutdown in response
          if self.sending:
              self.flushSendQueue()
          if self.receiving:
              self.handleReceive()
          if not self.canDoSomething():
              self.pause()
 
       self.passOnShutdown()
       # NOTE: the creator of this CSA is responsible for removing it from the selector

__kamaelia_components__  = ( ConnectedSocketAdapter, )
