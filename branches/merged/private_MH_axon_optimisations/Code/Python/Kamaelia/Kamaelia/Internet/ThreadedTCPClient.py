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
==========================
Simple Threaded TCP Client
==========================

This component is for making a TCP connection to a server. Send to its "inbox"
inbox to send data to the server. Pick up data received from the server on its
"outbox" outbox.

This component runs in its own separate thread so it can block on the socket
connection. This was written because some platforms that don't support
non-blocking calls to read/write data from sockets (eg. Python for
Nokia Series-60).



Example Usage
-------------

Sending the contents of a file to a server at address 1.2.3.4 on port 1000::

    pipeline( RateControlledFileReader("myfile", rate=100000),
              ThreadedTCPClient("1.2.3.4", 1000),
            ).activate()



How does it work?
-----------------

The component opens a socket connection to the specified server on the specified
port. Data received over the connection appears at the component's "outbox"
outbox as strings. Data can be sent as strings by sending it to the "inbox"
inbox.

The component will shutdown in response to a producerFinished message arriving
on its "control" inbox. The socket will be closed, and a socketShutdown message
will be sent to the "signal" outbox.

All socket errors exceptions are passed on out of the "signal" outbox. This will
always result in the socket being closed (if open) and a socketShutdown message
also being sent to the "signal" outbox (after the exception).

It does not use a ConnectedSocketAdapter, instead handling all socket
communications itself.

The compnent is based on Axon.ThreadedComponent.threadedcomponent
"""

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXX VOMIT
#
# - needs reworking somewhat - bit messy, plus lacks error handling
# - and spits all kinds of crud out of its "signal" outbox
# - shutdown behaviour is different to that of TCPClient
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

import socket
import errno
import Axon
from Axon.Component import component
from Kamaelia.KamaeliaIPC import socketShutdown
from Queue import Empty
import Axon.ThreadedComponent




class ThreadedTCPClient(Axon.ThreadedComponent.threadedcomponent):
   """\
   ThreadedTCPClient(host,port[,chargen][,initalsendmessage]) -> threaded component with a TCP connection to a server.

   Establishes a TCP connection to the specified server.
   
   Keyword arguments:
   - host     -- address of the server to connect to (string)
   - port     -- port number to connect on
   - initialsendmessage  -- to be send immediately after connection is established (default=None)
   """
   Inboxes  = { "inbox"   : "data to send to the socket",
                "control" : "",
              }
   Outboxes = { "outbox" : "data received from the socket",
                "signal" : "diagnostic output, errors and shutdown messages",
              }

   def __init__(self,host,port,chargen=0,initialsendmessage=None):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      self.__super.__init__()
      self.host = host
      self.port = port
      self.chargen=chargen
      self.sendmessage = initialsendmessage

   def run(self):
     """Main (thread) loop"""
     try:
      self.outqueues["signal"].put("Thread running",True)
      try:
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#; yield 0.3
      except socket.error, e:
         #handle initial failure to create socket.
         # If we can't create a socket we might as well give up now.
         # This matches the behaviour of the main TCP client but it might be better passing as
         # an Axon.Ipc.errorInformation carrying the exception otherwise what is the IPC class
         # for?
         self.outqueues["signal"].put(e)
         # I am assuming that by using queues there are no race conditions between this operations.
         self.outqueues["signal"].put(socketShutdown())
         return
      self.outqueues["signal"].put("socket object created")
      try:
         sock.connect((self.host, self.port))
      except socket.error, e:
         self.outqueues["signal"].put(e)
         try:
            result = sock.close()
         except:
            pass
         self.outqueues["signal"].put(socketShutdown())
         return
      self.outqueues["signal"].put("socket connected")
      
      producerFinished = 0
      if self.sendmessage != None:
        try:
            sock.send(self.sendmessage)
        except socket.error, e:
            self.outqueues["signal"].put(e)
            try:
                result = sock.close()
            except:
                pass
            self.outqueues["signal"].put(socketShutdown())
            return
      # This loop will handle sending, control and signal communications
      # including with the recv thread.  Apart from the sending all the calls
      # should be non-blocking.  sending should rarely take a significant
      # time.  One non-blocking call will operate with a short timeout to
      # prevent busy wait taking too much CPU time.
      while 1:
            try:
               data = sock.recv(1024)
               if not data: # This implies the connection has barfed.
                  break
               self.outqueues["outbox"].put(data)
#             except socket.timeout, to:
#               pass # common case Try again next loop.
            except socket.error, err:
               self.outqueues["signal"].put(err,True)
               break # The task is finished now.
         
            try:
               msg = self.inqueues["control"].get(False)
               if isinstance(msg, Axon.Ipc.producerFinished):
                  break
                  # Want to give opportunity for inbox messages to get into the
                  # inbox queue before shutting down the sending system.
            except Empty, e:
               pass # Normal case.
      
      #end while 1
      
      # After breaking out of while loop clean up socket before ending the thread.
      try:
         sock.shutdown(2)
      except socket.error, e:
         pass
      try:
         sock.close()
      except socket.error, e:
         self.outqueues["signal"].put(e)
      self.outqueues["signal"].put(socketShutdown())
      self.threadtoaxonqueue.put("ThreadStopped")
      #Normal exit
     except Exception, e:
      self.outqueues["signal"].put("Unexpected exception")
      self.outqueues["signal"].put(e)
      self.outqueues["signal"].put(socketShutdown())
      self.threadtoaxonqueue.put("ThreadStopped")
      #Unhandled exception exit.  Reports via the signal outqueue as it can't print errors here.

__kamaelia_components__  = ( ThreadedTCPClient, )


if __name__ =="__main__":
   from Axon.Scheduler import scheduler
   from Kamaelia.Util.ConsoleEcho import  consoleEchoer
   from Axon.Ipc import newComponent
   import Axon
   # _tests()

   class testHarness(component): # Spike component to test interoperability with TCPServer
      def __init__(self):
         self.__super.__init__() # I wonder if this can get forced to be called automagically?
         self.serverport = 4444
#         self.server = SimpleServer(protocol=FortuneCookieProtocol, port=self.serverport)
         self.client = None
         self.display = consoleEchoer()
         self.displayerr = consoleEchoer()

      def initialiseComponent(self):
         self.client = ThreadedTCPClient("132.185.133.18",self.serverport)
         self.addChildren(self.client,self.display,self.displayerr)
#         self.addChildren(self.server, self.display)
         self.link((self.client,"outbox"), (self.display,"inbox") )
         self.link((self.client,"signal"), (self.displayerr,"inbox") )
         self.link((self, "outbox"),(self.client, "inbox"))
         print self.children
         return Axon.Ipc.newComponent(*(self.children))

      def mainBody(self):
            return 1

   t = testHarness()
   t.activate()
   scheduler.run.runThreads(slowmo=0)
