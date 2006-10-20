#!/usr/bin/env python
#
# FIXME: This doesn't really provide a means for people to ask for
#        the service and release the service. The problem this
#        causes is that the selector has no simple means of shutting
#        down when no one is using it.
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
"""\
======================================
NOTIFICATION OF SOCKET AND FILE EVENTS
======================================

The Selector component listens for events on sockets and sends out notifications.
It is effectively a wrapper around the unix 'select' statement. Components
request that the Selector component notify them when a supplied socket or file
object is ready.

The selectorComponent is a service that registers with the Coordinating
Assistant Tracker (CAT).

NOTE: The behaviour and API of this component changed in Kamaelia 0.4 and is
likely to change again in the near future.



Example Usage
-------------

See the source code for TCPClient for an example of how the Selector component
can be used.



How does it work?
-----------------

Selector is a service. Obtain it by calling the static method 
Selector.getSelectorService(...). Any existing instance will be returned,
otherwise a new one is automatically created.

This component ignores anything sent to its "inbox" and "control" inboxes. This
component does not terminate.

Register socket or file objects with the selector, to receive a one-shot
notification when that file descriptor is ready. The file descriptor can be
a python file object or socket object. The notification is one-shot - meaning
you must resubmit your request every time you wish to receive a notification.

Ensure you deregister the file object when closing the file/socket. You may do
this even if you have already received the notification. The Selector component
will be unable to handle notifications for any other descriptors if it still has
a registered descriptor that has closed.

Register for a notification by sending an one of the following messages to the
"notify" inbox, as returned by Selector.getSelectorService():
   * Kamaelia.KamaeliaIpc.newReader( (component,inboxname), descriptor)
   * Kamaelia.KamaeliaIpc.newWriter( (component,inboxname), descriptor)
   * Kamaelia.KamaeliaIpc.newExceptional( (component,inboxname), descriptor)
   
Choose which as appropriate:
   * a newReader() request will notify when there is data ready to be read on
     the descriptor
   * a newWriter() request will notify when writing to the descriptor will not
     block.
   * a newExceptional() request will notify when an exceptional event occurs on
     the specified descriptor.
     
Selector will notify the taret component by sending the file/socket descriptor
object to the target inbox the component provided. It then automatically
deregisters the descriptor, unlinking from the target component's inbox.

For a given descriptor for a given type of event (read/write/exceptional) only
one notification will be sent when the event occurs. If multiple notification
requests have been received, only the first is listened to; all others are
ignored.

Of course, once the notification as happened, or someone has requested that
descriptor be deregistered, then someone can register for it once again.

Deregister by sending on of the following messages to the "notify" inbox of
Selector:
   * Kamaelia.KamaeliaIpc.removeReader( (component,inboxname), descriptor)
   * Kamaelia.KamaeliaIpc.removeWriter( (component,inboxname), descriptor)
   * Kamaelia.KamaeliaIpc.removeExceptional( (component,inboxname), descriptor)

It is advisable to send a deregister message when the corresponding file
descriptor closes, in case you registered for a notification, but it has not
occurred.
"""


import Axon
from Axon.Ipc import shutdown
import select, socket
from Kamaelia.IPC import newReader, removeReader, newWriter, removeWriter, newExceptional, removeExceptional
import Axon.CoordinatingAssistantTracker as cat
from Axon.ThreadedComponent import threadedadaptivecommscomponent
import time
#import sys,traceback

READERS,WRITERS, EXCEPTIONALS = 0, 1, 2
FAILHARD = False
timeout = 5

from Axon.Component import component

class _SelectorCore(threadedadaptivecommscomponent): #Axon.AdaptiveCommsComponent.AdaptiveCommsComponent): # SmokeTests_Selector.test_SmokeTest
    """\
    Selector() -> new Selector component

    Use Selector.getSelectorService(...) in preference as it returns an
    existing instance, or automatically creates a new one.
    """
    Inboxes = {
         "control" : "Recieving a Axon.Ipc.shutdown() message here causes shutdown",
         "inbox" : "Not used at present",
         "notify" : "Used to be notified about things to select"
    }

    def __init__(self,notifySocket=None):
        super(_SelectorCore, self).__init__()
        self.minSelectables = 0
        self.notifySocket = notifySocket
        if self.notifySocket:
            self.minSelectables += 1
            
    def removeLinks(self, selectable, meta, selectables):
        """\
        Removes a file descriptor (selectable).
        
        Removes the corresponding entry from meta and selectables; unlinks from
        the component to be notified; and deletes the corresponding outbox.
        """
