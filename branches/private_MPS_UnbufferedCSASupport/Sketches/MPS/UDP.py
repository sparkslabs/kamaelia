#!/usr/bin/python
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
"""
Simple UDP server and client code. May as well prototype the way we intend
the system to be used - design a single threaded approach first, and then
turn into components :)

Currently this only supports unidirectional clients, doesn't support
componentisation, etc.
"""

import socket
import select
import time

#
# Simple socket adapter helper
#
# Slight differences to CSA, can probably merge
#

def save_recv(sock, buf):
    data = None
    notRead=True
    while notRead:
       notRead=False # Assume success
       try:
          data,addr = sock.recvfrom(buf)
       except socket.error, e:
           notRead=True # We failed to read
           if e[0]!=11:
              break
    return data, addr

#
# Stub client protocol
#

def clientProtocol(delay=0.3):
    things_to_send = ["hello", "world",  "How",  "about", "that"]
    for i in things_to_send:
       yield i
       time.sleep(0.3)

#
# Stub server protocol
#
def serverProtocol(delay=0.3):
   while 1:
      yield "ACKNOWLEDGED"
      
#
# Local Exception for exitting main execution loop
#

class ExitMainLoop(Exception): pass

class UDPPeer:
   """Base class for UDP clients and servers, this would be the basic
      UDPClient class - probably a sensible as UDPComponent"""
   def __init__(self,host = "localhost", port = 1701, buf = 1024):
      self.host=host
      self.port=port
      self.buf=buf
      self.quitting=0

   def run(self):
      addr = (self.host,self.port)
      self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
      self.sock.setblocking(0)
      self.setup()
      IP,port= self.sock.getsockname()
      print "STARTING PEER"
      client = clientProtocol()
      conntrack = {}
      dataToSend = []
      while (1): # This mainloop, we need to check
         is_writeable = [self.sock]
         is_readable = [self.sock]
         is_error = []
         r,w,e = select.select(is_readable, is_writeable, is_error,0.0)
         if r:
            data, addr = save_recv(self.sock, self.buf)
            try:
               self.handleRecieveData(data, addr, conntrack, dataToSend)
            except ExitMainLoop:
               break
            data = None
         if w:
            self.handleSendData(addr, client, dataToSend)

         if self.quitting==1:
            time.sleep(0.4) # Allow response to arrive
         elif self.quitting==2:
            break

      self.shutdown(addr)
      self.sock.close()

   def setup(self):
      self.sock.bind(("",0))

   def shutdown(self,addr):
      print "HMM", self.sock.sendto('',addr)

   def handleRecieveData(self, data, addr, conntrack, dataToSend):
      print "CLIENT RECEIVED RESPONSE!", data, addr

   def handleSendData(self, addr, client, dataToSend):
      try:
         data = client.next()
         if(self.sock.sendto(data,addr)):
            print "CLIENT Sending message '",data,"'.....<done>"
      except StopIteration:
         self.quitting +=1 # First time will indicate we've sent data.
                           # Pause added below using this will allow
                           # 0.4s for the last response to arrive

#
# Possibly the most basic form of connection tracking:
#    * Simply maps client address to protocol handler
#    * As a result the ownership or creating handlers resides here
#      which simpliies the interface, but _possibly_ isn't _quite_
#      right.
#    * No conception of timeouts/etc
#

class ConnTrack:
   """Basic connection tracking - mapping addresses to protocol handlers"""
   def __init__(self, handlerGen):
      self.handlerGen=handlerGen
      self.conntrack = {}
   def clientShutdown(self, addr):
      print "Client has exited!"
      try:
         del self.conntrack[addr]
      except KeyError, e:
         # Server Shutdown message? 
         # (This sucks, don't use in production code)
         raise e
   def retrieveProtocolHandler(self,addr):
      try:
         protocol = self.conntrack[addr]
      except KeyError:
        protocol = self.handlerGen()
        self.conntrack[addr] = protocol
      return protocol

#
# Overrides the basic functionality of the UDPPeer to provide support for
# lossy connection oriented behaviour.
# No conception of timeouts/etc as yet.
#

class UDPServer(UDPPeer):

   def setup(self):
      self.sock.bind((self.host,self.port))
      self.ConnTrack= ConnTrack(serverProtocol)

   def shutdown(self,addr):
      pass

   def handleRecieveData(self, data, addr, conntrack, dataToSend):
      print "SERVER RECEIVED REQUEST!", data, addr
      if not data:
         try:
            self.ConnTrack.clientShutdown(addr)
         except KeyError:
            raise ExitMainLoop
      else:
         protocol = self.ConnTrack.retrieveProtocolHandler(addr)
         response = protocol.next()
         dataToSend.append((response+data,addr))
      print conntrack

   def handleSendData(self, addr, client, dataToSend):
      if dataToSend:
         (data,addr) = dataToSend[0]
         del dataToSend[0]
         if(self.sock.sendto(data,addr)):
            print "SERVER Sending message '",data,"'.....<done>"

#
# Basic factory function - decouple specific classes from the clients.
#

def mkUDPPeer(peertype="client",**args):
   if peertype=="server":
      return UDPServer(**args)
   return UDPPeer(**args)


def _standalone_usage():
   print "incorrect usage, sorry"
   print "Also, this isn't designed to be very useful!"

def main(argv,sys):
   if not argv[1:]:
      _standalone_usage()
      sys.exit(0)

   k = mkUDPPeer(peertype=argv[1])
   k.run()
   print

if __name__ == '__main__':
   import sys  
   main(sys.argv, sys)
