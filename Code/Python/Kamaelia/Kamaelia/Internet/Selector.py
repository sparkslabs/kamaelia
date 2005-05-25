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
"""

"""
import socket
import Axon
import select
from Axon.Ipc import status
import Axon.CoordinatingAssistantTracker as cat
from Kamaelia.KamaeliaIPC import shutdownCSA
AdaptiveCommsComponent=Axon.AdaptiveCommsComponent.AdaptiveCommsComponent
import time

class selectorComponent(AdaptiveCommsComponent):
   Inboxes=["inbox", "control","notify"]
   Outboxes=["outbox","signal"]
   requiredInboxes=["DataReady"]
   requiredOutboxes=["signal"]
   
   def setSelectorService(selector, tracker = None):
        "Sets the given selector as the service for the selected tracker or the default one."
        if not tracker:
            tracker = cat.coordinatingassistanttracker.getcat()
        tracker.registerService("selector", selector, "notify")
   setSelectorService = staticmethod(setSelectorService)

   def getSelectorService(tracker=None): # STATIC METHOD
      "Returns any live selector in the system, or creates one for the system to use"
      if tracker is None:
         tracker = cat.coordinatingassistanttracker.getcat()
      try:
         service = tracker.retrieveService("selector")
         return service, None
      except KeyError:
         selector = selectorComponent()
         selectorComponent.setSelectorService(selector, tracker)
         service=(selector,"notify")
         return service, selector
   getSelectorService = staticmethod(getSelectorService)

   def validComponentInput(message):
      interfaceOK = Axon.util.testInterface
      interfaceRequired = (selectorComponent.requiredInboxes,selectorComponent.requiredOutboxes)
      x,y = message
      return interfaceOK(x,interfaceRequired) and isinstance(y,socket.socket)
   validComponentInput=staticmethod(validComponentInput)

   def checkComponents(*components):
      "Check that the supplied components actually have the interface we require to link with"
      safeList=Axon.util.safeList
      theComponents = reduce(list.__add__,[safeList(x) for x in components])
      try:
         [ selectorComponent.validComponentInput(x) for x in theComponents ]
      except AttributeError, e:
         return False
      except ValueError, e:
         return False
      else:
         return True
   checkComponents=staticmethod(checkComponents)

   def __init__(self):
      """This used to take readers, writers, etc at creation time, but this made the system far more
      complex than it had to be, and the functionality has been removed to simplify the code. Server
      CSA factories and CSA's now need to be supplied via inboxes. Quite dramatically simplifies the
      code"""
      super(selectorComponent, self).__init__() # !!!! Must happen, if this method exists
      self.t = 0
      self.readers=[]
      self.writers=[]
      self.exceptionals=[]
      self.serversockets=[] # Server sockets? (subset of readers)
      self.readersockets=[] # General readers (includes listeners)
      self.writersockets=[] # Any writers
      self.exceptsockets = [] # Hmm...
      self.lookupBoxes = {}
      self.socketToOutbox = {}
      self.inboxToSocket = {}

   def wireInComponent(self, socketComponentPair):
      # Needs to check to see if the component pair has already been wired
      # in - due to changes in usage...
      # Actually now need to ensure that components have their interfaces checked *here*
      theComponent,theSocket = socketComponentPair
      selectorComponent.validComponentInput(socketComponentPair) # Raises invalidComponentInterface if wrong
      feedbackInboxName = self.addInbox("socketAdaptorFeedback")
      signalOutboxName = self.addOutbox("socketAdaptorSignal")
      #
      self.link((theComponent,self.requiredOutboxes[0]),(self,feedbackInboxName))
      self.link((self,signalOutboxName),(theComponent,self.requiredInboxes[0]))
      #
      self.lookupBoxes[theSocket] = (feedbackInboxName, signalOutboxName, theComponent)

   def checkForClosedSockets(self):
      pass
      #print "We're checking for closed sockets, but we're not really..."

   def handleNotify(self):
      if self.dataReady("notify"):
         message = self.recv("notify")

         payload,caller = message.object, message.caller
         managingComponent, sock = payload
         if isinstance(message, shutdownCSA): # This is cack - this should use a different inbox
            #
            # Problems with this:
            #    * This removes writing sockets only
            #    * It doesn't remove reading sockets
            #    * It doen't unwire any components
            #    * It doesn't remove any new in/out boxes
            #
            self.writersockets.remove(sock)
         else:
            if message.handlesWriting():
               self.writersockets.append(sock)
            else:
               self.readersockets.append(sock)
         self.wireInComponent((managingComponent, sock))  ### PROBLEM IS HERE... COOL.

   def handleExceptionalSocket(self, sock):
      """ Currently there is no support for exceptional sockets"""
      pass

   def handleWriteableSocket(self, sock):
      (feedbackInboxName, signalOutboxName, theComponent) = self.lookupBoxes[sock]
      self.send(status("write ready"),signalOutboxName)

   def handleReadableSocket(self, sock):
      (feedbackInboxName, signalOutboxName, theComponent) = self.lookupBoxes[sock]
      self.send(status("data ready"),signalOutboxName)

   def main(self):
      while 1:
         # print "ME", self
         # print "SERVER SOCKETS", self.readersockets
         # print "CONNECTED SOCKETS", self.writersockets
         self.handleNotify()
         # Do we actually do this any more?!
         self.checkForClosedSockets()
                        # Yes, its the way we get told a CSA/SF wishes to shutdown
                        # So actually a check for shutdown components
                        # Actually the checkForClosedSockets call is currently bunk
                        # Problems
         try:
            readables, writeables, excepts = select.select(self.readersockets, self.writersockets, [],0)
            for sock in readables:
               passBackResult = self.handleReadableSocket(sock)
               if passBackResult:
                  yield passBackResult
            for sock in writeables:
               passBackResult = self.handleWriteableSocket(sock)
               if passBackResult:
                  yield passBackResult
            #
            # for sock in excepts:
            #   passBackResult = self.handleExceptionalSocket(sock)
            #   if passBackResult:
            #      yield passBackResult
         except socket.error,e:
                  # (feedbackInboxName, signalOutboxName, theComponent) = self.lookupBoxes[sock]
                  if e[0] is 9 and time.time() - self.t > 1:
                     # print "SEL: Socket Error:", e[1]
                     # print "SEL: We want to remove the socket from the set of things to check"
                     # print "SEL:    Specifically: ", sock
                     # print "SEL: We want to signal the component to shutdown"
                     # print "SEL: We want to remove all references we have"
                     # print "SEL:    Specifically: ","".join([str(x)+"\n                  " for x in self.lookupBoxes[sock]])
                     # print "SEL: We let the thing managing the socket close the socket"
                     component = self.lookupBoxes[sock][2]
                     # print "SEL: Component that needs a shutdown message",component
                     # print "SEL: Contents out inboxes it has", component.inboxes
                     # print "SEL: Contents of DataReady inbox", [ x.status() for x in component.inboxes["DataReady"] ]
                     self.t = time.time()

                  if e[0] is not 9:
                     raise e
         yield status("ready")

def getSelectorService(tracker=None):
   "Returns any live selector in the system, or creates one for the system to use"
   if tracker is None:
      tracker = cat.coordinatingassistanttracker.getcat()
   try:
      service = tracker.retrieveService("selector")
      return service, None
   except KeyError:
      selector = selectorComponent()
      service = (selector,"notify")
      return service, selector


if __name__ =="__main__":
   #_tests()
   x=selectorComponent()
   x.getSelectorService()
   x.validComponentInput((x,"str"))

