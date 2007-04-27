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
=========================================
GUI for Ryans Lothians Bittorrent Package
=========================================

A 3D GUI for bittorrent downloading using Ryan Lothians Kamaelia
Bittorrent package. Features torrent fetching from URLs,
starting/stopping of torrents and showing torrent information.

To work properly, an installation of Bittorrent 4.20.8 or higher is
required.
"""

import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Kamaelia.UI.OpenGL.Vector import Vector
from Kamaelia.UI.OpenGL.Button import Button
from Kamaelia.UI.OpenGL.ArrowButton import ArrowButton
from Kamaelia.UI.OpenGL.ProgressBar import ProgressBar
from Kamaelia.UI.OpenGL.Container import Container
from Kamaelia.UI.OpenGL.SkyGrassBackground import SkyGrassBackground
from Kamaelia.UI.OpenGL.Label import Label
from Kamaelia.UI.OpenGL.PygameWrapper import PygameWrapper
from Kamaelia.UI.OpenGL.Movement import WheelMover, PathMover, LinearPath

from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.Protocol.Torrent.TorrentIPC import *

from BitTorrent.bencode import bdecode

import random
import os
import time
import sys

class TorrentOpenGLGUI(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Inboxes = {
        "inbox":"Receive messages from TorrentPatron",
        "control":"receive shutdown messages",
        
        "nav":"To receive commands from navigation buttons",

        "start": "Start commands from buttons",
        "stop": "Stop commands from buttons",

        "show_info": "Info commands from buttons",
        "hide_info": "Hide torrent info",

        "torrent_url": "For reception of torrent file URLs",
        "torrent_file": "For reception of torrent files",
    }
    
    Outboxes = {
        "outbox":"Send Messages to TorrentPatron",
        "signal" : "",

        "fetcher" : "Send URLs to SimpleHttpClient",

        "mover_signal": "Send command to WheelMover",
        "mover_switch": "Control WheelMover",
        
        "infomover_commands": "Send commands to info container mover",
        "torrent_info": "For sending info about a torrent"
    }
    
    
    def __init__(self, **argd):
        super(TorrentOpenGLGUI, self).__init__()
        
        self.torrents = []
        self.torrent_from_id = {}
        self.torrent_to_id = {}
        self.torrent_progress_comms = {}
        
        self.requested_files = []
        self.started_torrents = []
        
        
    def main(self):
        self.initUIComponents()        
        self.loadLocalTorrentFiles()
        
        while 1:
            yield 1
            
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
#                print msg
                
                if isinstance(msg, TIPCNewTorrentCreated):
                    torrent = self.started_torrents.pop(0)
                    self.torrent_from_id[msg.torrentid] = torrent
                    self.torrent_to_id[torrent] = msg.torrentid
                                        
                elif isinstance(msg, TIPCTorrentStartFail) or isinstance(msg, TIPCTorrentAlreadyDownloading):
                    self.started_torrents.pop(0)
                
                elif isinstance(msg, TIPCTorrentStatusUpdate):
                    self.send(msg.statsdictionary.get("fractionDone","0"), self.torrent_progress_comms[ self.torrent_from_id[msg.torrentid]] )

            while self.dataReady("torrent_url"):
                url = self.recv("torrent_url")
                filename = os.path.basename(url)
                self.requested_files.append(filename)
                self.send(url, "fetcher")

            while self.dataReady("torrent_file"):
                torrentfile = self.recv("torrent_file")
                # save received file
                filename = self.requested_files.pop()
                fobj = open(os.getcwd()+"/"+filename, 'w')
                fobj.write(torrentfile)
                fobj.close()
                # add torrent
                self.addTorrent(filename, torrentfile)                

            while self.dataReady("nav"):
                msg = self.recv("nav")
                if msg == "UP":
                    self.send("NEXT", "mover_switch")
                if msg == "DOWN":
                    self.send("PREVIOUS", "mover_switch")
                
            while self.dataReady("start"):
                torrent = self.recv("start")
                self.send(torrent)
                self.started_torrents.append(torrent)
                
            while self.dataReady("stop"):
                torrent = self.recv("stop")
                try:
                    self.send( TIPCCloseTorrent(torrentid=self.torrent_to_id[torrent]) )
                    self.send(0.0, self.torrent_progress_comms[torrent])
                except KeyError:
                    pass
                
            while self.dataReady("show_info"):
                torrent = self.recv("show_info")
                self.showInfo(torrent)

            while self.dataReady("hide_info"):
                msg = self.recv("hide_info")
                self.hideInfo()
            
            while self.dataReady("control"):
                cmsg = self.recv("control")
                if isinstance(cmsg, Axon.Ipc.shutdownMicroprocess):
                    # dirty way to terminate program
                    sys.exit(0)


    def initUIComponents(self):
        # listen to shutdown events
        ogl_display = OpenGLDisplay().getDisplayService()[0]
        self.link( (ogl_display, "signal"), (self, "control") )
        
        # init mover
        self.mover = WheelMover(radius=15, center=(0,0,-25), steps=500, slots=40).activate()
        self.link( (self, "mover_signal"), (self.mover, "notify") )
        self.link( (self, "mover_switch"), (self.mover, "switch") )

        self.background = SkyGrassBackground(size=(5000,5000,0), position=(0,0,-90)).activate()
        
        # create & link nav buttons
        self.up_button = ArrowButton(size=(1,1,0.3), position=(7,5,-15), msg="UP").activate()
        self.down_button = ArrowButton(size=(1,1,0.3), position=(7,-5,-15), rotation=(0,0,180), msg="DOWN").activate()
        self.link( (self.up_button, "outbox"), (self, "nav") )
        self.link( (self.down_button, "outbox"), (self, "nav") )
        
        # init info display
        self.infoticker = Ticker(text_height=21, render_right=250, render_bottom=500, background_colour=(250,250,200), text_colour=(0,0,0), outline_colour=(255,255,255)).activate()
        self.tickerwrapper = PygameWrapper(wrap=self.infoticker, size=(2.4,4.0,0.3)).activate()
        self.hideinfo_button = Button(caption="Hide", fontsize=30).activate()
        
        infocontents = {
            self.tickerwrapper : { "position":(0,0,0) },
            self.hideinfo_button : { "position":(0,-2.4,0) },
        }
        
        self.infocontainer = Container(contents=infocontents, position=(-10, 10, -16)).activate()
        infopath = LinearPath([(-10, 10, -16), (-3,0,-8)], 100)
        
        self.infomover = PathMover(infopath, False).activate()
        
        self.link( (self.infomover, "outbox"), (self.infocontainer, "position") )
        self.link( (self, "infomover_commands"), (self.infomover, "inbox") )
        self.link( (self, "torrent_info"), (self.infoticker, "inbox") )
        self.link( (self.hideinfo_button, "outbox"), (self, "hide_info") )
        
        self.send("Stop", "infomover_commands")


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
        self.torrents.append(torrent)
    
        start = Button(size=(0.8,0.5,0.3), caption="Start", fontsize=35, msg=torrent).activate()
        info  = Button(size=(0.8,0.5,0.3), caption="Info", fontsize=35, msg=torrent).activate()
        stop = Button(size=(0.8,0.5,0.3), caption="Stop", fontsize=35, msg=torrent).activate()
        colour = [ int(random.randint(100,255)) for i in range(3) ]
        progress = ProgressBar(size=(3.2,0.5,0.3), barcolour=colour).activate()
        label = Label( size=(6.0, 0.3, 0.3), caption=title, fontsize=26, bgcolour=colour).activate()

        self.link( (start, "outbox"), (self, "start") )
        self.link( (stop, "outbox"), (self, "stop") )
        self.link( (info, "outbox"), (self, "show_info") )
        
        container_elements = {
            progress : { "position":(-0.4,-0.3,0) },
            start : { "position":(1.8,-0.3,0) },
            stop : { "position":(2.7,-0.3,0) },
            info : { "position":(3.6,-0.3,0) },
            label : { "position":(1, 0.3, 0) },
        }
    
        container = Container(contents=container_elements, position=(0,0,-10)).activate()
        
        req = { "APPEND_CONTROL":True,
                "objectid": id(container),
                "control": (container,"position")
        }
        self.send(req, "mover_signal")
        
        # create & link box for progress update
        progbox = self.addOutbox("progress")
        self.torrent_progress_comms[torrent] = progbox
        self.link( (self, progbox), (progress, "progress") )


    def showInfo(self, torrent):
        decoded = bdecode(torrent)
        
        info = decoded.get("info", None)
        if info is not None:
            name = info.get("name", "??")
            length = info.get("length", "??")

        date = decoded.get("creation date", "??")
        creator = decoded.get("created by", "??")
        announce = decoded.get("announce", "??")
        comment = decoded.get("comment", "??")
            
        infotuple = (name, comment, length, date, creator)
        
        infostring = "Name:%s\nComment:%s\nLength:%s\nCreation_Date:%s\nCreated_by:%s\n ----- \n" % infotuple
        
        # move info container in front of everthig
        self.send("Forward", "infomover_commands")
        self.send("Play", "infomover_commands")
        self.send(infostring, "torrent_info")
        
        
    def hideInfo(self):
        self.send("Backward", "infomover_commands")
        self.send("Play", "infomover_commands")
        
        
if __name__ == "__main__":
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleReader
    from Kamaelia.UI.PygameDisplay import PygameDisplay
    from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
    from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
    from Kamaelia.Protocol.Torrent.TorrentPatron import TorrentPatron
    
    ogl_display = OpenGLDisplay(limit_fps=100).activate()  
    OpenGLDisplay.setDisplayService(ogl_display)
    # override pygame display service
    PygameDisplay.setDisplayService(ogl_display)
    
    Graphline(
        reader = ConsoleReader(prompt="Enter torrent location:", eol=""),
        httpclient = SimpleHTTPClient(),
        gui = TorrentOpenGLGUI(),
        backend = TorrentPatron(),
        linkages = {
            ("gui", "outbox") : ("backend", "inbox"),
            ("reader", "outbox") : ("gui", "torrent_url"),
            ("gui", "fetcher") : ("httpclient", "inbox"),
            ("httpclient", "outbox") : ("gui", "torrent_file"),
            ("backend", "outbox"): ("gui", "inbox")
        }
    ).run()

# Licensed to the BBC under a Contributor Agreement: THF
