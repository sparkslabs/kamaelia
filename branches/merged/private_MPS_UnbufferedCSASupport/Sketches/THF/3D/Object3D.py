#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
General 3D Object
=====================
TODO
"""


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Display3D import Display3D
from Util3D import *
import Axon

class Object3D(Axon.Component.component):
    Inboxes = {
       "inbox": "not used",
       "control": "ignored",
       "3dcontrol":"receive 3d movement commands here (rel_)?[position | rotation]",
    }
    
    Outboxes = {
        "outbox": "used for sending position information",
        "display_signal" : "Outbox used for communicating to the display surface"
    }
    
    def __init__(self, **argd):
        super(Object3D, self).__init__()
        # not sure about the needed data yet, just for testing
#       self.rotspeed = Vector(0.1, 0.0, 0.0)
        self.size = argd.get("size", Vector(2,2,2))
        self.pos = argd.get("pos",Vector(0,0,-15))
        self.rot = Vector(0.0,0.0,0.0)
        self.transform = Transform()
        
        self.name = argd.get("name", "nameless")
        self.grabbed = 0
        self.oldrot = self.rot.copy()
        self.oldpos = self.pos.copy()

        # prepare vertices for intersection test
        x = float(self.size.x/2)
        y = float(self.size.y/2)
        z = float(self.size.z/2)
        self.vertices = [ Vector(x, 0.0, 0.0), Vector(0.0, y, 0.0), Vector(0.0, 0.0, z) ]
        
        # similar to Pygame component registration
        self.disprequest = { "3DDISPLAYREQUEST" : True,
#                                          "callback" : (self,"callback"),
                                          "events" : (self, "inbox"),
#                                          "size": self.size,
#                                          "pos": self.pos,
                                          "object": self }
                                          

    # Ray intersection test
    # returns the distance of the origin o to the point of intersection
    # if no intersection occurs, 0 is returned
    # Algorithm from "Realtime Rendering"
    def intersectRay(self, o, d):
        transformed = [self.transform.transformVector(v) for v in self.vertices]
        tmin = -10000
        tmax = 10000
           
        p = self.pos-o
        halfwidths = [self.size.x/2, self.size.y/2, self.size.z/2]
        for i in range(3):
            a = transformed[i]-p
            h = halfwidths[i]
            e = a.dot(p)
            f = a.dot(d)
            if abs(f)>0.0001:
                t1 = (e+h)/f
                t2 = (e-h)/f
                if t1 > t2:
                    x = t1
                    t1 = t2
                    t2 = x
                if t1 > tmin: tmin = t1
                if t2 < tmax: tmax = t2
                if tmin > tmax: return 0
                if tmax < 0: return 0
            elif -e-h > 0 or -e+h < 0: return 0
        if tmin > 0: return tmin
        else: return tmax


    def applyTransforms(self):
        # generate transformation matrix
        self.transform.reset()
        self.transform.applyRotation(self.rot)
        self.transform.applyTranslation(self.pos)


    def draw(self):
        glMatrixMode(GL_MODELVIEW)

        # set generated matrix
        glPushMatrix()
        glLoadMatrixf(self.transform.getMatrix())

        # draw faces 
        glBegin(GL_QUADS)
        glColor4f(1.0,0.75,0.75,0.5)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(1.0,-1.0,1.0)

        glColor4f(0.75,1.0,0.75, 0.5)
        glVertex3f(1.0,1.0,-1.0)
        glVertex3f(1.0,-1.0,-1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0,1.0,-1.0)
        
        glColor4f(0.75,0.75,1.0, 0.5)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(1.0,-1.0,1.0)
        glVertex3f(1.0,-1.0,-1.0)
        glVertex3f(1.0,1.0,-1.0)

        glColor4f(1.0,0.75,1.0, 0.5)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0,1.0,-1.0)

        glColor4f(0.75,1.0,1.0, 0.5)
        glVertex3f(1.0,1.0,1.0)
        glVertex3f(-1.0,1.0,1.0)
        glVertex3f(-1.0,1.0,-1.0)
        glVertex3f(1.0,1.0,-1.0)

        glColor4f(1.0,1.0,0.75, 0.5)
        glVertex3f(1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(1.0,-1.0,-1.0)
        glEnd()

        glPopMatrix()
    
    
    def handleEvents(self):
        while self.dataReady("inbox"):
            for event in self.recv("inbox"):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in [1,3] and self.intersectRay(Vector(0,0,0), event.dir) > 0:
                        self.grabbed = event.button
                    if event.button == 4 and self.intersectRay(Vector(0,0,0), event.dir) > 0:
                        self.pos.z -= 1
                    if event.button == 5 and self.intersectRay(Vector(0,0,0), event.dir) > 0:
                        self.pos.z += 1
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button in [1,3]:
                        self.grabbed = 0
                if event.type == pygame.MOUSEMOTION:
                    if self.grabbed == 1:
                        self.rot.y += float(event.rel[0])
                        self.rot.x += float(event.rel[1])
                        self.rot %= 360
                    if self.grabbed == 3:
                        self.pos.x += float(event.rel[0])/10.0
                        self.pos.y -= float(event.rel[1])/10.0
                        
        if self.oldpos != self.pos:
            diff = self.pos-self.oldpos
            self.send("%s was moved by %s units\n" % (self.name, str(diff)) , "outbox",)
            self.oldpos = self.pos.copy()

        if self.oldrot != self.rot:
            diff = self.rot-self.oldrot
            self.send("%s was rotated by (%1.2f, %1.2f) degrees\n" % (self.name, diff.x, diff.y), "outbox",)
            self.oldrot = self.rot.copy()


    def handleMovementCommands(self):
        while self.dataReady("3dcontrol"):
            cmd = self.recv("3dcontrol")
            if cmd.type == "rotation":
                self.rot = cmd.value
            if cmd.type == "postition":
                self.pos = cmd.value
            if cmd.type == "rel_rotation":
                self.rot = (self.rot+cmd.value)%360
            if cmd.type == "rel_position":
                self.pos += cmd.value


    def main(self):
        displayservice = Display3D.getDisplayService()
        self.link((self,"display_signal"), displayservice)
        self.send(self.disprequest, "display_signal");

        while 1:

#            for _ in self.waitBox("callback"): yield 1
#            self.display = self.recv("callback")

# There is no need for a callback yet
            
            yield 1
            
            self.handleEvents()
            self.handleMovementCommands()
            self.applyTransforms()
            self.draw()

# Later it might be a good idea to provide a set of drawing functions
# so the component developer does not need to know about opengl
# This way opengl could later easily be replaced by an other mechanism
# for drawing
# e.g. TOGRA


if __name__=='__main__':
    class Bunch: pass
        
    class CubeRotator(Axon.Component.component):
        def main(self):
            while 1:
                yield 1
                cmd = Bunch()
                cmd.type = "rel_rotation"
                cmd.value = Vector(0.1, 0.1, 0.1)
                self.send(cmd, "outbox")

    class CubeMover(Axon.Component.component):
        def main(self):
            x,y,z = 3.0, 3.0, -20.0
            dx = -0.03
            dy = -0.03
            dz = -0.03
            while 1:
                yield 1
                cmd = Bunch()
                cmd.type = "postition" #
                cmd.value = Vector(x, y, z)
                self.send(cmd, "outbox")
                x +=dx
                y +=dy
                z +=dz
                if abs(x)>5: dx = -dx
                if abs(y)>5: dy = -dy
                if abs(z+20)>10: dz = -dz
                print x, y, abs(x), abs(y)

    
    from Kamaelia.Util.ConsoleEcho import consoleEchoer
    from Kamaelia.Util.Graphline import Graphline
    
    Graphline(
        CUBEC = Object3D(pos=Vector(0, 0,-12), name="Center cube"),
        CUBET = Object3D(pos=Vector(0,4,-20), name="Top cube"),
        CUBER = Object3D(pos=Vector(4,0,-22), name="Right cube"),
        CUBEB = Object3D(pos=Vector(0,-4,-18), name="Bottom cube"),
        CUBEL = Object3D(pos=Vector(-4, 0,-15), name="Left cube"),
        ROTATOR = CubeRotator(),
        MOVER = CubeMover(),
        ECHO = consoleEchoer(),
        linkages = {
            ("CUBEC", "outbox") : ("ECHO", "inbox"),
            ("CUBET", "outbox") : ("ECHO", "inbox"),
            ("CUBER", "outbox") : ("ECHO", "inbox"),
            ("CUBEB", "outbox") : ("ECHO", "inbox"),
            ("CUBEL", "outbox") : ("ECHO", "inbox"),
            ("ROTATOR", "outbox") : ("CUBEC", "3dcontrol"),
            ("MOVER", "outbox") : ("CUBEC", "3dcontrol"),
        } ).run()
        
    Axon.Scheduler.scheduler.run.runThreads()  
