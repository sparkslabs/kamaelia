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
import Queue
#from Kamaelia.Internet.ConnectedSocketAdapter import ConnectedSocketAdapter
#import Axon.CoordinatingAssistantTracker as cat

whinge = { "socketSendingFailure": True, "socketRecievingFailure": True }
crashAndBurn = { "uncheckedSocketShutdown" : True,
                            "receivingDataFailed" : True,
                            "sendingDataFailed" : True }

class receiveThread(threading.Thread):
   """
   This class is intended purely to make blocking receive calls.
   """
   def __init__(self,socket, outputqueue,controlqueue,signalqueue,size = 1024):
      self.Thread.__init__()
      self.oq = outputqueue
      self.cq = controlqueue
      self.sq = signalqueue
      self.size = size
      self.sock = socket
   def run():
      try:
         while 1:
            data = socket.recv(self.size)
            if not data: # This implies the connection has barfed.
               raise connectionDiedReceiving(sock,size)
            self.oq.put(socketdata)
            try:
               msg = self.cq.get(False)
               if msg == "StopThread":
                  break # Stop the iteration ignoring unread data.  The consumer is no longer
                            # iterested.
            except Empty: # This is the normal case
               pass
      except socket.error, socket.msg:
         # This is an actual error as we are blocking so should not receive errors
         (errorno, errmsg) = socket.msg.args # Copied from CSA
         self.sq.put(socket.msg)
      except connectionDiedReceiving, cd:
         self.sq.put(cd)
      except Exception, e: # Unexpected error that might cause crash. Do we want to really crash & burn?
         self.sq.put(e)
         if crashAndBurn["receivingDataFailed"]:
            # Should this be dealt with in the main socket thread.
            raise e #Throw as an uncaught exception as it is unexpected behaviour.
      try:
         self.sock.shutdown(0)
      except:
         pass # Don't need to do much here, shutdown is largely for politeness and may well have already
                 # been done.  The error is of little consequence to further actions.
      self.signalqueue.put("StoppedThread")
         

class ThreadedTCPClient(threadedcomponent):
   Inboxes = ["inbox", "control"]
   Outboxes = ["outbox","signal"]
#   Usescomponents=[ConnectedSocketAdapter] # List of classes used.

   def __init__(self,host,port,chargen=0,delay=0):
      self.__super.__init__()
      self.host = host
      self.port = port
      self.chargen=chargen
      self.delay=delay
      self.recvthreadsignal = Queue.Queue()
      self.recvthreadcontrol = Queue.Queue()

#   def setupCSA(self, sock):
#      CSA = ConnectedSocketAdapter(sock) #  self.createConnectedSocket(sock)
#      self.addChildren(CSA)
#      selectorService , newSelector = Selector.selectorComponent.getSelectorService(self.tracker)
#      if newSelector:
#         self.addChildren(newSelector)

#      self.link((self, "_selectorSignal"),selectorService)
#      self.link((CSA, "FactoryFeedback"),(self,"_socketFeedback"))
#      self.link((CSA, "outbox"), (self, "outbox"), passthrough=2)
#      self.link((self, "inbox"), (CSA, "DataSend"), passthrough=1)

#      self.send(newCSA(self, (CSA,sock)), "_selectorSignal")
#      return self.childComponents()

##~    def waitCSAClose(self):
##~       if self.dataReady("_socketFeedback"):
##~          message = self.recv("_socketFeedback")
##~          if isinstance(message, socketShutdown):
##~             return False
##~       return True

