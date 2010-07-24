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


class TexPlane(Object3D):
    
    def __init__(self, **argd):
        super(TexPlane, self).__init__(**argd)

        self.pixelscaling = argd.get("pixelscaling", 100.0)
        self.tex = argd.get("texture", None)
        self.texID = 0
                                          

    def draw(self):
        # set texure
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)

        # draw faces
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glBegin(GL_QUADS)
#        glColor3f(0,1,0)
        w = self.size.x/2.0
        h = self.size.y/2.0
        glTexCoord2f(0.0, 1.0-self.tex_h); glVertex3f(-w, -h,  0.0)
        glTexCoord2f(self.tex_w, 1.0-self.tex_h); glVertex3f( w, -h,  0.0)
        glTexCoord2f(self.tex_w, 1.0); glVertex3f( w,  h,  0.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-w,  h,  0.0)
        glEnd()

        glDisable(GL_TEXTURE_2D)


    def loadTexture(self):
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
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                            GL_RGBA, GL_UNSIGNED_BYTE, textureData );
            glDisable(GL_TEXTURE_2D)
        
    
    def setup(self):
        self.loadTexture()


if __name__=='__main__':
    PLANE = TexPlane(pos=Vector(0, 0,-6), texture="nemo.jpeg").activate()
        
    Axon.Scheduler.scheduler.run.runThreads()  
