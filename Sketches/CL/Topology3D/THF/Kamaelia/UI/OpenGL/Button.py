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
====================
OpenGL Button Widget
====================

A button widget for the OpenGL display service. Sends a message when
clicked or an assigned key is pressed.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

Example Usage
-------------
4 Buttons which could be used for playback control (output to the console)::

    Graphline(
        BUTTON1 = Button(caption="<<", msg="Previous", position=(-3,0,-10)),
        BUTTON2 = Button(caption=">>", msg="Next", position=(3,0,-10)),
        BUTTON3 = Button(caption="Play", msg="Play", position=(-1,0,-10)),
        BUTTON4 = Button(caption="Stop", msg="Stop", position=(1,0,-10)),
        ECHO = ConsoleEchoer(),
        linkages = {
            (BUTTON1, "outbox") : (ECHO, "inbox"),
            (BUTTON2, "outbox") : (ECHO, "inbox"),
            (BUTTON3, "outbox") : (ECHO, "inbox"),
            (BUTTON4, "outbox") : (ECHO, "inbox"),            
        }
    ).run()
    
How does it work?
-----------------
This component is a subclass of OpenGLComponent (for OpenGLComponent
functionality see its documentation). It overrides __init__(), setup(),
draw(), handleEvents() and frame().

In setup() it requests to receive mouse events and calls buildCaption()
where the set caption is rendered on a pygame surface. This surface is
then set as OpenGL texture.

In draw() a flat cuboid is drawn (if size is not specified) with the
caption texture on both the front and the back surface.

In handleEvents() the component reacts to mouse events and, if a key is
assigned, to the keydown event. If a mouse click happens when the mouse
pointer is over the button it gets "grabbed", which is visualised by
shrinking the button by a little amount, until the button is released
again. Only if the mouse button is released over the button widget it
gets activated. On activation the button gets rotated by 360 degrees
around the X axis.

In frame() the button gets rotated when it has been activated.

