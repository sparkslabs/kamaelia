#!/usr/bin/env python2.3

import socket
import socketConstants
import Axon
from Axon.util import Finality
from Axon.Component import component
from Axon.Ipc import newComponent, status
from Kamaelia.KamaeliaIPC import socketShutdown, newCSA
from Kamaelia.Internet.VirtualConnectedSocketAdapter import VirtualConnectedSocketAdapter
import Axon.CoordinatingAssistantTracker as cat

import Selector

class UDPPeer(component):
   Inboxes = ["inbox", "_socketFeedback", "control"]
   Outboxes = ["outbox","signal","_selectorSignal"]
   Usescomponents=[VirtualConnectedSocketAdapter] # List of classes used.

   def __init__(self,host,port,chargen=0,delay=0):
      self.__super.__init__()
      self.host = host
      self.port = port
      self.chargen=chargen
      self.delay=delay
      self.sock = None # XXXX
      print "Created"
# XXXX self.buf=buf

   def main(self):
      print "CLIENT RUNNING"
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

   def setupVCSA(self, sock):
      """XXXX Is ths as simple?"""
      print "GOO GOO GA GA"
      VCSA = VirtualConnectedSocketAdapter(sock, (self.host,self.port)) #  self.createConnectedSocket(sock)
      self.addChildren(VCSA)
      selectorService , newSelector = Selector.selectorComponent.getSelectorService(self.tracker)
      if newSelector:
         self.addChildren(newSelector)

      self.link((self, "_selectorSignal"),selectorService)
      self.link((VCSA, "FactoryFeedback"),(self,"_socketFeedback"))
      self.link((VCSA, "outbox"), (self, "outbox"), passthrough=2)
      self.link((self, "inbox"), (VCSA, "DataSend"), passthrough=1)

      self.send(newCSA(self, (VCSA,sock)), "_selectorSignal")
      return self.childComponents()

   def waitVCSAClose(self):
      if self.dataReady("_socketFeedback"):
         message = self.recv("_socketFeedback")
         if isinstance(message, socketShutdown):
            print "waitVCSAClose:"+str(message)+":"
            return False
      return True

   def setup(self):
      print "SETUP"
      self.sock.bind(("",0))

   def shutdown(self,addr):
      print "SHUTTING DOWN UDPPEER"
      print "HMM", self.sock.sendto('',addr)

   def runClient(self,sock=None):
      # The various numbers yielded here indicate progress through the function, and
      # nothing else specific.
      addr=(self.host,self.port)
      message = None
      try:
         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); yield 0.3 # UDPP
         try:
            self.sock.setblocking(0); yield 0.6
            # UDPP IP,port= self.sock.getsockname()
            try:
               self.setup() # UDPP
               # UDPP IP,port= self.sock.getsockname()
               # while not self.safeConnect(self.sock,(self.host, self.port)): UDPP
               #     We're UDP, we don't have to worry about this - no connection phase.
               #   yield 1
               #
               # Nice suggestion - collapse this into setup
               # 
               yield newComponent(*self.setupVCSA(self.sock))
               while self.waitVCSAClose():
                  self.pause()
                  yield 2
               raise Finality
            except Exception, x:
               print "Exception that caused us to shutdown:"+repr(x)+":"
               self.shutdown(addr) # UDPP
               # result = self.sock.shutdown(1) ; yield 3 # UDPP (Differs)
               raise x  # UDPP If X is not finality, an error message needs to get sent _somewhere_ else
               # The logical place to send the error is to
         except Exception, x:
            # UDPP - We don't/should NOT call close on ths.
            #self.sock.close() ;  yield 4,x # UDPP If X is not finality, an error message needs to get sent _somewhere_ else
            raise x
      except Finality:
         yield 5
      except socket.error, e:
         # We now do the flipside of setupVCSA, whether we had an error or not
         # A safe error relates to a disconnected server, and unsafe error is generally
         # bad. However either way, it's gone, let's let the person using this
         # component know, shutdown everything, and get outta here.
         #
         message = e
      self.send(message, "signal")

def _tests():
   from Axon.Linkage import linkage

   print "This test suite requires access to an active network server"
   client=UDPPeer("127.0.0.1",1500)
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
   VCSA=m.components()[0]

   # Put some linkages in place for testing
   outboxLink=linkage(VCSA,client,"outbox","outbox",passthrough=2)
   feedbackLink=linkage(VCSA,client,"FactoryFeedback","_socketFeedback")

   VCSA.initialiseComponent()
   VCSA.mainBody()
   VCSA._deliver(status("data ready"),"DataReady")
   print VCSA
   VCSA.mainBody()
   print VCSA
   VCSA._deliver(socketShutdown(1),"control")
   print VCSA
   VCSA.mainBody()
   print VCSA
   outboxLink.moveDataWithCheck()  # Move output from the VCSA to output of the client
   feedbackLink.moveDataWithCheck()  # Move output from the VCSA to input of client
   print VCSA,"\n",client
   client._safeCollect("_selectorSignal")
   print client._safeCollect("outbox")
   print VCSA,"\n",client
   for i in clientGen:
      print i

if __name__ =="__main__":

   from Axon.Scheduler import scheduler
   from Kamaelia.SimpleServerComponent import SimpleServer
   from Kamaelia.Protocol.FortuneCookieProtocol import FortuneCookieProtocol
   from Kamaelia.Util.ConsoleEcho import  consoleEchoer
   # _tests()
   import time

   class testHarness(component):
      def __init__(self):
         self.__super.__init__()
         self.serverport = 1701
         self.time = time.time()
         self.start = self.time

      def initialiseComponent(self):
         self.client = UDPPeer("127.0.0.1",self.serverport)
         self.addChildren(self.client)
         return Axon.Ipc.newComponent(*(self.children))

      def mainBody(self):
        if time.time() - self.start <10:
           if time.time() - self.time >1:
              self.time = time.time()
              self.client._deliver("Running","inbox")
              print "Running"
           return 1
        else:
           return 0
           
   t = testHarness()
   t.activate()
   scheduler.run.runThreads(slowmo=0)


   if 0:
      class testHarness(component): # Spike component to test interoperability with TCPServer
         def __init__(self):
            self.__super.__init__() # I wonder if this can get forced to be called automagically?
            import random
            self.serverport = random.randint(4000,8000)
            self.server = SimpleServer(protocol=FortuneCookieProtocol, port=self.serverport)
            self.client = None
            self.display = consoleEchoer()

         def initialiseComponent(self):
            self.client = UDPPeer("127.0.0.1",self.serverport, delay=1)
            self.addChildren(self.server,self.client,self.display)
            self.link((self.client,"outbox"), (self.display,"inbox") )
            return Axon.Ipc.newComponent(*(self.children))

         def mainBody(self):
               return 1
