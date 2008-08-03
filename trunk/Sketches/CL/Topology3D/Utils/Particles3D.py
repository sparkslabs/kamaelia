"""
3D particles

References: 1. Kamaelia.UI.OpenGL.Button
2. Kamaelia.UI.OpenGL.OpenGLComponent
"""

import math, sys, os

from urllib import urlopen
from cStringIO import StringIO
                
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Kamaelia.UI.OpenGL.Vector import Vector
from Kamaelia.UI.OpenGL.Transform import Transform

from Kamaelia.Support.Particles import Particle as BaseParticle

class Particle3D(BaseParticle):
    """\
    A super class for 3D particles
    """
    
    def __init__(self, position = (-1,0,-10), ID='', **argd):
        super(Particle3D, self).__init__(position=position, ID = ID)
        
        self.pos = position
        self.initSize = Vector(*argd.get("size", (0,0,0)))

        self.backgroundColourWhenUnselected = self.backgroundColour = argd.get("bgcolour", (230,230,230))
        self.foregroundColourWhenUnselected = self.foregroundColour = argd.get("fgcolour", (0,0,0))
        self.sideColourWhenUnselected = self.sideColour = argd.get("sidecolour", (200,200,244))
        
        self.backgroundColourWhenSelected = argd.get("bgcolourselected", (0,0,0))
        self.foregroundColourWhenSelected = argd.get("fgcolourselected", (244,244,244))
        self.sideColourWhenSelected = argd.get("sidecolourselected", (200,200,244))
        
        self.margin = argd.get("margin", 8)
        self.fontsize = argd.get("fontsize", 50)
        self.pixelscaling = argd.get("pixelscaling", 100)
        self.thickness = argd.get("thickness", 0.3)
        
        # For picture texture
        self.pic = argd.get("image", None)
        
        name = argd.get("name","NoName")
        self.set_label(name)
        
        # For rotation and scaling
        self.drotation = Vector()
        self.scaling = Vector( *argd.get("scaling", (1,1,1) ) )
        
        # For detection of changes
        self.oldpos = self.initialpos = Vector()
        self.oldscaling = Vector()
        
        # For transformation matrix multiplication
        self.transform = Transform()
        self.linkTransform = Transform()
        self.oldrotTransform = Transform()
        
        # For redraw detection
        self.needRedraw = True
        
        # For drag handling
        self.oldpoint = None
        
        
    
    def set_label(self, new_name):
        if self.initSize == Vector():
            self.size = Vector()
        self.name = new_name
        self.buildCaption()        
        #  It's after buildCaption() because self.size is decided only after buildCaption() if size=(0,0,0)
        self.radius = self.size.length()/2
    
    def draw(self):
        """\Stub method
        
        Override this method to draw particles and links.
        """
        pass
        
    def buildCaption(self):
        """Pre-render the text to go on the label."""
        # Text is rendered to self.image
        if self.pic is not None:
            if self.pic.find('://') != -1 and not os.path.exists(self.pic):
                fObject = urlopen(self.pic)
                picData = fObject.read()
                pic = StringIO(picData)
            else:
                pic = self.pic
            self.image = pygame.image.load(pic).convert()
        else:
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
        if self.oldscaling != self.scaling or self.drotation != Vector() or self.oldpos != Vector(*self.pos):
            self.transform = Transform()
            self.linkTransform = Transform()
            drotationTransform = Transform()
            drotationTransform.applyRotation(self.drotation)
            
            self.transform.applyScaling(self.scaling)
            self.linkTransform.applyScaling(self.scaling)
            
            self.transform = self.transform*self.oldrotTransform*drotationTransform
            self.oldrotTransform = self.oldrotTransform*drotationTransform
            
            self.transform.applyTranslation(Vector(*self.pos))
            self.linkTransform.applyTranslation(Vector(*self.pos))

            if self.oldscaling != self.scaling:
                self.oldscaling = self.scaling.copy()
            
            self.drotation = Vector()    
            
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

    
    def select( self ):
        """Tell this particle it is selected"""
        #self.selected = True
        self.sideColour = self.sideColourWhenSelected
        self.backgroundColour = self.backgroundColourWhenSelected
        self.foregroundColour = self.foregroundColourWhenSelected
        self.buildCaption()

    def deselect( self ):
        """Tell this particle it is deselected"""
        #self.selected = False
        self.sideColour = self.sideColourWhenUnselected
        self.backgroundColour = self.backgroundColourWhenUnselected
        self.foregroundColour = self.foregroundColourWhenUnselected
        self.buildCaption()

class CuboidParticle3D(Particle3D):
    """\
    Cuboid particle
    """
    
    def __init__(self, **argd):
        super(CuboidParticle3D, self).__init__(**argd)

    def draw(self):
        """ DRAW CUBOID Particle."""
        hs = self.size/2
        
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
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixf(self.linkTransform.getMatrix())
        for p in self.bondedTo:
            glBegin(GL_LINES)
            glVertex3f(*self.initialpos.toTuple())
            glVertex3f(*(Vector(*p.pos)-Vector(*self.pos)).toTuple())
            glEnd()
        glPopMatrix()


class SphereParticle3D(Particle3D):
    """\
    Sphere particle
    """
    
    def __init__(self, **argd):
        super(SphereParticle3D, self).__init__(**argd)
        self.drotation = Vector(0,0,90)

    def draw(self):
        """ DRAW sphere particle."""
        hs = self.radius
        
        # Create a quadratic object for sphere rendering
        quadratic = gluNewQuadric()
        gluQuadricNormals(quadratic, GLU_SMOOTH)
        gluQuadricTexture(quadratic, GL_TRUE)
        
        # Add texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        
        # Draw sphere
        gluSphere(quadratic,hs,32,32)
        #glutSolidSphere(hs,32,32)
        
        glDisable(GL_TEXTURE_2D)
        
        # Draw links        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixf(self.linkTransform.getMatrix())
        for p in self.bondedTo:
            glBegin(GL_LINES)
            glVertex3f(*self.initialpos.toTuple())
            glVertex3f(*(Vector(*p.pos)-Vector(*self.pos)).toTuple())
            glEnd()
        glPopMatrix()


class TeapotParticle3D(Particle3D):
    """\
    Teapot particle
    """
    
    def __init__(self, **argd):
        super(TeapotParticle3D, self).__init__(**argd)

    def draw(self):
        """ DRAW teapot particle."""
        hs = self.radius
        
        # Add texture
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        glLoadIdentity()
        glRotatef(180.0,0.0,0.0,1.0)
        glMatrixMode(GL_MODELVIEW)
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        
        
        
        # Draw teapot
        glFrontFace(GL_CW)
        glutSolidTeapot(hs)
        glFrontFace(GL_CCW)
        
        glDisable(GL_TEXTURE_2D)
        
        glMatrixMode(GL_TEXTURE)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        # Draw links        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixf(self.linkTransform.getMatrix())
        for p in self.bondedTo:
            glBegin(GL_LINES)
            glVertex3f(*self.initialpos.toTuple())
            glVertex3f(*(Vector(*p.pos)-Vector(*self.pos)).toTuple())
            glEnd()
        glPopMatrix()


from Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent        
class OpenGLComponentParticle3D(OpenGLComponent):
    pass
    
    
class RenderingParticle3D(object):
    pass