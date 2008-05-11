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
from Intersect3D import *
import Axon


class Button3D(Axon.Component.component):
    Inboxes = {
       "inbox": "not used",
       "control": "ignored",
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

    def __init__(self, caption=None, position=None, margin=8, bgcolour = (244,244,244), fgcolour = (0,0,0), msg=None,
                key = None, transparent = False,
                fontsize = 50, pixelscaling = 100, thickness = 0.2, sidecolour = (200,200,244),
                size=None, pos = Vector(0,0,0), rot = Vector(0,0,0), scaling = Vector(1,1,1)):
        super(Button3D, self).__init__()
        # 3D object initialisation
        self.size = size
        self.pos = pos
        self.rot = rot
        self.scaling = scaling
        self.transform = Transform()

        self.oldrot = Vector()
        self.oldpos = Vector()
        self.oldscaling = Vector()

        self.grabbed = 0

        # Button initialisation
        if caption is None:
            caption = "Button"

        self.backgroundColour = bgcolour
        self.foregroundColour = fgcolour
        self.margin = margin
        self.key = key
        self.caption = caption

        self.sideColour = sidecolour
        self.fontsize = fontsize
        self.pixelscaling = pixelscaling
        self.thickness = thickness

        if msg is None:
            msg = ("CLICK", self.id)
        self.eventMsg = msg

        self.wiggle = Vector(0.1,0.1,0.1)
        self.wiggleadd = Vector(0.001, 0.001, 0.001)
        self.activated = False
        self.actrot = 0

        # prepare vertices for intersection test
        self.vertices = [ Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1) ]

        # similar to Pygame component registration
        self.disprequest = { "3DDISPLAYREQUEST" : True,
#                                          "callback" : (self,"callback"),
                                          "events" : (self, "inbox"),
#                                          "size": self.size,
#                                          "pos": self.pos,
                                          "object": self }


    def buildCaption(self, text):
        """Pre-render the text to go on the button label."""
        # Text is rendered to self.image
        pygame.font.init()
        font = pygame.font.Font(None, self.fontsize)
        self.image = font.render(text,True, self.foregroundColour, )
        # create power of 2 dimensioned surface
        pow2size = (int(2**(ceil(log(self.image.get_width(), 2)))), int(2**(ceil(log(self.image.get_height(), 2)))))
        textureSurface = pygame.Surface(pow2size)
        textureSurface.fill( self.backgroundColour )
        # determine texture coordinates
        self.tex_w = float(self.image.get_width()+2*self.margin)/pow2size[0]
        self.tex_h = float(self.image.get_height()+2*self.margin)/pow2size[1]
        # copy image data to pow2surface
        textureSurface.blit(self.image, (self.margin,self.margin))
 #       textureSurface.set_alpha(128)
#        textureSurface = textureSurface.convert_alpha()

        # read pixel data
        textureData = pygame.image.tostring(textureSurface, "RGBX", 1)

        self.texID = glGenTextures(1)
        # create texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                        GL_RGBA, GL_UNSIGNED_BYTE, textureData );
        glDisable(GL_TEXTURE_2D)

        if self.size is None:
            self.size=Vector(self.image.get_width()/float(self.pixelscaling), self.image.get_height()/float(self.pixelscaling), self.thickness)


    # Ray intersection test
    # returns the distance of the origin o to the point of intersection
    # if no intersection occurs, 0 is returned
    # Algorithm from "Realtime Rendering"
    def intersectRay(self, o, d):
        transformed = [self.transform.transformVector(v) for v in self.vertices]
        halfwidths = [float(self.size.x/2), float(self.size.y/2), float(self.size.z/2)]
        return Intersect3D.ray_OBB(o, d, self.pos, transformed, halfwidths)


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

        # set generated matrix
        glPushMatrix()
        glLoadMatrixf(self.transform.getMatrix())

        hs = self.size/2.0
        # draw faces
