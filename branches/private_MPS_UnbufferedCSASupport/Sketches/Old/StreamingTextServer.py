#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#
# XXX TODO
#
# This could do with rewriting to utilise components such as PlugSplitter and/or
# Backplane.
#
# It could moved into Kamaelia/Examples - its basically a kind of plug server
# where a data source connects in, and multiple clients connect. If the data
# source goes down, teh clients don't notice, so it kinda "normalises" the
# connection from the clients' perspective.
#
# Of course, there is code specifically to do with subtitle data processing.
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Imports for streamingTextServer and streamingTextServerProtocol
from Axon.Component import component
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker
from Kamaelia.Util.Splitter import PlugSplitter as Splitter
import Kamaelia.Util.Splitter 

#imports for streamingTextServer
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.SimpleServerComponent import SimpleServer

#imports for streamingTextServerProtocol
from Axon.Ipc import producerFinished, newComponent
from SubtitleFilterComponent import SubtitleFilterComponent

#imports for main()
from Axon.Scheduler import scheduler

#imports for streamingTextReceiverProtocol
from Axon.AxonExceptions import ServiceAlreadyExists
from Kamaelia.KamaeliaIPC import socketShutdown

class streamingTextServer(component):
    """This server is set to receive a text stream from a single source only on
    port 1400 and serve this stream live to all clients connected on port 1500.
    There is virtually no work done in this class at all apart from setup.
   
    This may be replaceable with a graph object."""
    def __init__(self):
        super( streamingTextServer,  self).__init__()
        
    def initialiseComponent(self):
        """Setting up all the components and activating them.  Also registers
        the splitter with the CoordinatingAssistantTracker.
        
        Would be better to rewrite so that instead of activating directly the
        new components would be returned in a newComponents object.  At the
        moment the returned values are just ignored."""
#        testfile = "/usr/share/doc/packages/subversion/html/svn-book.html"
#        rfa = ReadFileAdaptor(filename = testfile, readsize = 5, steptime = 1.5).activate()
#        rfa = ReadFileAdaptor(command = "netcat -l -p 1400")
        splitter = Splitter().activate()
#        self.link((rfa,"outbox"),(splitter, "inbox"))
        str = SimpleServer(protocol=streamingTextReceiverProtocol, port=1400).activate()
        cat = coordinatingassistanttracker.getcat()
        cat.registerService("thesource", splitter, "configuration")
        cat.registerService("thesink", splitter, "inbox")
        ss = SimpleServer(protocol=streamingTextServerProtocol, port=1500).activate()
#        self.addChildren(rfa,splitter, ss)
        self.addChildren(str,splitter, ss)
#        return rfa, ss, splitter
        return str, ss, splitter
        
    def mainBody(self):
         """This class is solely to join the other components together and set
         them up which is handled in the initialiseComponent method.  Nothing
         needs to happen here."""
         self.pause
         return 1
    
class streamingTextServerProtocol(component):
    """The protocol component for streaming text server.  Looks in the
    CoordinatingAssistantTracker to find the splitter to connect to."""
    Inboxes=["inbox", "control"]
    Outboxes=["splittercontrol","outbox", "signal"]
    def __init__(self):
        super(streamingTextServerProtocol, self).__init__()
        
    
    def initialiseComponent(self):
        """Finds the splitter and connects to it and passes the data through the
        SubtitleFilterComponent to produce the right output which is passed out
        of the outbox to be sent to the client.
        
        Note:  The Filtering should be moved to the input so that it only has to
        be done once.""" 
        cat = coordinatingassistanttracker.getcat()
        # Find the splitter.
        self.splitter,self.splitterbox = cat.retrieveService("thesource")
        self.link((self, "splittercontrol"),(self.splitter,self.splitterbox))
        # Why is the filter here?  It should be in the receiver so that it only
        # gets done only once instead of once/client.  DOHHH!
        self.filter = SubtitleFilterComponent()
        self.link((self.filter, "outbox"), (self, "outbox"),passthrough = 2)
        self.send(Kamaelia.Util.Splitter.addsink(self.filter, "inbox"),"splittercontrol")
        return newComponent(self.filter)
    
    def mainBody(self):
        """Just has to handle the control to finish on request and to handle data
        on the inbox although this is just dropped to prevent buildup.
        """
        self.pause()
        if self.dataReady("control"):
            data = self.recv("control")
            self.send(data,"signal")
            if isinstance(data, producerFinished):
                return 0
        if self.dataReady("inbox"):
            self.recv() # Do nothing with the data but don't let it build up either.
        return 1
      
    def closeDownComponent(self):
        """Removes output from the splitter.
        """
        self.send(Kamaelia.Util.Splitter.removesink(self, "splittercontrol"))

class streamingTextReceiverProtocol(component):
    """This is a single server designed to be connected to by only a single
    client.  It could probably be transformed into using the SingleServer
    component.
    
    At the moment when it is spawned by the SimpleServer it
    registers itself with the CoordinatingAssistantTracker to stop others
    running and to find out if another is already running.  It also uses the
    CoordinatingAssistantTracker to find where to send the data.
    """
    def initialiseComponent(self):
        self.cat = coordinatingassistanttracker.getcat()
        self.isactivereceiver = False
        try:
            self.cat.registerService("streamingtextreceiver", self, "inbox")
        except ServiceAlreadyExists: # There is already a connected client sending data.
            self.send(socketShutdown(),"signal")
            return 0
        self.isactivereceiver = True
        # Find the splitter and passthrough link to it.
        self.splitter, self.splitterbox = self.cat.retrieveService("thesink")
        self.link((self, "inbox"),(self.splitter, self.splitterbox), passthrough=1)
        
    def mainBody(self):
        """If it isn't the only reciever it should shutdown immediately
        otherwise apart from waiting for shutdown messages it does nothing as
        the data is passed straight through without processing."""
        if not self.isactivereceiver:
            return 0
        if self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, producerFinished):
                return 0
#        if self.dataReady():
#            print self.recv()
        return 1
    
    def closeDownComponent(self):
        """Removes the service from the CoordinatingAssistantTracker so that a
        new protocol handler can be started if another client connects."""
        if self.isactivereceiver:
            self.cat.deRegisterService("streamingtextreceiver")

class textStreamer:
    pass
    
def main():
    streamingTextServer().activate()
    scheduler.run.runThreads()
    
if __name__==__name__:
    main()
    
