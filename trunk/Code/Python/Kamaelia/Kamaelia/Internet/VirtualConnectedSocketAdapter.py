# VirtualConnectedSocketAdapter Component Class
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
# Logically derived from ConnectedSocketAdapter
#

import socket
import time
import errno
from Axon.Component import component
import Axon
from Axon.Ipc import wouldblock, status, producerFinished
from Kamaelia.KamaeliaIPC import socketShutdown,newCSA
from Kamaelia.KamaeliaExceptions import *

whinge = { "socketSendingFailure": True, "socketRecievingFailure": True }
crashAndBurn = { "uncheckedSocketShutdown" : True,
                            "receivingDataFailed" : True,
                            "sendingDataFailed" : True }

def _safesend(sock, data,addr):
   """Internal only function, used for sending data, and handling EAGAIN style
   retry scenarios gracefully"""
   try:
      sock.sendto(data,addr)
      print "DID WE GET HERE????",
      return 1
   except socket.error, socket.msg:
      print "WE >>>>DID<<<<GET HERE", socket.msg
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
         "Recieving an error other than EAGAIN or EWOULDBLOCK when reading is a genuine error we don't handle"
         raise socket.msg # rethrow
   return data

class VirtualConnectedSocketAdapter(component):
   Inboxes=["DataReady", "DataSend", "Initialise", "control"]
   Outboxes=["outbox", "FactoryFeedback","signal"]

   def __init__(self, listensocket,addr):
      self.__super.__init__()
      self.time = time.time()
      self.socket = listensocket
      self.remoteaddr = addr

   def handleDataReady(self):
      if self.dataReady("DataReady"):
         data = self.recv("DataReady")
         if (isinstance(data, status)):
            socketdata = None
            try:
               socketdata = _saferecv(self.socket, 1024) ### Receiving may die horribly
               if socketdata is not None:
                  print "SOCKETDATA", socketdata
            except connectionDiedReceiving, cd:
               raise cd # rethrow
            except Exception, e: # Unexpected error that might cause crash. Do we want to really crash & burn?
               if crashAndBurn["receivingDataFailed"]:
                  raise e
            if (socketdata):
               self.send(socketdata, "outbox")

   def handleDataSend(self):
      if self.dataReady("DataSend"):
         data = self.recv("DataSend")
         try:
            result = _safesend(self.socket, data, self.remoteaddr) ### Sending may fail....
            # XXXX SMELL What about partial sends?
         except Exception, e: # If it does, and we get an exception the connection is unstable or closed
            if crashAndBurn["sendingDataFailed"]:
               raise connectionDiedReceiving(e)
            raise connectionClosedown(e)
      return 1        # Since we got here, client is still around, so return true.

   def handleControl(self):
         if self.dataReady("control"):
            print "CSA: Control Has a message!"
            data = self.recv("control")
            if isinstance(data, producerFinished):
               #print "Raising shutdown: VirtualConnectedSocketAdapter recieved producerFinished Message", self,data
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
         self.send(socketShutdown(self), "signal")
         return 0
      except connectionServerShutdown, cd: # Client went away or socket error
         self.send(socketShutdown(self,self.socket), "FactoryFeedback")
         self.send(socketShutdown(self), "signal")
         return 0
      except Exception, ex: # Some other exception
         self.send(socketShutdown(self,self.socket), "FactoryFeedback")
         self.send(socketShutdown(self), "signal")
         if crashAndBurn["uncheckedSocketShutdown"]:
            raise ex
         return 0
