#!/usr/bin/env python
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

import Axon
from Axon.Ipc import shutdown
import select, socket
from Kamaelia.KamaeliaIPC import newReader, removeReader, newWriter, removeWriter, newExceptional, removeExceptional
import Axon.CoordinatingAssistantTracker as cat
from Axon.ThreadedComponent import threadedadaptivecommscomponent
import time
#import sys,traceback

READERS,WRITERS, EXCEPTIONALS = 0, 1, 2
FAILHARD = False
class Selector(threadedadaptivecommscomponent): #Axon.AdaptiveCommsComponent.AdaptiveCommsComponent): # SmokeTests_Selector.test_SmokeTest
    Inboxes = {
         "control" : "Recieving a Axon.Ipc.shutdown() message here causes shutdown",
         "inbox" : "Not used at present",
         "notify" : "Used to be notified about things to select"
    }
    def removeLinks(self, selectable, meta, selectables):
#        \
#print "removeLinks",selectable,meta,selectables
        try:
            replyService, outbox, Linkage = meta[selectable]
            self.unlink(thelinkage=Linkage)
            selectables.remove(selectable)
            self.deleteOutbox(outbox)
            del meta[selectable]
            Linkage = None
#            print "removed",selectable,"from meta:",meta
#            print "removed",selectable,"from selectables:",selectables
        except:
#            print "removeLinks error:\n", traceback.format_exc()
#            print "contents of meta:",meta
#            print "contents of selectables:",selectables
            pass

    def addLinks(self, replyService, selectable, meta, selectables, boxBase):
#        \
#print "addinks",selectable,meta,selectables,boxBase
        if selectable not in meta:
            outbox = self.addOutbox(boxBase)
            L = self.link((self, outbox), replyService)
            meta[selectable] = replyService, outbox, L
            selectables.append(selectable)
            return L
        else:
            return meta[selectable][2]

    def handleNotify(self, meta, readers,writers, exceptionals):
        while self.dataReady("notify"):
            message = self.recv("notify")
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
#                \
#print "remove reader..."
                selectable = message.object
                self.removeLinks(selectable, meta[READERS], readers)

            if isinstance(message, removeWriter):
#                \
#print "remove writer..."
                selectable = message.object
                self.removeLinks(selectable, meta[WRITERS], writers)

            if isinstance(message, removeExceptional):
#                \
#print "remove exceptional..."
                selectable = message.object
                self.removeLinks(selectable, meta[EXCEPTIONALS], exceptionals)

    def main(self):
        readers,writers, exceptionals = [],[], []
        selections = [readers,writers, exceptionals]
        meta = [ {}, {}, {} ]
        if not self.anyReady():
            self.sync()        # momentary pause-ish thing
        last = 0
        numberOfFailedSelectsDueToBadFileDescriptor = 0
        while 1: # SmokeTests_Selector.test_RunsForever
            if self.dataReady("control"):
                message = self.recv("control")
                if isinstance(message,shutdown):
                   return
            self.handleNotify(meta, readers,writers, exceptionals)
            if len(readers) + len(writers) + len(exceptionals) > 0:
#                print "IN HERE"
                try:
                    read_write_except = select.select(readers, writers, exceptionals,5) #0.05
#                    print ".",
                    numberOfFailedSelectsDueToBadFileDescriptor  = 0
                    
                    for i in xrange(3):
                        for selectable in read_write_except[i]:
#                            try:
                                replyService, outbox, linkage = meta[i][selectable]
                                self.send(selectable, outbox)
                                replyService, outbox, linkage = None, None, None
    
    #                            print "i",i
#                                \
#    print "auto removing..."
                                self.removeLinks(selectable, meta[i], selections[i])
    #                            print selections
    
#                            except KeyError, k:
#                                pass
                            
                except ValueError, e:
#                    print "value error",e
#                    print "readers=",readers
#                    print "writers=",writers
#                    print "exceptionals=",exceptionals
                    if FAILHARD:
                        raise e
                except socket.error, e:
#                    print "socket error",e
                    if e[0] == 9:
                        numberOfFailedSelectsDueToBadFileDescriptor +=1
                        if numberOfFailedSelectsDueToBadFileDescriptor > 1000:
                            # For the moment, we simply raise an exception.
                            # We could brute force our way through the list of descriptors
                            # to find the broken ones, and remove
                            raise e

                self.sync()
            elif not self.anyReady():
                #print "IN HERE"
                self.sync()        # momentary pause-ish thing
            else:
                print "HMM"


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
