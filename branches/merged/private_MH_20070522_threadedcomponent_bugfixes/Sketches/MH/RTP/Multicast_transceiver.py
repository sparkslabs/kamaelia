#!/usr/bin/env python
#
# FIXME: Uses the selector service, but has no way of indicating to the
#        selector service that its services are no longer required.
#        This needs resolving.
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
============================
Simple multicast transceiver
============================

A simple component for transmitting and receiving multicast packets.

Remember that multicast is an unreliable connection - packets may be lost,
duplicated or reordered.



Example Usage
-------------

Send a file to, and receive data from multicast group address 1.2.3.4 on
port 1000 with no guarantees of reliability, integrity or packet ordering::

    Pipeline( RateControlledFileReader("myfile", rate=100000),
              Multicast_transceiver("0.0.0.0", 0, "1.2.3.4", 1000),
            ).activate()

    Pipeline( Multicast_transceiver("0.0.0.0", 1000, "1.2.3.4", 0)
              ConsoleEchoer()
            ).activate()

Or::
    
    Pipeline( RateControlledFileReader("myfile", rate=100000),
              Multicast_transceiver("0.0.0.0", 1000, "1.2.3.4", 1000),
              ConsoleEchoer()
            ).activate()

The data emitted by Multicast_transciever (and displayed by ConsoleEchoer) is of
the form (source_address, data).



Behaviour
---------

Data sent to the component's "inbox" inbox is sent to the multicast group.

Data received from the multicast group is emitted as a tuple:
(source_addr, data) where data is a string of the received data.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to its "control" inbox. This message is forwarded onto the CSA.
Multicast_transceiver will then wait for the CSA to terminate. It then sends its
own shutdownMicroprocess message out of the "signal" outbox.

Multicast groups do not 'shut down', so this component will not usually emit any
signals on its "signal" outbox. However if, for some reason, there is a socket
error, a shutdownMicroprocess message will be sent out the "signal" outbox and
this component will then immediately terminate.



Why a transciever component?
----------------------------

Listens for packets in the given multicast group. Any data received is
sent to the receiver's outbox. The logic here is likely to be not quite
ideal. When complete though, this will be preferable over the sender and
receiver components since it models what multicast really is rather than
what people tend to think it is.




How does it work?
-----------------

Multicast_transceiver opens a socket connection to the specified server on the
specified port. Data received over the connection appears at the component's
"outbox" outbox as strings. Data can be sent as strings by sending it to the
"inbox" inbox.

An optional delay (between component activation and attempting to connect) can
be specified. The default is no delay.

It creates a ConnectedSocketAdapter (CSA) to handle the socket connection and
registers it with a selectorComponent so it is notified of incoming data. The
selectorComponent is obtained by calling
selectorComponent.getSelectorService(...) to look it up with the local
Coordinating Assistant Tracker (CAT).

Multicast_transceiver wires itself to the "CreatorFeedback" outbox of the CSA.
It also wires its "inbox" inbox to pass data straight through to the CSA's
"inbox" inbox, and its "outbox" outbox to pass through data from the CSA's
"outbox" outbox.

Socket errors (after the connection has been successfully established) may be
sent to the "signal" outbox.

