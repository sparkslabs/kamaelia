#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
=====================
GUI for Ryans Bittorrent Package
=====================
TODO
"""

import sys
sys.path.append("../../Kamaelia/UI/OpenGL/")


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Util3D import *
from OpenGLComponent import *

from Button import Button
from ArrowButton import ArrowButton
from SimpleButton import SimpleButton
from ProgressBar import ProgressBar
from Container import Container
from SkyGrassBackground import SkyGrassBackground
from Movement import WheelMover
from Label import Label

import random
import os


class TorrentOpenGLGUI(Axon.Component.component):
    Inboxes = {
        "inbox":"not used",
        "control":"not used",
        "button":"To receive commands from buttons",
        "torrent_delivery": "for reception of torrent files",
    }
    
    Outboxes = {
        "outbox":"",
        "signal" : "",
        "fetcher" : "",
        "fetchersignal" : "",
        "mover_signal": "",
        "mover_switch": "",
    }
    
    
    def __init__(self, **argd):
        super(TorrentOpenGLGUI, self).__init__()
        
        
    def main(self):
        self.mover = WheelMover(radius=15, center=(0,0,-25), steps=500, slots=40).activate()
        self.link( (self, "mover_signal"), (self.mover, "notify") )
        self.link( (self, "mover_switch"), (self.mover, "switch") )

        self.background = SkyGrassBackground(size=(5000,5000,0), position=(0,0,-90)).activate()
        
        self.up_button = ArrowButton(size=(1,1,0.3), position=(7,5,-15), msg="UP").activate()
        self.down_button = ArrowButton(size=(1,1,0.3), position=(7,-5,-15), rotation=(0,0,180), msg="DOWN").activate()
        
        self.link( (self.up_button, "outbox"), (self, "button") )
        self.link( (self.down_button, "outbox"), (self, "button") )
        
        self.loadLocalTorrentFiles()
        
        while 1:
            
            if self.dataReady("button"):
                msg = self.recv("button")
                if msg == "UP":
                    self.send("NEXT", "mover_switch")
                if msg == "DOWN":
                    self.send("PREVIOUS", "mover_switch")
                if msg == "ADD":
                    self.addTorrent("Test")
                    
            if self.dataReady("torrent_delivery"):
                torrent = self.recv("torrent_delivery")
                
                    
            yield 1


    def loadLocalTorrentFiles(self):
        print "Loading local torrent files..."
        cwd = os.getcwd()
        files = os.listdir(cwd)
        for f in files:
            if f.endswith(".torrent"):
                print "- ",f
                fobj = open(f)
                torrent = fobj.read() 
                fobj.close()
                self.addTorrent(f, torrent)
                

    def addTorrent(self, title, torrent):
        start = Button(size=(0.9,0.5,0.3), caption="Start", msg=torrent).activate()
        info  = Button(size=(0.9,0.5,0.3), caption="Info", msg="Info").activate()
        progress = ProgressBar(size=(3,0.5,0.3)).activate()
        colour = [int(random.randint(100,255)) for i in range(3) ]
        label = Label( size=(5.4, 0.3, 0.3), caption=title, fontsize=26, bgcolour=colour).activate()
        
        container_elements = {
            progress : { "position":(-1.2,-0.3,0) },
            start : { "position":(1.1,-0.3,0) },
            info : { "position":(2.3,-0.3,0) },
            label : { "position":(0, 0.3, 0) },
        }
    
        container = Container(contents=container_elements, position=(0,0,-10)).activate()
        
        req = { "APPEND_CONTROL":True,
                "objectid": id(container),
                "control": (container,"position")
        }
        self.send(req, "mover_signal")
        
        
    def getTorrentName(self, torrent):
        if torrent.find("name") != -1:
            pass
        else:
            return "Unknown Name"
        
        
if __name__ == "__main__":
    from Kamaelia.Chassis.Graphline import Graphline
    import sys
    sys.path.append("../HTTP")

    from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
    from Kamaelia.Util.Console import ConsoleReader
    from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron
    from Kamaelia.Community.RJL.Kamaelia.Protocol.Torrent.TorrentIPC import TIPCNewTorrentCreated, TIPCTorrentStartFail, TIPCTorrentAlreadyDownloading, TIPCTorrentStatusUpdate
    
    Graphline(
        reader = ConsoleReader(prompt="Enter torrent location:"),
        gui = TorrentOpenGLGUI(),
        httpclient = SimpleHTTPClient(),
        backend = TorrentPatron(),
        linkages = {
            ("gui", "outbox") : ("backend", "inbox"),
            ("gui", "fetchersignal") : ("httpclient", "control"),
            ("gui", "signal") : ("backend", "control"),
            ("reader", "outbox") : ("httpclient", "inbox"),
            ("httpclient", "outbox") : ("gui", "torrent_delivery"),
            ("backend", "outbox"): ("gui", "inbox")
        }
    ).run()
        
    
    Axon.Scheduler.scheduler.run.runThreads()  