"""


import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#from OpenGLComponent import OpenGLComponent
from Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent
from Vector import Vector
from math import *


class Button(OpenGLComponent):
    """
    Button(...) -> A new Button component.

    A button widget for the OpenGL display service. Sends a message when
    clicked or an assigned key is pressed.

    Keyword arguments:

    -caption      -- Button caption (default="Button")
    -bgcolour     -- Colour of surfaces behind caption (default=(244,244,244))
    -fgcolour     -- Colour of the caption text (default=(0,0,0)
    -sidecolour   -- Colour of side planes (default=(200,200,244))
    -margin       -- Margin size in pixels (default=8)
    -key          -- Key to activate button (default=None)
    -fontsize     -- Font size for caption text (default=50)
    -pixelscaling -- Factor to convert pixels to units in 3d, ignored if size is specified (default=100)
    -thickness    -- Thickness of button widget, ignored if size is specified (default=0.3)
    -msg          -- Message which gets sent when button is activated (default="CLICK")
        
    """
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Button, self).__init__(**argd)

        self.grabbed = 0

        # Button initialisation
        self.caption = argd.get("caption", "Button")

        self.backgroundColour = argd.get("bgcolour", (244,244,244))
        self.foregroundColour = argd.get("fgcolour", (0,0,0))
        self.sideColour = argd.get("sidecolour", (200,200,244))
        self.margin = argd.get("margin", 8)
        self.key = argd.get("key", None)

        self.fontsize = argd.get("fontsize", 50)
        self.pixelscaling = argd.get("pixelscaling", 100)
        self.thickness = argd.get("thickness", 0.3)

        self.eventMsg = argd.get("msg", "CLICK")

        self.activated = False
        self.actrot = 0


    def setup(self):
        """ Build caption and request reception of events."""
        self.buildCaption()
        self.addListenEvents( [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN ])


    def draw(self):
        """ Draw button cuboid."""
        hs = self.size/2.0
        print hs
        print self.tex_w, self.tex_h
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
        #glVertex3f(-2.0, -1.0,  1.0)
        glTexCoord2f(self.tex_w, 1.0-self.tex_h)
        glVertex3f(hs.x,-hs.y,hs.z)
        #glVertex3f( 2.0, -1.0,  1.0)
        glTexCoord2f(self.tex_w, 1.0)
        glVertex3f(hs.x,hs.y,hs.z)
        #glVertex3f( 2.0,  5.0,  1.0) 
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-hs.x,hs.y,hs.z)
        #glVertex3f(-2.0,  5.0,  1.0)
        glEnd()
        
        glDisable(GL_TEXTURE_2D)

        
    def frame(self):
        """ Rotate button if it has been activated. """
        self.activationMovement()

        
    def handleEvents(self):
        """ Handle events. """
        while self.dataReady("events"):
            event = self.recv("events")
            if event.type == pygame.KEYDOWN:
                if event.key == self.key:
                    activate = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.identifier in event.hitobjects:
                    self.grabbed = event.button
                    self.scaling = Vector(0.9,0.9,0.9)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.grabbed = 0
                    self.scaling = Vector(1,1,1)
                    #activate
                    if self.identifier in event.hitobjects:
                        self.send( self.eventMsg, "outbox" )
                        self.activated = True

    

    def buildCaption(self):
        """Pre-render the text to go on the label."""
        # Text is rendered to self.image
        pygame.font.init()
        font = pygame.font.Font(None, self.fontsize)
        self.image = font.render(self.caption,True, self.foregroundColour, )
        
        if self.size != Vector(0,0,0):
            texsize = (self.size.x*self.pixelscaling, self.size.y*self.pixelscaling)
        else:
            texsize = ( self.image.get_width()+2*self.margin, self.image.get_height()+2*self.margin )
            self.size=Vector(texsize[0]/float(self.pixelscaling), texsize[1]/float(self.pixelscaling), self.thickness)

        # create power of 2 dimensioned surface
        pow2size = (int(2**(ceil(log(texsize[0]+2*self.margin, 2)))), int(2**(ceil(log(texsize[1]+2*self.margin, 2)))))
        textureSurface = pygame.Surface(pow2size)
        textureSurface.fill( self.backgroundColour )
        # determine texture coordinates
        self.tex_w = float(texsize[0])/pow2size[0]
        self.tex_h = float(texsize[1])/pow2size[1]
        # copy image data to pow2surface
        dest = ( max((texsize[0]-self.image.get_width())/2, 0), max((texsize[1]-self.image.get_height())/2, 0) )
        textureSurface.blit(self.image, dest)
#        textureSurface.set_alpha(128)
        textureSurface = textureSurface.convert_alpha()

        # read pixel data
        textureData = pygame.image.tostring(textureSurface, "RGBX", 1)
        print self.image.get_width(), self.image.get_height()
        print textureSurface.get_width(), textureSurface.get_height()
        #print textureData

        self.texID = glGenTextures(1)
        # create texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                        GL_RGBA, GL_UNSIGNED_BYTE, textureData );
        glDisable(GL_TEXTURE_2D)


    def activationMovement(self):
        """ Rotate button stepwise by 360 degrees when it has been activated. """
        if self.activated:
            amount = 800.0*self.frametime
            self.rotation.x += amount
            self.rotation.x %= 360.0
            self.actrot += amount
            if self.actrot >= 360.0:
                self.rotation.x -= (self.actrot-360.0)
                self.actrot = 0.0
                self.activated = False




if __name__=='__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline

    Graphline(
#        BUTTON1 = Button(caption="<<", msg="Previous", position=(-3,0,-10)),
#        BUTTON2 = Button(caption=">>", msg="Next", position=(3,0,-10)),
        BUTTON3 = Button(caption="Play", msg="Play", position=(0,0,-5)),
#        BUTTON4 = Button(caption="Stop", msg="Stop", position=(1,0,-10)),
        ECHO = ConsoleEchoer(),
        linkages = {
            ("BUTTON1", "outbox") : ("ECHO", "inbox"),
#            ("BUTTON2", "outbox") : ("ECHO", "inbox"),
#            ("BUTTON3", "outbox") : ("ECHO", "inbox"),
#            ("BUTTON4", "outbox") : ("ECHO", "inbox"),            
        }
    ).run()
# Licensed to the BBC under a Contributor Agreement: THF
