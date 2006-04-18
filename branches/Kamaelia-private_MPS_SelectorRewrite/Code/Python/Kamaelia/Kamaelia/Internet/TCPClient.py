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
Simple TCP Client
=================

This component is for making a TCP connection to a server. Send to its "inbox"
inbox to send data to the server. Pick up data received from the server on its
"outbox" outbox.



Example Usage
-------------

Sending the contents of a file to a server at address 1.2.3.4 on port 1000::

    pipeline( RateControlledFileReader("myfile", rate=100000),
              TCPClient("1.2.3.4", 1000),
            ).activate()



How does it work?
-----------------

TCPClient opens a socket connection to the specified server on the specified
port. Data received over the connection appears at the component's "outbox"
outbox as strings. Data can be sent as strings by sending it to the "inbox"
inbox.

An optional delay (between component activation and attempting to connect) can
be specified. The default is no delay.

It creates a ConnectedSocketAdapter (CSA) to handle the socket connection and
registers it with a selectorComponent so it is notified of incoming data. The
selectorComponent is obtained by calling
selectorComponent.getSelectorService(...) to look it up with the local
Coordinating Assistant Tracker (CAT).

TCPClient wires itself to the "FactoryFeedback" outbox of the CSA. It also wires
its "inbox" inbox to pass data straight through to the CSA's "DataSend" inbox,
and its "outbox" outbox to pass through data from the CSA's "outbox" outbox.

Socket errors (after the connection has been successfully established) may be
sent to the "signal" outbox.

This component will terminate if the CSA sends a socketShutdown message to its
"FactoryFeedback" outbox.

