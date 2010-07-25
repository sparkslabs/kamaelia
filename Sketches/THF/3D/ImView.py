#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------

import Axon
from os import *
from Util3D import *
from TexPlane import *
from Button3D import *
from Movement3D import *

class ImView(Axon.Component.component):
    Inboxes = {"inbox":"Receive commands from Buttons here",
                      "mover_in": "Receive status of path here",
                      "mover_out": "Receive status of path here",
                       "control": "",
                     }
                     
    Outboxes = {"outbox":"",
                          "mover_in": "Control Pathmover in",
                          "mover_out": "Control Pathmover out",
                        }
                        
    def __init__(self, path):
        super(ImView, self).__init__()
        self.path = path
        self.texplane_controls = []
        self.ready = 0
        self.current = 0
        
    def initialiseComponent(self):
        # look in path for images
        filelist = listdir(self.path)
        imlist = []
        print "Loaded images:"
        for f in filelist:
            fl = f.lower()
            if fl.endswith(".jpg") or fl.endswith(".png") or fl.endswith(".jpeg"):
                imlist.append(f)
                print " ",f
                
        # create Texplane for each image
        for im in imlist:
            tp = TexPlane(tex="".join((self.path,im)), pos = Vector(20,0,-20)).activate()
            self.texplane_controls.append( (tp, "control3d") )
            
        # create buttons
        b1 = Button3D(caption="<<", msg="Previous", pos=Vector(-3,-3,-9)).activate()    
        b1.link( (b1,"outbox"), (self, "inbox") )
        b2 = Button3D(caption=">>", msg="Next", pos=Vector(3,-3,-9)).activate()    
        b2.link( (b2,"outbox"), (self, "inbox") )
#        b3 = Button3D(caption="Close", msg="Close", pos=Vector(0,-3.5,-10)).activate()    
#        b3.link( (b3,"outbox"), (self, "inbox") )
            
        # create paths for movement
        path_in = LinearPath3D( points = [ Vector(20,0,-30), Vector(0,0,-10) ], steps=100 )
        path_out = LinearPath3D( points = [ Vector(0,0,-10), Vector(-20,0,-30) ], steps=100 )
        
        # create pathmovers
        mover_in = PathMover(path_in, repeat=False).activate()
        mover_in.link( (mover_in, "status"), (self, "mover_in") )
        self.link( (self, "mover_in"), (mover_in, "inbox") )
        self.mover_in_comms = (mover_in, "outbox")
        
        mover_out = PathMover(path_out, repeat=False).activate()
        mover_out.link( (mover_out, "status"), (self, "mover_out") )
        self.link( (self, "mover_out"), (mover_out, "inbox") )
        self.mover_out_comms = (mover_out, "outbox")

        # move first pic in front
        self.link( self.mover_in_comms, self.texplane_controls[self.current])
        
        return 1
    
    def mainBody(self):
        # check status of paths
        while self.dataReady("mover_in"):
            msg = self.recv("mover_in")
            if msg == "Finish" or msg=="Start":
                self.ready += 1
        while self.dataReady("mover_out"):
            msg = self.recv("mover_out")
            if msg == "Finish" or msg=="Start":
                self.ready += 1

        # check inbox for button commands
        while self.dataReady("inbox"):
            msg = self.recv("inbox")
#            print msg
#            print self.ready
            if msg == "Next" and self.ready == 2 and self.current+1 < len(self.texplane_controls):
                self.ready = 0
                self.link( self.mover_out_comms, self.texplane_controls[self.current])
                self.current += 1
                self.link( self.mover_in_comms, self.texplane_controls[self.current])
                self.send("Forward", "mover_in")
                self.send("Forward", "mover_out")
                self.send("Rewind", "mover_in")
                self.send("Rewind", "mover_out")
                self.send("Play", "mover_in")
                self.send("Play", "mover_out")
            elif msg == "Previous"  and self.ready == 2 and self.current>0:
                self.ready = 0
                self.link( self.mover_in_comms, self.texplane_controls[self.current])
                self.current -= 1
                self.link( self.mover_out_comms, self.texplane_controls[self.current])
                self.send("Backward", "mover_in")
                self.send("Backward", "mover_out")
                self.send("Rewind", "mover_in")
                self.send("Rewind", "mover_out")
                self.send("Play", "mover_in")
                self.send("Play", "mover_out")
                
            elif msg == "Close":
                return False
    
        return True
    
    def closeDownComponent(self):
        return 1

if __name__ == '__main__':
    import sys
    try:
        path = sys.argv[1]
    except IndexError:
        path = "./"
    iv = ImView(path).activate()
    
    Axon.Scheduler.scheduler.run.runThreads()  
