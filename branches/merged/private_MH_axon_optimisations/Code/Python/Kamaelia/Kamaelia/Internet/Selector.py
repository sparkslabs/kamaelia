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
======================================
NOTIFICATION OF SOCKET AND FILE EVENTS
======================================

The selectorComponent listens for events on sockets and sends out notifications.
It is effectively a wrapper around the unix 'select' statement.

Components should register their ConnectedSocketAdapter (CSA) components with
the selectorComponent. The selector will then wire up to the CSA and provide it
with the notifications it needs.

The selectorComponent is a service that registers with the Coordinating
Assistant Tracker (CAT).



Example Usage
-------------

See the source code for TCPClient for an example of how the selectorComponent
can be used.



How does it work?
-----------------

The selectorComponent is a service. obtain it by calling the
selectorComponent.getSelectorService(...) static method. Any existing instance
will be returned, otherwise a new one is automatically created.

To register a socket with the selector, send a newCSA(self, (CSA, sock)) message
to the "notify" inbox. Where CSA is the component to be notified (usually a
ConnectedSocketAdapter component), and sock is the corresponding socket object
that selectorComponent should watch.

selectorComponent will wire itself to the target component's "DataReady" inbox
and "signal" outbox. (selectorComponent adds its own unique inbox(es) and
outbox(es) for this purpose).

When there is activity on the socket, the selectorComponent will send a
status("write ready") or status("data ready") message (as appropriate) to the
target component's "DataReady" inbox.

The socket is deregistered if the target component sends a
shutdownCSA(self, (CSA,sock)) message to its "signal" outbox. The
selectorComponent will stop sending it notifications and will unwire from it.

The selectorComponent does not terminate, even if there are no sockets for it
to watch. If termination is added, it must be taken into account that other
components in the system may still be retaining a reference to the
selectorComponent instance.
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
   """\
   selectorComponent() -> new selectorComponent component

   Use selectorComponent.getSelectorService(...) in preference as it returns an
   existing instance, or automatically creates a new one.
   """
   
   Inboxes  = { "inbox"   : "NOT USED",
                "control" : "NOT USED",
                "notify"  : "newCSA(...) and shutdownCSA(...) notifications",
              }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "NOT USED",
              }
              
   requiredInboxes=["DataReady"]    # required inboxes on target component
   requiredOutboxes=["signal"]      # required outboxes on target component
   
   def setSelectorService(selector, tracker = None):
        """\
        Sets the given selector as the service for the selected tracker or the
        default one.

        (static method)
        """
        if not tracker:
            tracker = cat.coordinatingassistanttracker.getcat()
        tracker.registerService("selector", selector, "notify")
   setSelectorService = staticmethod(setSelectorService)

   def getSelectorService(tracker=None): # STATIC METHOD
      """\
      Returns any live selector registered with the specified (or default) tracker,
      or creates one for the system to use.

      (static method)
      """
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
      """\
      validComponentInput((component,sock)) -> True/False
      
      True if the component is suitable to wire to the selectorComponent and
      sock is a socket.
      """
      interfaceOK = Axon.util.testInterface
      interfaceRequired = (selectorComponent.requiredInboxes,selectorComponent.requiredOutboxes)
      x,y = message
      return interfaceOK(x,interfaceRequired) and isinstance(y,socket.socket)
   validComponentInput=staticmethod(validComponentInput)

   def checkComponents(*components):
      """\
      checkComponents( *(component,sock) ) -> True/False

      True if all components are suitable to wire to the selectorComponent and
      if all socks are sockets.
      """
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
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(selectorComponent, self).__init__() # !!!! Must happen, if this method exists
      # Kept simple by NOT taking readers/writers etc at creation time - they're registered
      # via messages to an inbox instead
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
      """\
      Wires in the (component, socket) pair, so the component receives 
      notifications of events on socket.

      Checks their interfaces with validComponentInput().
      
      Does not check if the component,socket pair has already been wired in.
      """
      theComponent,theSocket = socketComponentPair
      selectorComponent.validComponentInput(socketComponentPair) # Raises invalidComponentInterface if wrong
      feedbackInboxName = self.addInbox("socketAdaptorFeedback")
      signalOutboxName = self.addOutbox("socketAdaptorSignal")
      #
      self.link((theComponent,self.requiredOutboxes[0]),(self,feedbackInboxName))
      self.link((self,signalOutboxName),(theComponent,self.requiredInboxes[0]))
      #
      self.lookupBoxes[theSocket] = (feedbackInboxName, signalOutboxName, theComponent)

   def wireOutComponent(self, socketComponentPair):
      """\
      Unwires the specified (component, socket) pair, so it no longer receives
      notifications of events on the socket.
      """
      # remove any lookup table entries
      # unwire
      # delete in/outboxes it used
      theComponent,theSocket = socketComponentPair
      (feedbackInboxName, signalOutboxName, theComponentL) = self.lookupBoxes[theSocket]
      assert(theComponent == theComponentL)
      del self.lookupBoxes[theSocket]
      self.postoffice.deregisterlinkage(thecomponent=theComponent)
      self.deleteInbox(feedbackInboxName)
      self.deleteOutbox(signalOutboxName)
      
   def checkForClosedSockets(self):
      pass
      #print "We're checking for closed sockets, but we're not really..."

   def handleNotify(self):
      """\
      Handle requests to register/deregister (component,socket) pairs.
      """
      if self.dataReady("notify"):
         message = self.recv("notify")

         payload,caller = message.object, message.caller
         managingComponent, sock = payload
         if isinstance(message, shutdownCSA): # This is cack - this should use a different inbox
            try: self.writersockets.remove(sock)
            except: pass
            try: self.readersockets.remove(sock)
            except: pass
            self.wireOutComponent((managingComponent, sock))
         else:
            if message.handlesWriting():
               self.writersockets.append(sock)
            else:
               self.readersockets.append(sock)
            self.wireInComponent((managingComponent, sock))

   def handleExceptionalSocket(self, sock):
      """ Currently there is no support for exceptional sockets"""
      pass

   def handleWriteableSocket(self, sock):
      """Notifys corresponding component that its socket is ready for writing new data."""
      (feedbackInboxName, signalOutboxName, theComponent) = self.lookupBoxes[sock]
      self.send(status("write ready"),signalOutboxName)

   def handleReadableSocket(self, sock):
      """Notifys corresponding component that its socket is ready for reading new data."""
      (feedbackInboxName, signalOutboxName, theComponent) = self.lookupBoxes[sock]
      self.send(status("data ready"),signalOutboxName)

   def main(self):
      """Main loop"""
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
   """\
      Returns any live selector registered with the specified (or default) tracker,
      or creates one for the system to use.

      (Identical to selectorComponent.getSelectorService(...)
   """
   if tracker is None:
      tracker = cat.coordinatingassistanttracker.getcat()
   try:
      service = tracker.retrieveService("selector")
      return service, None
   except KeyError:
      selector = selectorComponent()
      service = (selector,"notify")
      return service, selector

__kamaelia_components__  = ( selectorComponent, )



if __name__ =="__main__":
   #_tests()
   x=selectorComponent()
   x.getSelectorService()
   x.validComponentInput((x,"str"))