#        \
#print "removeLinks",selectable,meta,selectables
        try:
            replyService, outbox, Linkage = meta[selectable]
            self.unlink(thelinkage=Linkage)
            selectables.remove(selectable)
            self.deleteOutbox(outbox)
            del meta[selectable]
            Linkage = None
        except:
            pass

    def addLinks(self, replyService, selectable, meta, selectables, boxBase):
        """\
        Adds a file descriptor (selectable).
        
        Creates a corresponding outbox, with name based on boxBase; links it to
        the component that wants to be notified; adds the file descriptor to the
        set of selectables; and records the box and linkage info in meta.
        """
        if selectable not in meta:
            outbox = self.addOutbox(boxBase)
            L = self.link((self, outbox), replyService)
            meta[selectable] = replyService, outbox, L
            selectables.append(selectable)
            return L
        else:
            return meta[selectable][2]

    def handleNotify(self, meta, readers,writers, exceptionals):
        """\
        Process requests to add and remove file descriptors (selectables) that
        arrive at the "notify" inbox.
        """
        while self.dataReady("notify"):
            message = self.recv("notify")
#            \
#print type(message)
            if isinstance(message, newReader):
                replyService, selectable = message.object
                L = self.addLinks(replyService, selectable, meta[READERS], readers, "readerNotify")
                L.showtransit = 0

            if isinstance(message, newWriter):
                replyService, selectable = message.object
                L = self.addLinks(replyService, selectable, meta[WRITERS], writers, "writerNotify")
                L.showtransit = 0

            if isinstance(message, newExceptional):
                replyService, selectable = message.object
                self.addLinks(replyService, selectable, meta[EXCEPTIONALS], exceptionals, "exceptionalNotify")

            if isinstance(message, removeReader):
                selectable = message.object
                self.removeLinks(selectable, meta[READERS], readers)

            if isinstance(message, removeWriter):
                selectable = message.object
                self.removeLinks(selectable, meta[WRITERS], writers)

            if isinstance(message, removeExceptional):
                selectable = message.object
                self.removeLinks(selectable, meta[EXCEPTIONALS], exceptionals)

    def main(self):
        """Main loop"""
        global timeout
        readers,writers, exceptionals = [],[], []
        if self.notifySocket:
            readers.append(self.notifySocket)
        selections = [readers,writers, exceptionals]
        meta = [ {}, {}, {} ]
        if not self.anyReady():
            self.sync()        # momentary pause-ish thing
        last = 0
        numberOfFailedSelectsDueToBadFileDescriptor = 0
        shuttingDown = False
        while 1: # SmokeTests_Selector.test_RunsForever
            if self.dataReady("control"):
                message = self.recv("control")
                if isinstance(message,shutdown):
#                   print "recieved shutdown message"
                   shutdownStart = time.time()
                   timeWithNooneUsing = 0
                   shuttingDown = True
            if shuttingDown:
#               print "we're shutting down"
               if len(readers) + len(writers) + len(exceptionals) <= self.minSelectables: # always have at least teh wakeup socket
                   if timeWithNooneUsing == 0:
#                       print "starting timeout"
                       timeWithNooneUsing = time.time()
                   else:
                       if time.time() - timeWithNooneUsing > timeout:
#                           print "Yay, timed out!"
                           break # exit the loop
               else:
                   timeWithNooneUsing == 0 # reset this to zero if readers/writers/excepts goes up again...
