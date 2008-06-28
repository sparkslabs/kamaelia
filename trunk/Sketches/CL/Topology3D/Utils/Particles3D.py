"""
References: 1. Kamaelia.UI.OpenGL.Button
2. Kamaelia.UI.OpenGL.OpenGLComponent
"""

import math

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

from THF.Kamaelia.UI.OpenGL.Vector import Vector
from THF.Kamaelia.UI.OpenGL.Transform import Transform

from Kamaelia.Support.Particles import Particle as BaseParticle

class Particle3D(BaseParticle):
    def __init__(self, position = (-1,0,-10), ID='a', name='a', sidecolour=(200,200,244), 
                 size=(0,0,0), **argd):
        super(Particle3D, self).__init__(position=position, ID = ID)
        self.pos = position
        #self.posVector = Vector(*position)
        self.sideColour = sidecolour
        self.size = Vector(*size)
        self.ID = ID
        self.name = name
        self.backgroundColour = argd.get("bgcolour", (244,244,244))
        self.foregroundColour = argd.get("fgcolour", (0,0,0))
        #self.sideColour = argd.get("sidecolour", (200,200,244))
        self.margin = argd.get("margin", 8)
        self.key = argd.get("key", None)

        self.fontsize = argd.get("fontsize", 50)
        self.pixelscaling = argd.get("pixelscaling", 100)
        self.thickness = argd.get("thickness", 0.3)
        #self.margin = 8
        self.buildCaption()        
        #  It's after buildCaption() because self.size is decided only after buildCaption() if size=(0,0,0)
        self.radius = self.size.length()
                
        self.identifier = None
        
        # get transformation data and convert to vectors
        #self.posVector = Vector( *argd.get("position", (0,0,0)) )
        self.rotation = Vector( *argd.get("rotation", (0.0,0.0,0.0)) )
        self.scaling = Vector( *argd.get("scaling", (1,1,1) ) )
        
        # for detection of changes
        self.oldrot = Vector()
        self.oldpos = self.initialpos = Vector()
        self.oldscaling = Vector()
        self.transform = Transform()
        
        
        
        self.needRedraw = True
    
    
    def draw(self):
        """ Draw button cuboid."""
        #print self.size
        hs = self.size/2
        #print hs
#        #glLoadIdentity() # LoadIdentity will clear matrix and invalidate applyTransforms                            
#        glTranslatef(*self.posVector.toTuple())
#        glScalef(2.1,2.1,2.1)
#        glRotatef(20.2,1.0,0.0,0.0)
#        glRotatef(20.2,0.0,1.0,0.0)
#        glRotatef(2.2,0.0,0.0,1.0)
        #print self.tex_w, self.tex_h
        
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
        
        # Draw links
        for p in self.bondedTo:
            glBegin(GL_LINES)
            glVertex3f(*self.initialpos.toTuple())
            glVertex3f(*(Vector(*p.pos)*10).toTuple())
            glEnd()
        
    def buildCaption(self):
        """Pre-render the text to go on the label."""
        # Text is rendered to self.image
        
        pygame.font.init()
        font = pygame.font.Font(None, self.fontsize)
        self.image = font.render(self.name,True, self.foregroundColour, )
        
        if self.size != Vector(0,0,0):
            texsize = (self.size.x*self.pixelscaling, self.size.y*self.pixelscaling)
        else:
            texsize = ( self.image.get_width()+2*self.margin, self.image.get_height()+2*self.margin )
            self.size=Vector(texsize[0]/float(self.pixelscaling), texsize[1]/float(self.pixelscaling), self.thickness)

        # create power of 2 dimensioned surface
        pow2size = (int(2**(math.ceil(math.log(texsize[0]+2*self.margin, 2)))), int(2**(math.ceil(math.log(texsize[1]+2*self.margin, 2)))))
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
        #print self.image.get_width(), self.image.get_height()
        #print textureSurface.get_width(), textureSurface.get_height()
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
        
        
        
    def applyTransforms(self):
        """ Use the objects translation/rotation/scaling values to generate a new transformation Matrix if changes have happened. """
        # generate new transformation matrix if needed
        if self.oldscaling != self.scaling or self.oldrot != self.rotation or self.oldpos != Vector(*self.pos):
            self.transform = Transform()
            self.transform.applyScaling(self.scaling)
            self.transform.applyRotation(self.rotation)
            self.transform.applyTranslation(Vector(*self.pos))

            if self.oldscaling != self.scaling:
                self.oldscaling = self.scaling.copy()

            if self.oldrot != self.rotation:
                self.oldrot = self.rotation.copy()

            if self.oldpos != Vector(*self.pos):
                self.oldpos = Vector(*self.pos)  
            # send new transform to display service
            transform_update = { "TRANSFORM_UPDATE": True,
                                 "objectid": id(self),
                                 "transform": self.transform
                               }
            return transform_update
        else:
            return None

    
    def setOffset( self, (left,top) ):
        """\
        Set the offset of the top left corner of the rendering area.

        If this particle is at (px,py) it will be rendered at (px-x,py-y).
        """
        self.left = left
        self.top  = top
        


from THF.Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent        
class OpenGLComponentParticle3D(OpenGLComponent):
    pass
    
    
class RenderingParticle3D(object):
    pass