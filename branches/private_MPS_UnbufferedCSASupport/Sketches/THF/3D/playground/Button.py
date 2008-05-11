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


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Display3D import Display3D
from Util3D import *
from Object3D import *


class Button(Object3D):

    def __init__(self, **argd):
        super(Button, self).__init__(**argd)

        self.grabbed = 0

        # Button initialisation
        caption = argd.get("caption", "Button")

        self.backgroundColour = argd.get("bgcolour", (244,244,244))
        self.foregroundColour = argd.get("fgcolour", (0,0,0))
        self.sideColour = argd.get("sidecolour", (200,200,244))
        self.margin = argd.get("margin", 8)
        self.key = argd.get("key", None)
        self.caption = argd.get("caption", "Button")

        self.fontsize = argd.get("fontsize", 50)
        self.pixelscaling = argd.get("pixelscaling", 100)
        self.thickness = argd.get("thickness", 0.2)

        self.eventMsg = argd.get("msg", "CLICK")

        self.activated = False
        self.actrot = 0


    def setup(self):
        self.buildCaption()
        self.addListenEvents( [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP ])


    def draw(self):
        hs = self.size/2.0
        # draw faces
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
        
        glDisable(GL_TEXTURE_2D)

    def handleEvents(self):
        while self.dataReady("inbox"):
            event = self.recv("inbox")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.ogl_name in event.hitobjects:
                    self.grabbed = event.button
                    self.scaling = Vector(0.9,0.9,0.9)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.grabbed = 0
                    self.scaling = Vector(1,1,1)
                    #activate
                    if self.ogl_name in event.hitobjects:
                        self.send( self.eventMsg, "outbox" )
                        self.activated = True

    

    def buildCaption(self):
        """Pre-render the text to go on the button label."""
        # Text is rendered to self.image
        pygame.font.init()
        font = pygame.font.Font(None, self.fontsize)
        self.image = font.render(self.caption,True, self.foregroundColour, )
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


    def frame(self):
        self.steadyMovement()


from SkyGrassBackground import *

if __name__=='__main__':

    BUTTON1 = Button(caption="<<", msg="Previous", pos=Vector(-3,0,-10)).activate()
    BUTTON2 = Button(caption=">>", msg="Next", pos=Vector(3,0,-10)).activate()
    BUTTON3 = Button(caption="Play", msg="Play", pos=Vector(-1,0,-10)).activate()
    BUTTON4 = Button(caption="Stop", msg="Stop", pos=Vector(1,0,-10)).activate()
    bg = SkyGrassBackground(size=Vector(5000,5000,0), pos = Vector(0, 0, -100)).activate()


    Axon.Scheduler.scheduler.run.runThreads()
    
