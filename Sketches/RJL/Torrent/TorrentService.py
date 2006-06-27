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
import Axon.CoordinatingAssistantTracker as cat
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from btkam import TorrentClient, IPCNewTorrentCreated, IPCTorrentAlreadyDownloading, IPCTorrentStartFail, IPCTorrentStatusUpdate, IPCCreateNewTorrent, IPCCloseTorrent

class TSPassOn(object):
    def __init__(self, replyService, message):
        self.replyService = replyService
        self.message = message

class TSAdd(object):
    def __init__(self, replyService):
        self.replyService = replyService

class TSRemove(object):
    def __init__(self, replyService):
        self.replyService = replyService
        
                
class TorrentService(AdaptiveCommsComponent): #Axon.AdaptiveCommsComponent.AdaptiveCommsComponent): # SmokeTests_Selector.test_SmokeTest
    """\
    TorrentService() -> new TorrentService component

    Use TorrentService.getTorrentService(...) in preference as it returns an
    existing instance, or automatically creates a new one.
    """
    Inboxes = {
         "control" : "Recieving a Axon.Ipc.shutdown() message here causes shutdown",
         "inbox"   : "Connects to TorrentClient (the BitTorrent code)",
         "notify"  : "Used to be notified about things to select"
    }
    Outboxes = {
        "signal"   : "Not used",
        "outbox"   : "Connects to TorrentClient (the BitTorrent code)"
    }
    
    def __init__(self):
        print "Torrent service init"
        self.outboxFor = {}
        self.torrentBelongsTo = {}
        self.pendingAdd = []
        super(TorrentService, self).__init__()
        
        self.handler = TorrentClient()
        self.addChildren(self.handler)
        self.link((self, "outbox"), (self.handler, "inbox"))
        self.link((self.handler, "outbox"), (self, "inbox"))        
        
        self.handler.activate()
        
    def addClient(self, replyService):
        print "Adding client!"
        print replyService
        particularOutbox = self.addOutbox("clientoutbox")
        self.link((self, particularOutbox), replyService)
        self.outboxFor[replyService] = particularOutbox;
        
    def removeClient(self, replyTo, replyInbox):
        particularOutbox = self.outboxFor[replyService]
        self.unlink((self, particularOutbox), replyService)
        self.deleteOutbox(particularoutbox)

    def sendToClient(self, msg, replyService):
        self.send(msg, self.outboxFor[replyService])

    def main(self):
        while 1:
            print "TorrentService main loop"
            yield 1
            while self.dataReady("notify"):
                message = self.recv("notify")
                print "NOTIFY"
                print message
                if isinstance(message, TSAdd):
                    self.addClient(message.replyService)
                elif isinstance(message, TSRemove):
                    self.removeClient(message.replyService)
                elif isinstance(message, TSPassOn):
                    replyService = message.replyService
                    message = message.message
                    #Requests to TorrentClient
                    if isinstance(message, IPCCreateNewTorrent) or isinstance(message, str):
                        self.pendingAdd.append(replyService)
                        self.send(message, "outbox")
                    else:
                        self.send(message, "outbox")

            while self.dataReady("inbox"):
                message = self.recv("inbox")
                print "INBOX"
                print message                
                if isinstance(message, IPCNewTorrentCreated):
                    replyService = self.pendingAdd.pop(0)
                    self.torrentBelongsTo[message.torrentid] = replyService
                    self.sendToClient(message, replyService)
                elif isinstance(message, IPCTorrentAlreadyDownloading) or isinstance(message, IPCTorrentStartFail):
                    replyService = self.pendingAdd.pop(0)            
                    self.sendToClient(message, replyService)                
                elif isinstance(message, IPCTorrentStatusUpdate):
                    replyService = self.torrentBelongsTo[message.torrentid]
                    self.sendToClient(message, replyService)
                else:
                    print "Unknown message to TorrentService from TorrentClient!\n"
                    print message

            while self.dataReady("control"):
                message = self.recv("control")
                print "CONTROL"
                print message                
                if isinstance(message, shutdown):
                    return
                    
            self.pause()
       
    def setTorrentServices(torrentsrv, tracker = None):
        """\
        Sets the given selector as the service for the selected tracker or the
        default one.

        (static method)
        """
        if not tracker:
            tracker = cat.coordinatingassistanttracker.getcat()
        tracker.registerService("torrentsrv", torrentsrv, "notify")
        tracker.registerService("torrentsrvshutdown", torrentsrv, "control")
    setTorrentServices = staticmethod(setTorrentServices)

    def getTorrentServices(tracker = None): # STATIC METHOD
      """\
      Returns any live TorrentService registered with the specified (or default) tracker,
      or creates one for the system to use.

      (static method)
      """
      if tracker is None:
         tracker = cat.coordinatingassistanttracker.getcat()
      try:
         service = tracker.retrieveService("torrentsrv")
         shutdownservice = tracker.retrieveService("torrentsrvshutdown")
         return service, shutdownservice, None
      except KeyError:
         torrentsrv = TorrentService()
         torrentsrv.setTorrentServices(torrentsrv, tracker)
         service = (torrentsrv, "notify")
         shutdownservice = (torrentsrv, "control")
         print "Gonna return"
         print (service, shutdownservice, torrentsrv)
         return service, shutdownservice, torrentsrv
    getTorrentServices = staticmethod(getTorrentServices)


class TorrentPatron(Axon.Component.component):
    Inboxes = {
        "inbox"          : "Commands for the TorrentClient",
        "torrent-inbox"  : "Received feedback from TorrentClient",
        "control"        : "Shut me down"
    }
                 
    Outboxes = {
        "outbox"         : "Forward feedback from TorrentClient out of",
        "torrent-outbox" : "Talk to TorrentClient with",
        "signal"         : "Unused"
    }
                 
                
    def main(self):
        torrentService, torrentShutdownService, newTorrentService = TorrentService.getTorrentServices(self.tracker)
        if newTorrentService:
            newTorrentService.activate()
            self.addChildren(newTorrentService)

        self.link((self, "torrent-outbox"), torrentService)
        self.send(TSAdd((self, "torrent-inbox")), "torrent-outbox")
        
        loop = True
        while loop:
            print "TorrentPatron.main loop"
            yield 1
            
            if self.dataReady("inbox"):
                print "TorrentPatron inbox"            
                msg = self.recv("inbox")
                msg = TSPassOn((self, "torrent-inbox"), msg)
                self.send(msg, "torrent-outbox")
                
            elif self.dataReady("torrent-inbox"):
                msg = self.recv("torrent-inbox")
                print "TorrentPatron torrent-inbox"
                print msg
                self.send(msg, "outbox")
                
            elif self.dataReady("control"):
                print "TorrentPatron control"            
                msg = self.recv("control")
                if isinstance(msg, shutdown):
                    break
                    
            else:
                self.pause()
            
            
        #unregister with the service
        self.send(TSRemove(self, "torrent-inbox"), "torrent-outbox")
        
__kamaelia_components__  = ( TorrentService, TorrentPatron, )

