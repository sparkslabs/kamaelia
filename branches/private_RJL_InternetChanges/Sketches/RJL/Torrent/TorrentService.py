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

# You should NOT be using/importing TorrentService unless you are working on
# modifying Kamaelia's BitTorrent functionality. It's sole purpose is as a
# dependency of TorrentPatron!

import Axon
from Axon.Ipc import shutdown
import Axon.CoordinatingAssistantTracker as cat
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent

from TorrentClient import TorrentClient
from TorrentIPC import *
                
"""\
=================
TorrentService - a service that co-ordinates the sharing of a single BitTorrent Client
=================

This component shares a single TorrentClient between several TorrentPatrons.

Generally, you should not create a TorrentService yourself. If one is needed, one will
be created by TorrentPatron. If a TorrentService already exists, creating one yourself
may crash Python (see the effects of creating two TorrentClient components in
TorrentClient.py)

"""

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
        """Registers a TorrentPatron with this service, creating an outbox connected to it"""
        
        print "Adding client!"
        print replyService
        particularOutbox = self.addOutbox("clientoutbox")
        self.link((self, particularOutbox), replyService)
        self.outboxFor[replyService] = particularOutbox;
        
    def removeClient(self, replyTo, replyInbox):
        """Deregisters a TorrentPatron with this service, deleting its outbox"""
            
        particularOutbox = self.outboxFor[replyService]
        self.unlink((self, particularOutbox), replyService)
        self.deleteOutbox(particularoutbox)

    def sendToClient(self, msg, replyService):    
        """Send a message to a TorrentPatron"""
        self.send(msg, self.outboxFor[replyService])

    def main(self):
        """Main loop"""    
        while 1:
            print "TorrentService main loop"
            yield 1
            while self.dataReady("notify"):
                message = self.recv("notify")
                print "NOTIFY"
                print message
                if isinstance(message, TIPCServiceAdd):
                    self.addClient(message.replyService)
                elif isinstance(message, TIPCServiceRemove):
                    self.removeClient(message.replyService)
                elif isinstance(message, TIPCServicePassOn):
                    replyService = message.replyService
                    message = message.message
                    #Requests to TorrentClient
                    if isinstance(message, TIPCCreateNewTorrent) or isinstance(message, str):
                        self.pendingAdd.append(replyService)
                        self.send(message, "outbox")
                    else:
                        self.send(message, "outbox")

            while self.dataReady("inbox"):
                message = self.recv("inbox")
                print "INBOX"
                print message                
                if isinstance(message, TIPCNewTorrentCreated):
                    replyService = self.pendingAdd.pop(0)
                    self.torrentBelongsTo[message.torrentid] = replyService
                    self.sendToClient(message, replyService)
                elif isinstance(message, TIPCTorrentAlreadyDownloading) or isinstance(message, TIPCTorrentStartFail):
                    replyService = self.pendingAdd.pop(0)            
                    self.sendToClient(message, replyService)                
                elif isinstance(message, TIPCTorrentStatusUpdate):
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
        Sets the given TorrentService as the service for the selected tracker or the
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

__kamaelia_components__  = ( TorrentService, )

