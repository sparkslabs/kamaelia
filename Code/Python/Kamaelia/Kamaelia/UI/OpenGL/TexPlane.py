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

"""\
=====================
Textured Plane
=====================

A plane showing a texture loaded from an image file.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

Example Usage
-------------
A plane showing an image loaded from the file "nemo.jpeg"::

    PLANE = TexPlane(position=(0, 0,-6), texture="nemo.jpeg").activate()
        
    Axon.Scheduler.scheduler.run.runThreads()
    
How does it work?
-----------------
This component is a subclass of OpenGLComponent (for OpenGLComponent
functionality see its documentation). It overrides
__init__(), setup(), draw().

In setup() the method loadTexture() get called which loads the texure
from the image file specified. If the image in the file has dimensions
which are not equal a power of two, the texture dimensions get enlarged
(this is needed because of OpenGL texturing limitations).

In draw() a simple plane is drawn whith the loaded texture on it.

"""


import Axon
import pygame
from OpenGL.GL import GL_TEXTURE_2D, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_QUADS, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR, GL_TEXTURE_MIN_FILTER, GL_RGBA, GL_UNSIGNED_BYTE
from OpenGL.GL import glEnable, glBindTexture, glTexEnvf, glTexCoord2f, glVertex3f, glEnd, glDisable, glGenTextures, glTexParameterf, glTexImage2D, glDisable

from .Vector import Vector
from .OpenGLComponent import OpenGLComponent

class TexPlane(OpenGLComponent):
    """\
    TexPlane(...) -> A new TexPlane component.
    
    A plane showing a texture loaded from an image file.

    Keyword arguments:
    
    - tex           -- image file name
    - pixelscaling  -- factor for translation from pixels to units in 3D space (default=100.0)
    """
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(TexPlane, self).__init__(**argd)

        self.tex = argd.get("texture")
        self.texID = 0

        self.pixelscaling = argd.get("pixelscaling", 100.0)
                                          

    def draw(self):
        """ Draws textured plane. """
        # set texure
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)

        # draw faces
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glBegin(GL_QUADS)
        w = self.size.x/2.0
        h = self.size.y/2.0
        glTexCoord2f(0.0, 1.0-self.tex_h); glVertex3f(-w, -h,  0.0)
        glTexCoord2f(self.tex_w, 1.0-self.tex_h); glVertex3f( w, -h,  0.0)
        glTexCoord2f(self.tex_w, 1.0); glVertex3f( w,  h,  0.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-w,  h,  0.0)
        glEnd()

        glDisable(GL_TEXTURE_2D)


    def loadTexture(self):
        """ Loads texture from specified image file. """
        if self.tex is not None:
            # load image
            image = pygame.image.load(self.tex)
            # create power of 2 dimensioned surface
            pow2size = (int(2**(ceil(log(image.get_width(), 2)))), int(2**(ceil(log(image.get_height(), 2)))))
            if pow2size != image.get_size():
                textureSurface = pygame.Surface(pow2size, pygame.SRCALPHA, 32)
                # determine texture coordinates
                self.tex_w = float(image.get_width())/pow2size[0]
                self.tex_h = float(image.get_height())/pow2size[1]
                # copy image data to pow2surface
                textureSurface.blit(image, (0,0))
            else:
                textureSurface = image
                self.tex_w = 1.0
                self.tex_h = 1.0
            # set plane size
            self.size = Vector(float(image.get_width())/float(self.pixelscaling), float(image.get_height())/float(self.pixelscaling), 0)
            # read pixel data
            textureData = pygame.image.tostring(textureSurface, "RGBX", 1)
            # gen tex name
            self.texID = glGenTextures(1)
            # create texture
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texID)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                            GL_RGBA, GL_UNSIGNED_BYTE, textureData );
            glDisable(GL_TEXTURE_2D)
        
    
    def setup(self):
        """ Load texture. """
        self.loadTexture()

__kamaelia_components__ = (TexPlane,)

if __name__=='__main__':
    PLANE = TexPlane(position=(0, 0,-6), texture="nemo.jpeg").activate()
        
    Axon.Scheduler.scheduler.run.runThreads()  
# Licensed to the BBC under a Contributor Agreement: THF
