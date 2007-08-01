#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: RJL

# You should NOT be using/importing TorrentService unless you are working on
# modifying Kamaelia's BitTorrent functionality. It's sole purpose is as a
# dependency of TorrentPatron!

"""\
==========================
BitTorrent Sharing Service
==========================

The TorrentService component provides a service that allows the sharing of
a single BitTorrent Client with more than one component that might want to use
it.

Use the TorrentPatron component to make use of BitTorrent through this service.

Generally, you should not create a TorrentService yourself. If one is needed, one will
be created by TorrentPatron. If a TorrentService already exists, creating one yourself
may crash Python (see the effects of creating two TorrentClient components in
TorrentClient.py)

The shutting down of this component (when it is no longer in use) is very ugly.



How does it work?
-----------------
This component forwards messages from TorrentPatrons to a single TorrentClient
it creates and also delivers responses from TorrentClient to the TorrentPatron
appropriate to the response content.

TorrentClient handles new torrent requests sequentially, so as long as we keep a 
record of what order the requests of TorrentPatrons were forwarded, we can work
out who to send TorrentClient's response to. Then, since all further messages are
assigned a torrentid by TorrentClient, we can route all messages labelled with a
particular id to to the TorrentPatron that started that torrent.
"""

import Axon.CoordinatingAssistantTracker as cat

from Axon.Ipc import shutdown, producerFinished
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent

from Kamaelia.Protocol.Torrent.TorrentClient import TorrentClient
from Kamaelia.Protocol.Torrent.TorrentIPC import *

class TorrentService(AdaptiveCommsComponent):
    """\
    TorrentService() -> new TorrentService component

    Use TorrentService.getTorrentService(...) in preference as it returns an
    existing instance, or automatically creates a new one.
    """
    Inboxes = {
        "control" : "Recieving a Axon.Ipc.shutdown() message here causes shutdown",
        "inbox"   : "Connects to TorrentClient (the BitTorrent code)",
        "notify"  : "Used to be notified about things to select",
        "_torrentcontrol" : "Notice that TorrentClient has shutdown"
    }
    Outboxes = {
        "signal"   : "Not used",
        "outbox"   : "Connects to TorrentClient (the BitTorrent code)",
        "debug"    : "Information that may aid debugging"
    }
    
    def debug(self, msg):
        self.send(msg, "debug")
        
    def __init__(self):
        super(TorrentService, self).__init__()
        
        self.debug("Torrent service init")
                
        self.outboxFor = {}
        self.torrentBelongsTo = {}
        self.pendingAdd = []
        
        self.initTorrentClient()
        self.myclients = 0
        
    def initTorrentClient(self):
        self.handler = TorrentClient()
        self.addChildren(self.handler)
        self.link((self, "outbox"), (self.handler, "inbox"))
        self.link((self, "signal"), (self.handler, "control"))
        self.link((self.handler, "outbox"), (self, "inbox"))        
        self.link((self.handler, "signal"), (self, "_torrentcontrol"))
        
        self.handler.activate()
    
    def addClient(self, replyService):
        """Registers a TorrentPatron with this service, creating an outbox connected to it"""
        
        self.debug("Adding client!")
        self.debug(replyService)
        
        self.myclients += 1
        particularOutbox = self.addOutbox("clientoutbox")
        self.link((self, particularOutbox), replyService)
        self.outboxFor[replyService] = particularOutbox;
        
    def removeClient(self, replyService):
        """Deregisters a TorrentPatron with this service, deleting its outbox"""

        self.myclients -= 1            
        particularOutbox = self.outboxFor[replyService]
        self.unlink((self, particularOutbox), replyService)
        #self.deleteOutbox(particularOutbox) WHY NOT

    def sendToClient(self, msg, replyService):    
        """Send a message to a TorrentPatron"""
        self.send(msg, self.outboxFor[replyService])

    def main(self):
        """Main loop"""
        while 1:
            #print "TorrentService main loop"
            yield 1
            while self.dataReady("notify"):
                message = self.recv("notify")
                self.debug("NOTIFY")
                self.debug(message)
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
                self.debug("INBOX")
                self.debug(message)
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
                    self.debug("Unknown message to TorrentService from TorrentClient!\n")
                    self.debug(message)

            while self.dataReady("control"):
                message = self.recv("control")
                self.debug("CONTROL")
                self.debug(message)
                if isinstance(message, shutdown):
                    return
                    
            if self.myclients == 0:
                self.send(shutdown(), "signal")
                torrentclientfinished = False
                while not torrentclientfinished:
                    yield 1            
                    while self.dataReady("_torrentcontrol"):
                        msg = self.recv("_torrentcontrol")
                        if isinstance(msg, producerFinished):
                            torrentclientfinished = True
                            yield 1
                            break
                    self.pause()
                
                if not self.dataReady("notify"):
                    TorrentService.endTorrentServices()
                else:
                    #whoops we need to start again doh!
                    initTorrentClient()
                    
            self.pause()                
        
        
        
    def endTorrentServices(tracker = None): # STATIC METHOD
        if not tracker:
            tracker = cat.coordinatingassistanttracker.getcat()
        tracker.deRegisterService("torrentsrv")
        tracker.deRegisterService("torrentsrvshutdown")
    endTorrentServices = staticmethod(endTorrentServices) 
    
    def setTorrentServices(torrentsrv, tracker = None): # STATIC METHOD
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
         #print "Gonna return"
         #print (service, shutdownservice, torrentsrv)
         return service, shutdownservice, torrentsrv
    getTorrentServices = staticmethod(getTorrentServices)

__kamaelia_components__  = ( TorrentService, )
