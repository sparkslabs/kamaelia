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
   Inboxes = ["inbox", "_socketFeedback", "control"]
   Outboxes = ["outbox","signal","_selectorSignal"]
   Usescomponents=[ConnectedSocketAdapter] # List of classes used.

   def __init__(self,host,port,chargen=0,delay=0):
      self.__super.__init__()
      self.host = host
      self.port = port
      self.chargen=chargen
      self.delay=delay

   def main(self):
      import time
      t=time.time()
      while time.time()-t<self.delay:
         yield 1
      for v in self.runClient():
         yield v
      print "We have indeed ceased looking at the connection. "
      print "The stuff going on elsewhere is spurious"
      print "if we're closing down, and we know we're closing down,"
      print "then can send shutdown info from here"

   def setupCSA(self, sock):
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
      if self.dataReady("_socketFeedback"):
         message = self.recv("_socketFeedback")
         if isinstance(message, socketShutdown):
            return False
      return True

   def safeConnect(self, sock, *sockArgsList):
      try:
         sock.connect(*sockArgsList); # Expect socket.error: (115, 'Operation now in progress')
            # EALREADY
            #   The  socket  is  non-blocking  and  a  previous connection
            #   attempt has not yet been completed.
         self.connecting=0
         self.connected=1
         return True
      except socket.error, socket.msg:
         (errorno, errmsg) = socket.msg.args
         if errorno==errno.EALREADY:
            # The socket is non-blocking and a previous connection attempt has not yet been completed
            # We handle this by allowing  the code to come back and repeatedly retry
            # connecting. This is a valid, if brute force approach.
            assert(self.connecting==1)
            return False
         if errorno==errno.EINPROGRESS:
            #The socket is non-blocking and the connection cannot be completed immediately.
            # We handle this by allowing  the code to come back and repeatedly retry
            # connecting. Rather brute force.
            self.connecting=1
            return False # Not connected should retry until no error
         # Anything else is an error we don't handle
         raise socket.msg

   def runClient(self,sock=None):
      # The various numbers yielded here indicate progress through the function, and
      # nothing else specific.
      message = None
      try:
         print "TCPC: RHUBARB", 87
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
               print "TCPC: I would expect to get here"
               raise Finality
            except Exception, x:
               print "TCPC: I think we do indeed shutdown?"
               result = sock.shutdown(1) ; yield 3
               print "TCPC: We do indeed :)"
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
         message = e
      self.send(message, "signal")
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

if __name__ =="__main__":
   from Axon.Scheduler import scheduler
   from Kamaelia.SimpleServerComponent import SimpleServer
   from Kamaelia.Protocol.FortuneCookieProtocol import FortuneCookieProtocol
   from Kamaelia.Util.ConsoleEcho import  consoleEchoer
   # _tests()

   class testHarness(component): # Spike component to test interoperability with TCPServer
      def __init__(self):
         self.__super.__init__() # I wonder if this can get forced to be called automagically?
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