#        glDisable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        glBegin(GL_QUADS)
        glColor4f(self.sideColour[0]/256.0, self.sideColour[1]/256.0, self.sideColour[2]/256.0, 0.5)


        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,hs.y,-hs.z)

        glVertex3f(-hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)

        glVertex3f(hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,hs.z)
        glVertex3f(-hs.x,hs.y,-hs.z)
        glVertex3f(hs.x,hs.y,-hs.z)

        glVertex3f(hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glVertex3f(hs.x,-hs.y,-hs.z)
        glEnd()


        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

        glBegin(GL_QUADS)
        # back plane
        glTexCoord2f(self.tex_w, 1.0-self.tex_h)
        glVertex3f(hs.x,hs.y,-hs.z)
        glTexCoord2f(0.0, 1.0-self.tex_h)
        glVertex3f(-hs.x,hs.y,-hs.z)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-hs.x,-hs.y,-hs.z)
        glTexCoord2f(self.tex_w, 1.0)
        glVertex3f(hs.x,-hs.y,-hs.z)
        # front plane
        glTexCoord2f(0.0, 1.0-self.tex_h)
        glVertex3f(-hs.x,-hs.y,hs.z)
        glTexCoord2f(self.tex_w, 1.0-self.tex_h)
        glVertex3f(hs.x,-hs.y,hs.z)
        glTexCoord2f(self.tex_w, 1.0)
        glVertex3f(hs.x,hs.y,hs.z)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-hs.x,hs.y,hs.z)
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
#        glEnable(GL_DEPTH_TEST)


    def handleEvents(self):
        while self.dataReady("inbox"):
            for event in self.recv("inbox"):
                if event.movementMode:
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
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and self.intersectRay(Vector(0,0,0), event.dir) > 0:
                            self.grabbed = event.button
                            self.scaling = Vector(0.9,0.9,0.9)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            self.grabbed = 0
                            self.scaling = Vector(1,1,1)
                            if self.intersectRay(Vector(0,0,0), event.dir) > 0:
                                #activate
                                self.send( self.eventMsg, "outbox" )
                                self.activated = True


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


    def steadyMovement(self):
#        self.rot += self.wiggle
#        if self.wiggle.x >= 0.1 or self.wiggle.x <=-0.1:
#            self.wiggleadd *= -1
#        self.wiggle += self.wiggleadd

        if self.activated:
            self.rot += Vector(3,0,0)%360
            self.actrot += 3
            if self.actrot >= 360:
                self.actrot = 0
                self.activated = False

    def main(self):
        displayservice = Display3D.getDisplayService()
        self.link((self,"display_signal"), displayservice)
        self.send(self.disprequest, "display_signal");

        self.buildCaption(self.caption)


        while 1:

#            for _ in self.waitBox("callback"): yield 1
#            self.display = self.recv("callback")

# There is no need for a callback yet

            yield 1
            self.steadyMovement()

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
    from Kamaelia.Util.ConsoleEcho import consoleEchoer
    from Display3D import *
    from Movement3D import *
    path1 = LinearPath3D([Vector(3,3,-20), Vector(4,0,-20), Vector(3,-3,-20), Vector(0,-4,-20), Vector(-3,-3,-20),Vector(-4,0,-20),  Vector(-3,3,-20),Vector(0,4,-20),  Vector(3,3,-20)], 1000)

    Display3D.overridePygameDisplay()

    ECHO = consoleEchoer().activate()
    BUTTON1 = Button3D(caption="<<", msg="Previous", pos=Vector(-3,0,-10)).activate()
    BUTTON2 = Button3D(caption=">>", msg="Next", pos=Vector(3,0,-10)).activate()
    BUTTON3 = Button3D(caption="Play", msg="Play", pos=Vector(-1,0,-10)).activate()
    BUTTON4 = Button3D(caption="Stop", msg="Stop", pos=Vector(1,0,-10)).activate()
    PATHMOVER = PathMover(path1).activate()
    CUBE = SimpleCube().activate()

    BUTTON1.link((BUTTON1, "outbox"), (PATHMOVER, "inbox"))
    BUTTON2.link((BUTTON2, "outbox"), (PATHMOVER, "inbox"))
    BUTTON3.link((BUTTON3, "outbox"), (PATHMOVER, "inbox"))
    BUTTON4.link((BUTTON4, "outbox"), (PATHMOVER, "inbox"))
    PATHMOVER.link((PATHMOVER,"outbox"), (CUBE,"control3d"))
    PATHMOVER.link((PATHMOVER,"status"), (ECHO,"inbox"))

    Axon.Scheduler.scheduler.run.runThreads()
    
