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
General 3D Object
=====================
TODO
"""


from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, pygame.image
from pygame.locals import *
from Display3D import Display3D
from Util3D import *
import Axon

textures = [0,0]

class Control3D:
    POSITION, REL_POSITION, ROTATION, REL_ROTATION, SCALING, REL_SCALING = range(6)
    def __init__(self, type, amount):
        # Command types
        self.type = type
        self.amount = amount
                

class TexPlane(Axon.Component.component):
    Inboxes = {
       "inbox": "not used",
       "control": "ignored",
        # 3D control
#       "translation" : "receive 3D movement Vectors here"
#       "rotation": "receive 3D rotation Vectors here",
#       "scaling": "receive 3D scaling Vectors here",
#       "rel_translation" : "receive 3D movement Vectors here"
#       "rel_rotation": "receive 3D rotation Vectors here",
#       "rel_scaling": "receive 3D scaling Vectors here",

        "control3d": "receive Control3D commands here"
    }
    
    Outboxes = {
        "outbox": "not used",
        "display_signal" : "Outbox used for communicating to the display surface",
        # 3D status
        "position" : "send position status when updated",
        "rotation": "send rotation status when updated",
        "scaling": "send scaling status when updated"
    }
    
    def __init__(self, **argd):
        super(TexPlane, self).__init__()
        
        self.size = argd.get("size", Vector(2,2,2))
        self.pos = argd.get("pos",Vector(0,0,-15))
        self.rot = Vector(0.0,0.0,0.0)
        self.scaling = argd.get("scaling",Vector(1,1,1))
        self.transform = Transform()

        self.oldrot = Vector()
        self.oldpos = Vector()
        self.oldscaling = Vector()

        self.name = argd.get("name", "nameless")

        self.tex = argd.get("tex", None)

        self.grabbed = 0

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
        # generate new transformation matrix if needed
        if True:#self.oldscaling != self.scaling or self.oldrot != self.rot or self.oldpos != self.pos:
            self.transform.reset()
            self.transform.applyScaling(self.scaling)
            self.transform.applyRotation(self.rot)
            self.transform.applyTranslation(self.pos)

            if self.oldscaling != self.scaling:
                self.send(self.scaling, "scaling")
                self.oldscaling = self.scaling.copy()

            if self.oldrot != self.rot:
                self.send(self.rot, "rotation")
                self.oldrot = self.rot.copy()

            if self.oldpos != self.pos:
                self.send(self.pos, "position")
                self.oldpos = self.pos.copy()


    def draw(self):
        glMatrixMode(GL_MODELVIEW)

        # set generated matrix
        glPushMatrix()
        glLoadMatrixf(self.transform.getMatrix())

        # draw faces 
        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 0.5)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  0.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  0.0)
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
                        
    def handleMovementCommands(self):
        while self.dataReady("control3d"):
            cmd = self.recv("control3d")
            if cmd.type == Control3D.POSITION:
                self.pos = cmd.amount
            if cmd.type == Control3D.REL_POSITION:
                self.pos += cmd.amount
            if cmd.type == Control3D.ROTATION:
                self.rot = cmd.amount
            if cmd.type == Control3D.REL_ROTATION:
                self.rot = (self.rot+cmd.amount)%360
            if cmd.type == Control3D.SCALING:
                self.scaling = cmd.amount
            if cmd.type == Control3D.REL_SCALING:
                self.scaling += cmd.amount


    def main(self):
        displayservice = Display3D.getDisplayService()
        self.link((self,"display_signal"), displayservice)
        self.send(self.disprequest, "display_signal");

        # load texture
        if self.tex is not None:
            print self.tex
            glEnable(GL_TEXTURE_2D)

            textureSurface = pygame.image.load(self.tex)
            textureData = pygame.image.tostring(textureSurface, "RGBX", 1)

            glBindTexture(GL_TEXTURE_2D, textures[0])
            print glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                          GL_RGBA, GL_UNSIGNED_BYTE, textureData );
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                

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
                self.send( Control3D(Control3D.REL_ROTATION, Vector(0.1, 0.1, 0.1)), "outbox")

    class CubeMover(Axon.Component.component):
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

    class CubeBuzzer(Axon.Component.component):
        def main(self):
            r = 1.00
            f = 0.01
            while 1:
                yield 1
                if  r>1.0: f -= 0.001
                else: f += 0.001
                r += f
                
                self.send( Control3D(Control3D.SCALING, Vector(r, r, r)), "outbox")


    
    from Kamaelia.Util.ConsoleEcho import consoleEchoer
    from Kamaelia.Util.Graphline import Graphline
    
    Graphline(
        PLANE = TexPlane(pos=Vector(0, 0,-6), tex="Kamaelia.gif", name="1st Tex Plane"),
        ROTATOR = CubeRotator(),
#        MOVER = CubeMover(),
#        BUZZER = CubeBuzzer(),
        ECHO = consoleEchoer(),
        linkages = {
            ("PLANE", "outbox") : ("ECHO", "inbox"),
            ("ROTATOR", "outbox") : ("PLANE", "control3d"),
#            ("MOVER", "outbox") : ("PLANE", "control3d"),
#            ("BUZZER", "outbox") : ("CUBER", "control3d"),
        } ).run()
        
    Axon.Scheduler.scheduler.run.runThreads()  