#               else:
#                   print "But someone is still using us...."
#                   print readers, writers, exceptionals
                   
            self.handleNotify(meta, readers,writers, exceptionals)
            if len(readers) + len(writers) + len(exceptionals) > 0:
                try:
                    read_write_except = select.select(readers, writers, exceptionals,5) #0.05
                    numberOfFailedSelectsDueToBadFileDescriptor  = 0
                    
                    for i in xrange(3):
                        for selectable in read_write_except[i]:
                            try:
                                replyService, outbox, linkage = meta[i][selectable]
                                self.send(selectable, outbox)
                                replyService, outbox, linkage = None, None, None
                                # Note we remove the selectable until we know the reason for it being here has cleared.
                                self.removeLinks(selectable, meta[i], selections[i])
                            except KeyError, k:
                                # must be the wakeup signal, don't remove it or act on it
                                selectable.recv(1)
                            
                except ValueError, e:
                    if FAILHARD: 
                        raise e
                except socket.error, e:
                    if e[0] == 9:
                        numberOfFailedSelectsDueToBadFileDescriptor +=1
                        if numberOfFailedSelectsDueToBadFileDescriptor > 1000:
                            # For the moment, we simply raise an exception.
                            # We could brute force our way through the list of descriptors
                            # to find the broken ones, and remove
                            raise e

                self.sync()
            elif not self.anyReady():
                self.pause()        # momentary pause-ish thing
#            else:
#                print "HMM"
##        print "SELECTOR HAS EXITTED"


class Selector(component):
    Inboxes = {
         "control" : "Recieving a Axon.Ipc.shutdown() message here causes shutdown",
         "inbox" : "Not used at present",
         "notify" : "Used to be notified about things to select",
         "_sink" : "For dummy notifications from selector",
    }
    Outboxes = {
         "outbox" : "",
         "signal" : "",
         "_toNotify"  : "Forwarding of messages to notify inbox of actual selector",
         "_toControl" : "Forwarding of messages to control inbox of actual selector",
    }

    def __init__(self):
        super(Selector, self).__init__()
        self.trackedby = None

    
    def trackedBy(self, tracker):
        self.trackedby = tracker

    def main(self):
        self.notifySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.notifySocket.setblocking(False)
        self.notifySocket.bind(("127.0.0.1",1678))
        self.notifySocket.connect(("127.0.0.1",1678))
        
        self.selector =  _SelectorCore(self.notifySocket)
        self.addChildren(self.selector)
        self.selector.activate()
        self.link((self,"_toNotify"),(self.selector, "notify"))
        self.link((self,"_toControl"),(self.selector, "control"))

#        self.send( newReader( (self,"_sink"), self.notifySocket), "_toNotify")

        shutdownMessage = shutdown()
        
        while not self.childrenDone():
            if not self.anyReady():
                self.pause()
            yield 1
            
            wakeSelector=False
            
            while self.dataReady("notify"):
                message=self.recv("notify")
                self.send(message, "_toNotify")
                wakeSelector=True
            
            while self.dataReady("control"):
                message = self.recv("control")
                if isinstance(message,shutdown):
                   if self.trackedby is not None:
#                       print "we are indeed tracked"
                       self.trackedby.deRegisterService("selector")
                       self.trackedby.deRegisterService("selectorshutdown")
                       self.send(message, "_toControl")
                       shutdownMessage=message
                       wakeSelector=True

            if wakeSelector:
                self.notifySocket.send("X")


        self.send(shutdownMessage, "signal")

    def childrenDone(self):
        """Unplugs any children that have terminated, and returns true if there are no
           running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())
    
    def setSelectorServices(selector, tracker = None):
        """\
        Sets the given selector as the service for the selected tracker or the
        default one.

        (static method)
        """
        if not tracker:
            tracker = cat.coordinatingassistanttracker.getcat()
        tracker.registerService("selector", selector, "notify")
        tracker.registerService("selectorshutdown", selector, "control")
        selector.trackedBy(tracker)
    setSelectorServices = staticmethod(setSelectorServices)

    def getSelectorServices(tracker=None): # STATIC METHOD
      """\
      Returns any live selector registered with the specified (or default) tracker,
      or creates one for the system to use.

      (static method)
      """
      if tracker is None:
         tracker = cat.coordinatingassistanttracker.getcat()
      try:
         service = tracker.retrieveService("selector")
         shutdownservice = tracker.retrieveService("selectorshutdown")
         return service, shutdownservice, None
      except KeyError:
         selector = Selector()
         Selector.setSelectorServices(selector, tracker)
         service=(selector,"notify")
         shutdownservice=(selector,"control")
         return service, shutdownservice, selector
    getSelectorServices = staticmethod(getSelectorServices)


__kamaelia_components__  = ( Selector, )
