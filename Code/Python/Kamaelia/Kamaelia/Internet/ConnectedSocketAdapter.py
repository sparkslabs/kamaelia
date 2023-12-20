# -*- coding: utf-8 -*-
# ConnectedSocketAdapter Component Class
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
producerFinished or shutdownMicroprocess message on its "control" inbox.

When this component terminates, it sends a socketShutdown(socket) message out of
its "CreatorFeedback" outbox and a shutdownCSA((selfCSA,self.socket)) message
out of its "signal" outbox.

The message sent to "CreatorFeedback" is to notify the original creator that
the socket is now closed and that this component should be unwired.

The message sent to the "signal" outbox serves to notify any other component
involved - such as the one feeding notifications to the "ReadReady" inbox (eg.
the Selector component).
"""

import sys
import socket, time
import errno

import Axon
from Axon.Component import component
from Axon.Ipc import wouldblock, status, producerFinished, shutdownMicroprocess
from Kamaelia.IPC import socketShutdown,newCSA,shutdownCSA
from Kamaelia.IPC import removeReader, removeWriter
from Kamaelia.IPC import newReader, newWriter, removeReader, removeWriter

# from Kamaelia.Apps.SocialBookmarks.Print import Print # For debug purposes

import traceback
import ssl

whinge = { "socketSendingFailure": True, "socketRecievingFailure": True }
crashAndBurn = { "uncheckedSocketShutdown" : True,
                            "receivingDataFailed" : True,
                            "sendingDataFailed" : True }

class SSLSocket(object):
   def __init__(self, sock):
#      self.sslobj = socket.ssl(sock)
      self.sslobj = ssl.wrap_socket(sock)
      # we keep a handle to the real socket 
      # so that we can perform some operations on it
      self.sock = sock
      
   def shutdown(self, code):
      self.sock.shutdown(code)

   def close(self):
      self.sock.close()

   def fileno(self):
      return self.sock.fileno()
   
   def setblocking(self, state):
      self.sock.setblocking(state)
      
   def recv(self, size=1024):
      try:
         return self.sslobj.read(size)
      except socket.sslerror:
         e = sys.exc_info()[1]
         # We allow those errors to go through
         if e.args[0] not in [socket.SSL_ERROR_WANT_READ, 
                              socket.SSL_ERROR_WANT_WRITE]:
            raise
         return ''

   def send(self, data):
      try:
         return self.sslobj.write(data)
      except socket.sslerror:
         e = sys.exc_info()[1]
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
#              print ("Raising shutdown: ConnectedSocketAdapter recieved producerFinished Message", self,data)
              self.connectionRECVLive = False
              self.connectionSENDLive = False
              self.howDied = "producer finished"
              # Print( "producerFinished")
          elif isinstance(data, shutdownMicroprocess):
#              print ("Raising shutdown: ConnectedSocketAdapter recieved shutdownMicroprocess Message", self,data)
              self.connectionRECVLive = False
              self.connectionSENDLive = False
              self.howDied = "shutdown microprocess"
              # Print( "shutdownMicroprocess")
          else:
              # Print( "Random control message")
              pass # unrecognised message
   

   def passOnShutdown(self):
        self.send(socketShutdown(self,[self.socket,self.howDied]), "CreatorFeedback")
        self.send(shutdownCSA(self, (self,self.socket)), "signal")

   def stop(self):
       # Some of these are going to crash initially when stop is called
#       print ("I AM CALLED")
       # Print( "stopping")
       if self.socket is None:
           # SELF.STOP CALLED TWICE - possible under limited circumstances (crashes primarily)
           # Only want to call once though, so exit here.
           # Print( "Oh, hold on")
           return
       try:
           self.socket.shutdown(2)
           # Print( "socket.shutdown succeeded")
       except Exception:
           e = sys.exc_info()[1]
           # Explicitly silencing this because it is possible (but rare) that
           # the socket was already shutdown due to an earlier error.
           # Print( "socket.shutdown failed for some reason", e)
           pass

       try:
           # Print( "socket.close ...")
           self.socket.close()
           # Print( "             ... succeeded")
       except Exception:
           e = sys.exc_info()[1]
           # Print( "             ... failed")
           # Explicitly silencing this because it is possible (but rare) that
           # the socket was already closed due to an earlier error.
           pass
       sock = self.socket
       self.socket = None

       self.passOnShutdown()
       if (sock is not None):
           self.send(removeReader(self, sock), "_selectorSignal")
           self.send(removeWriter(self, sock), "_selectorSignal")
       sock = None
       super(ConnectedSocketAdapter, self).stop()
       self.stop = lambda : None   # Make it rather hard to call us twice by mistake
       # Print( "Really pretty sure we're stopped")

#       import gc
#       import pprint
#       gc.collect()
#       print ("REFERRERS", len(gc.get_referrers(self)))
#       pprint.pprint([(type(x),x) for x in gc.get_referrers(self)])

   def _safesend(self, sock, data):
       """Internal only function, used for sending data, and handling EAGAIN style
       retry scenarios gracefully"""
       bytes_sent = 0
       try:
          bytes_sent = sock.send(data)
          return bytes_sent

       except socket.error:
          msg = sys.exc_info()[1]
          (errorno, errmsg) = msg.args
          if not (errorno == errno.EAGAIN or  errorno == errno.EWOULDBLOCK):
             self.connectionSENDLive = False
             self.howDied = sg
             # Print( "Oh No! Socket Died - sending!", e)

       except TypeError:
          ex = sys.exc_info()[1]

          if self.noisyErrors:
             print ("CSA: Exception sending on socket: ", ex, "(no automatic conversion to string occurs).")
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

       except socket.error:
          msg = sys.exc_info()[1]
          (errorno, errmsg) = msg.args
          if not (errorno == errno.EAGAIN or errorno == errno.EWOULDBLOCK):
              # "Recieving an error other than EAGAIN or EWOULDBLOCK when reading is a genuine error we don't handle"
              self.connectionRECVLive = False
              self.howDied = msg
              # Print( "Oh No! Socket Died - receiving!", e)
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
#       print ("self.selectorService", self, self.selectorService)
       self.link((self, "_selectorSignal"), self.selectorService)
       # self.selectorService ...
       self.sending = True
       self.receiving = True
       self.connectionRECVLive = True
       self.connectionRECVLive = True
       self.connectionSENDLive = True
       # Print( "CSA Activated")

       while self.connectionRECVLive and self.connectionSENDLive: # Note, this means half close == close
          yield 1
          if self.dataReady("makessl"):
#             print ("****************************************************** Making SSL ******************************************************")
             # Print( "CSA Made SSL")
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
#             print ("****************************************************** SSL IS READY ******************************************************")
             yield 1

          self.checkSocketStatus() # To be written
          self.handleControl()     # Check for producerFinished message in "control" and shutdown in response
          if self.sending:
              self.flushSendQueue()
          if self.receiving:
              self.handleReceive()
          if not self.canDoSomething():
              self.pause()
 
#       self.passOnShutdown()
       # Print( "Stopping...")
       self.stop()
       # NOTE: the creator of this CSA is responsible for removing it from the selector

#       print ("") 
#       print ("------------------------------------------------------------------------------------")
#       print ("DROPPED OFF THE END OF THE GENERATOR",self.socket)
       self.socket=None
#       print (self.__dict__)
#       print (self.postoffice)
#       print ([str(x) for x in self.postoffice.linkages])
       for linkage in self.postoffice.linkages:
           self.unlink(thelinkage=linkage)
#       print ("------------------------------------------------------------------------------------")

__kamaelia_components__  = ( ConnectedSocketAdapter, )
