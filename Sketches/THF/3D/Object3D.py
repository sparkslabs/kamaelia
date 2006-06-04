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
    }
    
    Outboxes = {
        "outbox": "not used",
        "display_signal": "for communication with display3d",
    }
    
    def __init__(self, **argd):
        super(Object3D, self).__init__()
        # not sure about the needed data yet, just for testing
        self.rotspeed = Vector(0.1, 0.0, 0.0)
        self.size = Vector(2,2,2)
        self.pos = argd.get("pos",Vector(0,0,-15))
        self.rot = Vector(45,45,45)
        self.transform = Transform()

        # prepare vertices for intersection test
        x = float(self.size.x/2)
        y = float(self.size.y/2)
        z = float(self.size.z/2)
        self.vertices = [ Vector(x, 0.0, 0.0), Vector(0.0, y, 0.0), Vector(0.0, 0.0, z) ]
        
        # similar to Pygame component registration
        self.disprequest = { "3DDISPLAYREQUEST" : True,
#                                          "callback" : (self,"callback"),
#                                          "events" : (self, "inbox"),
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

    def turn(self):
        # simple test action: change rotation dir
        self.rotspeed.invert()
        pass
 
    def main(self):
        displayservice = Display3D.getDisplayService()
        self.link((self,"display_signal"), displayservice)
        self.send(self.disprequest, "display_signal");

        while 1:

#            for _ in self.waitBox("callback"): yield 1
#            self.display = self.recv("callback")

# There is no need for a callback yet
            
            yield 1
            
            self.rot += self.rotspeed
            self.rot %= 360

            # generate transformation matrix
            self.transform.reset()
            self.transform.applyRotation(self.rot)
            self.transform.applyTranslation(self.pos)

# Later it might be a good idea to provide a set of drawing functions
# so the component developer does not need to know about opengl
# This way opengl could later easily be replaced by an other mechanism
# for drawing
# TOGRA
            glMatrixMode(GL_MODELVIEW)

            # set generated matrix
            glPushMatrix()
            glLoadMatrixf(self.transform.getMatrix())

            # draw faces 
            glBegin(GL_QUADS)
            glColor3f(1.0,0.0,0.0)
            glVertex3f(1.0,1.0,1.0)
            glVertex3f(1.0,-1.0,1.0)
            glVertex3f(-1.0,-1.0,1.0)
            glVertex3f(-1.0,1.0,1.0)

            glColor3f(0.0,1.0,0.0)
            glVertex3f(1.0,1.0,-1.0)
            glVertex3f(1.0,-1.0,-1.0)
            glVertex3f(-1.0,-1.0,-1.0)
            glVertex3f(-1.0,1.0,-1.0)
            
            glColor3f(0.0,0.0,1.0)
            glVertex3f(1.0,1.0,1.0)
            glVertex3f(1.0,-1.0,1.0)
            glVertex3f(1.0,-1.0,-1.0)
            glVertex3f(1.0,1.0,-1.0)

            glColor3f(1.0,0.0,1.0)
            glVertex3f(-1.0,1.0,1.0)
            glVertex3f(-1.0,-1.0,1.0)
            glVertex3f(-1.0,-1.0,-1.0)
            glVertex3f(-1.0,1.0,-1.0)

            glColor3f(0.0,1.0,1.0)
            glVertex3f(1.0,1.0,1.0)
            glVertex3f(-1.0,1.0,1.0)
            glVertex3f(-1.0,1.0,-1.0)
            glVertex3f(1.0,1.0,-1.0)

            glColor3f(1.0,1.0,0.0)
            glVertex3f(1.0,-1.0,1.0)
            glVertex3f(-1.0,-1.0,1.0)
            glVertex3f(-1.0,-1.0,-1.0)
            glVertex3f(1.0,-1.0,-1.0)
            glEnd()

            glPopMatrix()
            glFlush()


if __name__=='__main__':
    from Kamaelia.Util.Graphline import Graphline
    pygame.init()
    obj = Object3D(pos=Vector(0, 0,-12)).activate()
    obj = Object3D(pos=Vector(0,4,-20)).activate()
    obj = Object3D(pos=Vector(4,0,-22)).activate()
    obj = Object3D(pos=Vector(0,-4,-18)).activate()
    obj = Object3D(pos=Vector(-4, 0,-15)).activate()
    Axon.Scheduler.scheduler.run.runThreads()  
