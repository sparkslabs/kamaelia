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
from Movement import CircleMover


class TorrentOpenGLGUI(Axon.Component.component):
    Inboxes = {
        "inbox":"not used",
        "control":"not used",
        "button":"To receive commands from buttons",
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
        self.mover = CircleMover(radius=15, center=(0,0,-25), steps=2000, slots=40).activate()
        self.link( (self, "mover_signal"), (self.mover, "notify") )
        self.link( (self, "mover_switch"), (self.mover, "switch") )

        self.background = SkyGrassBackground(size=(5000,5000,0), position=(0,0,-90)).activate()
        
        self.up_button = ArrowButton(size=(1,1,0.3), position=(7,5,-15), msg="UP").activate()
        self.down_button = ArrowButton(size=(1,1,0.3), position=(7,-5,-15), rotation=(0,0,180), msg="DOWN").activate()
        self.add_button = SimpleButton(size=(1,1,0.3), position=(7,0,-15), msg="ADD").activate()
        
        self.link( (self.up_button, "outbox"), (self, "button") )
        self.link( (self.down_button, "outbox"), (self, "button") )
        self.link( (self.add_button, "outbox"), (self, "button") )
        
        self.addTorrent("Test")
        self.addTorrent("Test")
        self.addTorrent("Test")
        self.addTorrent("Test")
        
        while 1:
            
            if self.dataReady("button"):
                msg = self.recv("button")
                if msg == "UP":
                    self.send("NEXT", "mover_switch")
                if msg == "DOWN":
                    self.send("PREVIOUS", "mover_switch")
                if msg == "ADD":
                    self.addTorrent("Test")
                    
            yield 1


    def addTorrent(self, torrent):
        start = Button(size=(0.9,0.5,0.3), caption="Start", msg="Start").activate()
        info  = Button(size=(0.9,0.5,0.3), caption="Info", msg="Info").activate()
        progress = ProgressBar(size=(3,0.5,0.3)).activate()
        
        container_elements = {
            progress : { "position":(-1,0,0) },
            start : { "position":(1.3,0,0) },
            info : { "position":(2.5,0,0) },
        }
    
        container = Container(contents=container_elements, position=(0,0,-10)).activate()
        
        req = { "APPEND_CONTROL":True,
                "objectid": id(container),
                "control": (container,"position")
        }
        self.send(req, "mover_signal")
        
        
if __name__ == "__main__":
    from Kamaelia.Chassis.Graphline import Graphline
    import sys
    sys.path.append("../HTTP")

#    from HTTPClient import SimpleHTTPClient
    
    #Graphline(
        #gui=TorrentOpenGLGUI(),
        #httpclient=SimpleHTTPClient(),
        #backend=TorrentPatron(),
        #linkages = {
            #("gui", "outbox") : ("backend", "inbox"),
            #("gui", "fetchersignal") : ("httpclient", "control"),
            #("gui", "signal") : ("backend", "control"),
            #("gui", "fetcher") : ("httpclient", "inbox"),
            #("httpclient", "outbox") : ("backend", "inbox"),
            #("backend", "outbox"): ("gui", "inbox")
        #}
    #).run()
        
    TorrentOpenGLGUI().activate()
    
    Axon.Scheduler.scheduler.run.runThreads()  

