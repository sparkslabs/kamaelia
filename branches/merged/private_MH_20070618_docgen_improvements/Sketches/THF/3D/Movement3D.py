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

import Axon
from Util3D import Vector
from SimpleCube import SimpleCube
from math import *

# =========================
# Control3D contains movement commands
# =========================
class Control3D:
    POSITION, REL_POSITION, ROTATION, REL_ROTATION, SCALING, REL_SCALING = range(6)
    def __init__(self, type, amount):
        # Command types
        self.type = type
        self.amount = amount

# =========================
# Path3D generates a linear interpolated Path
# =========================
class LinearPath3D:
    def __init__(self, points = [], steps = 0):
        self.nextpoint = 0
    
        if steps == 0:
            steps = len(points)
        
        if steps == len(points):
            self.points = points
        else:
            totallen = 0.0
            p1 = points[0]
            for p2 in points[1:]:
                totallen += (p2-p1).length()
                p1=p2
#            print "totallen", totallen
            steplen = totallen/float(steps)
#            print steplen
            prelen = 0.0
            postlen = 0.0
            proclen = 0.0
            addedpoints = 0
            
            p1 = points[0]
            self.points = []
            for p2 in points[1:]:
                v = p2-p1
                vlen = v.length()
                postlen += vlen
#                print proclen
                while proclen <= postlen and addedpoints < steps:
                    self.points.append(p1+v*((proclen-prelen)/vlen))
                    proclen += steplen
                    addedpoints += 1
                prelen += vlen
                p1 = p2
            self.points.append(p2)
#        for v in self.points:print str(v)
#        print
            
    def __getitem__(self, key):
        return self.points[key]
        
    def __len__(self):
        return len(self.points)
        
    def next(self):
        v = self.points[self.nextpoint]
        self.nextpoint += 1
        if self.nextpoint == len(self.points): self.nextpoint = 0
        return v
    
    
# ==================================
# InterpolatedPath3D generates a hermitean interpolated Path
# ==================================
class InterpolatedPath3D:
    def __init__(self, points = [], steps = 0):
        pass
    
        
# =========================
# PathMover: moves a 3d object along a path
# =========================
class PathMover(Axon.Component.component):
    Inboxes = {
       "inbox": "Commands are received here",
       "control": "ignored",
    }
    
    Outboxes = {
        "outbox" : "Outbox for sending Control3D commands",
        "status": "Used to send status messages",
    }
    def __init__(self, path, repeat=True):
        super(PathMover, self).__init__()
        self.path = path
        self.repeat = repeat
        
        self.running = True
        self.currentIndex = 0
        self.lastIndex = 0
        self.flipped = False
        
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                if msg == "Play":
                    self.running = True
                if msg == "Stop":
                    self.running = False
                if msg == "Next":
                    self.currentIndex += 1
                if msg == "Previous":
                    self.currentIndex -= 1
                if msg == "Rewind":
                    if not self.flipped:
                        self.currentIndex = 0
                    else:
                        self.currentIndex = len(self.path)-1
                if msg == "Forward":
                    self.flipped = False
                if msg == "Backward":
                    self.flipped = True
            
            if self.running:
                if not self.flipped:
                    self.currentIndex += 1
                else:
                    self.currentIndex -= 1
                
            if self.currentIndex >= len(self.path):
                self.send("Finish", "status")
                if self.repeat:
                    self.currentIndex = 0
                else:
                    self.currentIndex -=1
                    self.running = False
            elif self.currentIndex < 0:
                self.send("Start", "status")
                if self.repeat:
                    self.currentIndex = len(self.path)-1
                else:
                    self.currentIndex = 0
                    self.running = False
                
            if self.currentIndex != self.lastIndex:
                self.send( Control3D(Control3D.POSITION, self.path[self.currentIndex].copy()), "outbox")
                self.lastIndex = self.currentIndex


class Rotator(Axon.Component.component):
    def main(self):
        while 1:
            yield 1
            self.send( Control3D(Control3D.REL_ROTATION, Vector(0.1, 0.1, 0.1)), "outbox")

class Mover(Axon.Component.component):
    def main(self):
        x,y,z = 3.0, 3.0, -20.0
        dx = -0.03
        dy = -0.03
        dz = -0.03
        while 1:
            yield 1
            self.send( Control3D(Control3D.POSITION, Vector(x, y, z)), "outbox")
            x +=dx
            y +=dy
            z +=dz
            if abs(x)>5: dx = -dx
            if abs(y)>5: dy = -dy
            if abs(z+20)>10: dz = -dz
#                print x, y, abs(x), abs(y)


import random

class Buzzer(Axon.Component.component):
    def main(self):
        r = 1.00
        f = 0.01
        while 1:
            yield 1
            if  r>1.0: f -= 0.001
            else: f += 0.001
            r += f
            
            self.send( Control3D(Control3D.SCALING, Vector(r, r, r)), "outbox")
    
        
if __name__=='__main__':
    path1 = LinearPath3D([Vector(3,3,-20), Vector(4,0,-20), Vector(3,-3,-20), Vector(0,-4,-20), Vector(-3,-3,-20),Vector(-4,0,-20),  Vector(-3,3,-20),Vector(0,4,-20),  Vector(3,3,-20)], 1000)
#    path2 = Path3D([Vector(1,0,0), Vector(0,0,0), Vector(0,1,0)], 9)

    cube = SimpleCube().activate()
    mover = PathMover(path1).activate()
    
    mover.link((mover,"outbox"), (cube,"control3d"))
    
    Axon.Scheduler.scheduler.run.runThreads()  