##~    def safeConnect(self, sock, *sockArgsList):
##~       try:
##~          sock.connect(*sockArgsList); # Expect socket.error: (115, 'Operation now in progress')
##~             # EALREADY
##~             #   The  socket  is  non-blocking  and  a  previous connection
##~             #   attempt has not yet been completed.
##~          self.connecting=0
##~          self.connected=1
##~          return True
##~       except socket.error, socket.msg:
##~          (errorno, errmsg) = socket.msg.args
##~          if errorno==errno.EALREADY:
##~             # The socket is non-blocking and a previous connection attempt has not yet been completed
##~             # We handle this by allowing  the code to come back and repeatedly retry
##~             # connecting. This is a valid, if brute force approach.
##~             assert(self.connecting==1)
##~             return False
##~          if errorno==errno.EINPROGRESS:
##~             #The socket is non-blocking and the connection cannot be completed immediately.
##~             # We handle this by allowing  the code to come back and repeatedly retry
##~             # connecting. Rather brute force.
##~             self.connecting=1
##~             return False # Not connected should retry until no error
##~          # Anything else is an error we don't handle
##~          raise socket.msg

   def run(self):
      try:
         print "TCPC: RHUBARB", 87
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#; yield 0.3
      except socket.error, e:
         #handle initial failure to create socket.
         # If we can't create a socket we might as well give up now.
         # This matches the behaviour of the main TCP client but it might be better passing as
         # an Axon.Ipc.errorInformation carrying the exception otherwise what is the IPC class
         # for?
         self.outqueues["signal"].put(e)
         # I am assuming that by using queues there are no race conditions between this operations.
         self.threadtoaxonqueue.put("StoppedThread")
         return
      try:
         sock.connect(self.host, self.port)
      except socket.error, e:
         self.outqueues["signal"].put(e)
         try:
            result = sock.close()
         except:
            pass
         self.threadtoaxonqueue("StoppedThread")
         return
      receivethread = receiveThread(socket = sock, outputqueue = self.outqueues["outbox"],controlqueue = self.recvthreadcontrol,signalqueue = recvthreadsignal)
      receivethread.setDaemon(True)
      receivethread.start()
      recvingfinished = False
      sendingfinished = False
      producerFinished = 0
      while 1:
         # This loop will handle sending, control and signal communications
         # including with the recv thread.  Apart from the sending all the calls
         # should be non-blocking.  sending should rarely take a significant
         # time.  One non-blocking call will operate with a short timeout to
         # prevent busy wait taking too much CPU time.
         
         # TODO: All Exception Handling
         if not sendingfinished:
            try:
               # This blocks for a short time to avoid busy wait if there is
               # nothing to do.
               data = self.inqueues["inbox"].get(True, 0.2)
               sock.send(data)
               if producerFinished: #If there is still coming extend the time
                                               #window for data to get in the queue
                  producerFinished = time.time()
            except Empty, e:
                # A four second delay ought to be enough for the component to
                # get a timeslice and move some data from inbox to the queue.
                # Yet it shouldn't cause critical errors, delays or leaks if it
                # allowed to take this long.
               if time.time() > producerFinished + 4:
                  try:
                     sock.shutdown(1)
                  except socket.error, e:
                     pass
                  sendingfinished = True
                  if receiverFinished:
                     break
            except socket.error, err:
               self.outqueues["signal"].put(err)
               try:
                  sock.shutdown(1)
               except socket.error, e:
                  pass
               sendingfinished = True
               if receiverFinished:
                  break # The task is finished now.
         
         if not receivingfinished:
            try:
               msg = self.recvthreadsignal.get(False)
               if msg == "ThreadStopped":
                  recvingfinished = True
                  # self.outqueues["signal"].put(consumerFinished())
               else:
                  self.outqueues["signal"].put(msg)
            except Empty, e:
               pass # This is the common case.

         try:
            msg = self.inqueues["control"].get(False)
            if isinstance(msg, producerFinished):
               producerStopTime = time.time() 
               # Want to give opportunity for inbox messages to get into the
               # inbox queue before shutting down the sending system.
         except Empty, e:
            pass # Normal case.

      try:
         sock.close()
      except socket.error, e:
         self.outqueues["signal"].put(e)
      self.outqueues["signal"].put(socketShutdown())
      self.signalqueue.put("ThreadStopped")
   
   def __startrecvthread(self, sock):
      

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