Messages sent to the "control" inbox are ignored - users of this component
cannot ask it to close the connection.
"""

import socket
import errno

import Axon
from Axon.util import Finality
from Axon.Component import component
from Axon.Ipc import newComponent, status
from Kamaelia.KamaeliaIPC import socketShutdown, newCSA
from Kamaelia.Internet.ConnectedSocketAdapter import ConnectedSocketAdapter
import Axon.CoordinatingAssistantTracker as cat

import Selector

class TCPClient(component):
   """\
   TCPClient(host,port[,delay]) -> component with a TCP connection to a server.

   Establishes a TCP connection to the specified server.
   
   Keyword arguments:
   - host     -- address of the server to connect to (string)
   - port     -- port number to connect on
   - delay    -- delay (seconds) after activation before connecting (default=0)
   """
   Inboxes  = { "inbox"           : "data to send to the socket",
                "_socketFeedback" : "notifications from the ConnectedSocketAdapter",
                "control"         : "NOT USED"
              }
   Outboxes = { "outbox"         :  "data received from the socket",
                "signal"         :  "socket errors",
                "_selectorSignal" : "communicating with a selectorComponent",
              }
   Usescomponents=[ConnectedSocketAdapter] # List of classes used.

   def __init__(self,host,port,delay=0):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(TCPClient, self).__init__()
      self.host = host
      self.port = port
      self.delay=delay

   def main(self):
      """Main loop."""

      # wait before connecting
      import time
      t=time.time()
      while time.time()-t<self.delay:
         yield 1

      for v in self.runClient():
         yield v
      # SMELL - we may need to send a shutdown message

   def setupCSA(self, sock):
      """\
      setupCSA(sock) -> new ConnectedSocketAdapter component

      Creates a ConnectedSocketAdapter component for the socket, and wires up to
      it. Also sends the CSA to the "selector" service.
      """
      CSA = ConnectedSocketAdapter(sock) #  self.createConnectedSocket(sock)
      self.addChildren(CSA)
      selectorService , newSelector = Selector.selectorComponent.getSelectorService(self.tracker)
      if newSelector:
         self.addChildren(newSelector)

      self.link((self, "_selectorSignal"),selectorService)
      self.link((CSA, "FactoryFeedback"),(self,"_socketFeedback"))
      self.link((CSA, "outbox"), (self, "outbox"), passthrough=2)
      self.link((self, "inbox"), (CSA, "DataSend"), passthrough=1)

      self.send(newCSA(self, (CSA,sock)), "_selectorSignal")
      return self.childComponents()

   def waitCSAClose(self):
      """Returns True if a socketShutdown message is received on "_socketFeedback" inbox."""
      if self.dataReady("_socketFeedback"):
         message = self.recv("_socketFeedback")
         if isinstance(message, socketShutdown):
            return False
      return True

   def safeConnect(self, sock, *sockArgsList):
      """\
      Connect to socket and handle possible errors that may occur.

      Returns True if successful, or False on failure. Unhandled errors are raised
      as exceptions.
      """
      try:
         sock.connect(*sockArgsList); # Expect socket.error: (115, 'Operation now in progress')
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
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); yield 0.3
         try:
            sock.setblocking(0); yield 0.6
            try:
               while not self.safeConnect(sock,(self.host, self.port)):
                  yield 1
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
          self.send(e, "signal")
        # "TCPC: Exitting run client"

def _tests():
   from Axon.Linkage import linkage

   print "This test suite requires access to an active network server"
   client=TCPClient("127.0.0.1",1500)
   clientGen = client.main()
   r = clientGen.next() # assert r == 0.3 (Socket Created)
   assert r==0.3, "Socket Created"
   r = clientGen.next() # assert r == 0.6 (Socket set non-blocking)
   assert r==0.6, "Socket set non-blocking"
   r = clientGen.next() # assert r == 1   (Socket connecting)
   assert r==1, "Socket connecting"
   print "1", r
   m=clientGen.next()
   try:
      assert isinstance(m, newComponent), "We connected and have been returned a new component to activate"
   except AssertionError:
      print "Connection to remote server Failed", m
      raise

   print "cgn", m
   CSA=m.components()[0]

   # Put some linkages in place for testing
   outboxLink=linkage(CSA,client,"outbox","outbox",passthrough=2)
   feedbackLink=linkage(CSA,client,"FactoryFeedback","_socketFeedback")

   CSA.initialiseComponent()
   CSA.mainBody()
   CSA._deliver(status("data ready"),"DataReady")
   print CSA
   CSA.mainBody()
   print CSA
   CSA._deliver(socketShutdown(1),"control")
   print CSA
   CSA.mainBody()
   print CSA
   outboxLink.moveDataWithCheck()  # Move output from the CSA to output of the client
   feedbackLink.moveDataWithCheck()  # Move output from the CSA to input of client
   print CSA,"\n",client
   client._safeCollect("_selectorSignal")
   print client._safeCollect("outbox")
   print CSA,"\n",client
   for i in clientGen:
      print i

__kamaelia_components__  = ( TCPClient, )


if __name__ =="__main__":
   from Axon.Scheduler import scheduler
   from Kamaelia.SimpleServerComponent import SimpleServer
   from Kamaelia.Protocol.FortuneCookieProtocol import FortuneCookieProtocol
   from Kamaelia.Util.ConsoleEcho import  consoleEchoer
   # _tests()

   class testHarness(component): # Spike component to test interoperability with TCPServer
      def __init__(self):
         super(testHarness, self).__init__() # I wonder if this can get forced to be called automagically?
         import random
         self.serverport = random.randint(4000,8000)
         self.server = SimpleServer(protocol=FortuneCookieProtocol, port=self.serverport)
         self.client = None
         self.display = consoleEchoer()

      def initialiseComponent(self):
         self.client = TCPClient("127.0.0.1",self.serverport, delay=1)
         self.addChildren(self.server,self.client,self.display)
#         self.addChildren(self.server, self.display)
         self.link((self.client,"outbox"), (self.display,"inbox") )
         return Axon.Ipc.newComponent(*(self.children))

      def mainBody(self):
            return 1

   t = testHarness()
   t.activate()
   scheduler.run.runThreads(slowmo=0)
