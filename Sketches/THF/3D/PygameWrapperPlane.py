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
from Intersect3D import *
import Axon

textures = [0,0]

class PygameWrapperPlane(Axon.Component.component):
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
        "control3d": "receive Control3D commands here",
        "wrapcallback": "receive wrap data after WRAPREQUEST",
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
        super(PygameWrapperPlane, self).__init__()
        
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
        
        self.texID = 0
        
        self.wrappedComp = argd.get("wrap")

        # prepare vertices for intersection test
        x = float(self.size.x/2)
        y = float(self.size.y/2)
        self.vertices = [ Vector(-x, y, 0.0), Vector(x, y, 0.0), Vector(x, -y, 0.0), Vector(-x, -y, 0.0) ]
        
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
        transformedVerts = [self.transform.transformVector(v) for v in self.vertices]    
        t = Intersect3D.ray_Polygon(o, d, transformedVerts)
        pint = d*t
        Ap = pint-transformedVerts[0]
        AB = transformedVerts[1]-transformedVerts[0]
        AD = transformedVerts[3]-transformedVerts[0]
        x = Ap.dot(AB)
        y = Ap.dot(AD)
        
        if t!=0:
            print "2D:", x, y
        return t


    def applyTransforms(self):
        # generate new transformation matrix if needed
        if self.oldscaling != self.scaling or self.oldrot != self.rot or self.oldpos != self.pos:
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

        # set texure
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)

        # set generated matrix
        glPushMatrix()
        glLoadMatrixf(self.transform.getMatrix())

        # draw faces 
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glBegin(GL_QUADS)
        glColor3f(0,1,0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  0.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  0.0)
        glEnd()

        glPopMatrix()

        glDisable(GL_TEXTURE_2D)
    
    
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

    def waitBox(self,boxname):
        """Generator. yields 1 until data ready on the named inbox."""
        waiting = True
        while waiting:
            if self.dataReady(boxname): return
            else: yield 1
    

    def main(self):
        displayservice = Display3D.getDisplayService()
        self.link((self,"display_signal"), displayservice)
        self.send(self.disprequest, "display_signal");

        print "HELLO1"
        while 1:
            try: 
                self.wraprequest = { "WRAPPERREQUEST" : True,
                                                  "wrapcallback" : (self, "wrapcallback"),
                                                  "surface": self.wrappedComp.display }
                print "HELLO"
                self.send( self.wraprequest, "display_signal")
                break
            except AttributeError:
                yield 1
                
        for _ in self.waitBox("wrapcallback"): yield 1
        self.texID = self.recv("wrapcallback")

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


    text = """\
The lights begin to twinkle from the rocks;
The long day wanes; the slow moon climbs; the deep
Moans round with many voices.  Come, my friends.
'T is not too late to seek a newer world.Push off, and sitting well in order smite
The sounding furrows; for my purpose holds
To sail beyond the sunset, and the baths
Of all the western stars, until I die.
It may be that the gulfs will wash us down;
It may be we shall touch the Happy Isles,
And see the great Achilles, whom we knew.
Tho' much is taken, much abides; and tho'
We are not now that strength which in old days
Moved earth and heaven, that which we are, we are,--
One equal temper of heroic hearts,
Made weak by time and fate, but strong in will
To strive, to seek, to find, and not to yield.
"""
    class datasource(Axon.Component.component):
        def main(self):
            for x in text.split():
                self.send(x,"outbox")
                yield 1
    
    from Kamaelia.Util.ConsoleEcho import consoleEchoer
    from Kamaelia.Util.Graphline import Graphline
    from Kamaelia.UI.Pygame.Ticker import Ticker

    Display3D.getDisplayService()[0].overridePygameDisplay()
   
    TEXT = datasource().activate()
    TICKER = Ticker(position = (400, 300), render_left = 0, render_right=350, render_top=0, render_bottom=257).activate()
    WRAPPER = PygameWrapperPlane(wrap=TICKER, pos=Vector(0, 0,-6), tex="Kamaelia.gif", name="1st Tex Plane").activate()
    ECHO = consoleEchoer().activate()
    WRAPPER.link((WRAPPER, "outbox"), (ECHO, "inbox"))
    TEXT.link((TEXT, "outbox"), (TICKER, "inbox"))
        
    Axon.Scheduler.scheduler.run.runThreads()  