This component will terminate if the CSA sends a socketShutdown message to its
"CreatorFeedback" outbox.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to its "control" inbox. This message is forwarded onto the CSA.
Multicast_transceiver will then wait for the CSA to terminate. It then sends its
own shutdownMicroprocess message out of the "signal" outbox.
"""

import socket
import errno

import Axon
from Axon.util import Finality

from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.Ipc import newComponent, status
from Kamaelia.IPC import socketShutdown, newCSA

from Kamaelia.IPC import newReader, newWriter
from Kamaelia.IPC import removeReader, removeWriter

#from Kamaelia.Internet.ConnectedSocketAdapter import ConnectedSocketAdapter
from ConnectedSocketAdapter import ConnectedSocketAdapter

#from Kamaelia.Internet.Selector import Selector
from Selector import Selector

class Multicast_transceiver(Axon.Component.component):
   """\
   Multicast_transceiver(local_addr,local_port,remote_addr,remote_port) -> new Multicast_transceiver component.

   Keyword arguments::

   - local_addr   -- address of the local interface to send to/receive from, usually "0.0.0.0"
   - local_port   -- port number to receive on
   - remote_addr  -- address of multicast group
   - remote_port  -- port number to send to
   """
   Inboxes  = { "inbox"           : "data to send to the socket",
                "_socketFeedback" : "notifications from the ConnectedSocketAdapter",
                "control"         : "Shutdown signalling"
              }
   Outboxes = { "outbox"         :  "data received from the socket",
                "signal"         :  "socket errors",
                "_selectorSignal"       : "For registering and deregistering ConnectedSocketAdapter components with a selector service",

              }
   Usescomponents=[ConnectedSocketAdapter] # List of classes used.

   def __init__(self,local_addr, local_port, remote_addr, remote_port):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Multicast_transceiver, self).__init__()
      self.local = (local_addr, local_port)
      self.remote = (remote_addr, remote_port)
      self.CSA = None
      self.sock = None

   def main(self):
      """Main loop."""

      for v in self.runClient():
         yield v
      
      if (self.sock is not None) and (self.CSA is not None):
         self.send(removeReader(self.CSA, self.sock), "_selectorSignal")
         self.send(removeWriter(self.CSA, self.sock), "_selectorSignal")
      

   def setupCSA(self, sock):
      """\
      setupCSA(sock) -> new ConnectedSocketAdapter component

      Creates a ConnectedSocketAdapter component for the socket, and wires up to
      it. Also sends the CSA to the "selector" service.
      """
      selectorService, selectorShutdownService, newSelector = Selector.getSelectorServices(self.tracker)
      if newSelector:
         self.addChildren(newSelector)

      CSA = ConnectedSocketAdapter(sock, selectorService, sendTo=self.remote) #  self.createConnectedSocket(sock)
      self.addChildren(CSA)
      self.link((self, "_selectorSignal"),selectorService)
 
      self.link((CSA, "CreatorFeedback"),(self,"_socketFeedback"))
      self.link((CSA, "outbox"), (self, "outbox"), passthrough=2)
      self.link((self, "inbox"), (CSA, "inbox"), passthrough=1)
      
      self.link((self, "control"), (CSA, "control"), passthrough=1)  # propagate shutdown msgs

      self.send(newReader(CSA, ((CSA, "ReadReady"), sock)), "_selectorSignal")            
      self.send(newWriter(CSA, ((CSA, "SendReady"), sock)), "_selectorSignal")            
      self.CSA = CSA # We need this for shutdown later

      return self.childComponents()

   def waitCSAClose(self):
      """Returns True if a socketShutdown message is received on "_socketFeedback" inbox."""
      if self.dataReady("_socketFeedback"):
         message = self.recv("_socketFeedback")
         if isinstance(message, socketShutdown):
            return False
      return True

   def safeConnect(self, sock):
      """\
      Connect to socket and handle possible errors that may occur.

      Returns True if successful, or False on failure. Unhandled errors are raised
      as exceptions.
      """
      try:
         sock.bind(self.local) # Receive from server on this port
            # EALREADY
            #   The  socket  is  non-blocking  and  a  previous connection
            #   attempt has not yet been completed.
         self.connecting=0
         return True
      except socket.error, socket.msg:
         (errorno, errmsg) = socket.msg.args
         if errorno==errno.EALREADY:
            # The socket is non-blocking and a previous connection attempt has not yet been completed
            # We handle this by allowing  the code to come back and repeatedly retry
            # connecting. This is a valid, if brute force approach.
            assert(self.connecting==1)
            return False
         if errorno==errno.EINPROGRESS or errorno==errno.EWOULDBLOCK:
            #The socket is non-blocking and the connection cannot be completed immediately.
            # We handle this by allowing  the code to come back and repeatedly retry
            # connecting. Rather brute force.
            self.connecting=1
            return False # Not connected should retry until no error
         if errorno == errno.EISCONN:
             # This is a windows error indicating the connection has already been made.
             self.connecting = 0 # as with the no exception case.
             return True
         # Anything else is an error we don't handle
         raise socket.msg

   def runClient(self,sock=None):
      # The various numbers yielded here indicate progress through the function, and
      # nothing else specific.
      try:
         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
         yield 0.3
         self.sock = sock # We need this for shutdown later
         try:
            sock.setblocking(0); yield 0.6
            try:
               while not self.safeConnect(sock):
                  if self.shutdown():
                      return
                  yield 1
               sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
               status = sock.setsockopt(socket.IPPROTO_IP,
                                        socket.IP_ADD_MEMBERSHIP,
                                        socket.inet_aton(self.remote[0]) + socket.inet_aton("0.0.0.0"))
               yield newComponent(*self.setupCSA(sock))
               while self.waitCSAClose():
                  self.pause()
                  yield 2
               raise Finality
            except Exception, x:
               result = sock.shutdown(2) ; yield 3
               raise x  # XXXX If X is not finality, an error message needs to get sent _somewhere_ else
               # The logical place to send the error is to the signal outbox
         except Exception, x:
            sock.close() ;  yield 4,x # XXXX If X is not finality, an error message needs to get sent _somewhere_ else
            raise x
      except Finality:
         yield 5
      except socket.error, e:
         # We now do the flipside of setupCSA, whether we had an error or not
         # A safe error relates to a disconnected server, and unsafe error is generally
         # bad. However either way, it's gone, let's let the person using this
         # component know, shutdown everything, and get outta here.
         #
         pass
         self.send(shutdownMicroprocess(self), "signal")
#          self.send(e, "signal")
        # "TCPC: Exitting run client"

   def shutdown(self):
       while self.dataReady("control"):
           msg = self.recv("control")
           self.send(msg,"signal")
           if isinstance(msg, (producerFinished,shutdownMicroprocess)):
               return True
       return False

__kamaelia_components__  = ( Multicast_transceiver, )


if __name__ =="__main__":
   pass
