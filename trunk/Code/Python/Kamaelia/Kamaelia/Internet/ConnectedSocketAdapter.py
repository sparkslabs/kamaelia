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
#
# A connected socket adapter (CSA) component acts as a wrapper
# between a network server socket which has a connected client,
# and the component framework. It deals with new data arriving
# on the socket, and packetises it into messages available in its
# outbox, and taking messages from it's inbox "DataReady", and
# sending the data verbatim out the network socket.
#
# A component does not directly create a CSA, but rather it gets
# passed to a component from a Primary Listener Socket component,
# when a new connection is recieved on the server socket.
# A CSA presents its user with the following external connectors:
#    * inboxes=DataReady, DataSend, Initialise, control
#       * DataReady - this is a private connector, which tells the
#         component to read from the socket. It is used by the PLS
#         that created this component to tell the CSA that there is
#         data ready for reading from the socket.
#       * DataSend - a user of this component would expect to connect
#         a linkage to this inbox - since this is the inbox whereby recieved
#         data is sent to the client as soon as possible.
#       * Initialise - not actually used for anything, candidate for removal.
#       * control - standard control inbox, the socket will close connection
#         when there is nothing left in its DataSend and DataReady boxes if it is
#         sent a Axon.Ipc.producerFinished ipc object.
#    * outboxes=outbox, FactoryFeedback, signal
#       * outbox - Any data recieved from the socket will be made available
#         on this outbox.
#       * FactoryFeedback - In order to signal to the Primary Listener that the socket
#         has died, this outbox is made available for signalling purposes.
#       * signal - This performs a similar function, but is intended for use by
#         the client of the CSA - ie what ever is actually expecting data from the
#         CSA. You should check the signal for a message of the form:
#         {'shutdownCSA': CSA} periodically to check whether the client
#         has disappeared or not!
#
#    Other than the external interface, this component has no user servicable
#    parts.
#

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
   Inboxes=["DataReady", "DataSend", "Initialise", "control"]
   Outboxes=["outbox", "FactoryFeedback","signal"]

   def __init__(self, listensocket):
      super(ConnectedSocketAdapter, self).__init__()
      self.time = time.time()
      self.socket = listensocket
      self.resend_queue = []
      self.file = None

   def handleDataReady(self):
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
