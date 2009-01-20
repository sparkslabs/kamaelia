#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===============================================================================
Particle3D: Simple generic/ supertype particle for 3D Topology visualisation
===============================================================================

This is an implementation of a simple supertype particle for 3D topology
visualisation.



Example Usage
-------------
Subclass it and extend it by adding draw() method to render any shape you want the particle to be.


How does it work?
-----------------

This object subclasses Kamaelia.Support.Particles.Particle and adds 3D elements.

At initialisation, provide a unique ID, a starting (x,y,z) position tuple, and
a name. The name is displayed as a label on top of the particle. For other parameters,
such as bgcolour and fgcolour, see its doc string below.

If the particle becomes selected it changes its visual appearance to reflect
this.

There are two kinds of textures, i.e. text label and image textures. 
When the 'image' argument is provided, it uses image textures; otherwise, it uses
text label textures in which particle name is used as the caption of the label.
Note, the value of the 'image' argument is the uri of the image; it could be a
path in local drive, a network address or an internet address.

It only serves as a superclass of 3D particle and has no rendering (draw) method,
so it leaves the shape rendering to subclasses.




===========================================================================
CuboidParticle3D: cuboid rendering particle for 3D Topology visualisation
===========================================================================

This is an implementation of a simple cuboid particle for 3D topology
visualisation.



Example Usage
-------------
A 3D topology viewer where particles of type "-" are rendered by CuboidParticle3D
instances::

    TopologyViewer3D( particleTypes = {"-":CuboidParticle3D},
                    laws = Kamaelia.Support.Particles.SimpleLaws(bondLength=2),
                  ).run()

SimpleLaws are used that apply the same simple physics laws for all particle
types.



How does it work?
-----------------

This object subclasses Kamaelia.Visualisation.PhysicsGraph3D.Particles3D.Particle3D 
and adds methods to support rendering (draw).



===========================================================================
SphereParticle3D: sphere rendering particle for 3D Topology visualisation
===========================================================================

This is an implementation of a simple sphere particle for 3D topology
visualisation.

Note: it would be much slower than CuboidParticle3D because it uses GLU library.



Example Usage
-------------
A 3D topology viewer where particles of type "sphere" are rendered by SphereParticle3D
instances::

    TopologyViewer3D( particleTypes = {"sphere":SphereParticle3D},
                    laws = Kamaelia.Support.Particles.SimpleLaws(bondLength=2),
                  ).run()

SimpleLaws are used that apply the same simple physics laws for all particle
types.



How does it work?
-----------------

This object subclasses Kamaelia.Visualisation.PhysicsGraph3D.Particles3D.Particle3D 
and adds methods to support rendering (draw).




===========================================================================
TeapotParticle3D: teapot rendering particle for 3D Topology visualisation
===========================================================================

This is an implementation of a simple teapot particle for 3D topology
visualisation.

Note: it would be much slower than CuboidParticle3D and SphereParticle3D because it uses GLUT library.



Example Usage
-------------
A 3D topology viewer where particles of type "teapot" are rendered by CuboidParticle3D
instances::

    TopologyViewer3D( particleTypes = {"teapot":TeapotParticle3D},
                    laws = Kamaelia.Support.Particles.SimpleLaws(bondLength=2),
                  ).run()

SimpleLaws are used that apply the same simple physics laws for all particle
types.



How does it work?
-----------------

This object subclasses Kamaelia.Visualisation.PhysicsGraph3D.Particles3D.Particle3D 
and adds methods to support rendering (draw).



References: 1. Kamaelia.UI.OpenGL.Button
2. Kamaelia.UI.OpenGL.OpenGLComponent
"""

import math, os

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
    super(RenderingParticle3D, self).__init__(**argd)
    
    Simple 3D generic superclass particle for topology visualisation.
    
    Keyword arguments:
    
    - ID        -- a unique ID for this particle
    - position  -- (x,y,z) tuple of particle coordinates
    - name      -- A name this particle will be labelled with
    - bgcolour  -- Colour of surfaces behind text label (default=(230,230,230)), only apply to label texture 
    - fgcolour  -- Colour of the text label (default=(0,0,0), only apply to label texture 
    - sidecolour -- Colour of side planes (default=(200,200,244)), only apply to CuboidParticle3D
    - bgcolourselected  -- Background colour when the particle is selected (default=(0,0,0)
    - bgcolourselected  -- Frontground colour when the particle is selected (default=(244,244,244))
    - sidecolourselected -- Side colour when the particle is selected (default=(0,0,100))
    - size         -- Size of particle (length, width, depth), it depends on texture size if unspecified
    - margin       -- Margin size in pixels (default=8)
    - fontsize     -- Font size for label text (default=50)
    - pixelscaling -- Factor to convert pixels to units in 3d, ignored if size is specified (default=100)
    - thickness    -- Thickness of button widget, ignored if size is specified (default=0.3)
    - image        -- The uri of image, image texture instead of label texture is used if specified
    """
    
    
    def __init__(self, position = (-1,0,-10), ID='', **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Particle3D, self).__init__(position=position, ID = ID)
        
        self.pos = position
        self.initSize = Vector(*argd.get("size", (0,0,0)))
        
        self.selected = False

        self.bgcolour = argd.get("bgcolour", (230,230,230))
        self.fgcolour = argd.get("fgcolour", (0,0,0))
        self.sidecolour = argd.get("sidecolour", (200,200,244))
        
        self.bgcolourselected = argd.get("bgcolourselected", (0,0,0))
        self.fgcolourselected = argd.get("fgcolourselected", (244,244,244))
        self.sidecolourselected = argd.get("sidecolourselected", (0,0,100))
        
        self.margin = argd.get("margin", 8)
        self.fontsize = argd.get("fontsize", 50)
        self.pixelscaling = argd.get("pixelscaling", 100)
        self.thickness = argd.get("thickness", 0.3)
        
        # For picture texture
        self.image = argd.get("image", None)
        # For remote picture
        self.imageIO = None
        
        name = argd.get("name","NoName")
        self.set_label(name)
        
        # For rotation and scaling
        self.drotation = Vector()
        self.scaling = Vector( *argd.get("scaling", (1,1,1) ) )
        
        # For detection of changes
        self.oldpos = self.initialpos = Vector()
        self.oldscaling = Vector()
        
        # For transformation matrix multiplication
        # Store all transformations
        self.transform = Transform()
        # Specially store link transformations because link doesn't do rotation and scaling
        self.linkTransform = Transform()
        # Store all previous transformations to be multiplied with the current one
        self.oldrotTransform = Transform()
        
        # For redraw detection
        self.needRedraw = True
        
        # For drag handling
        self.oldpoint = None
    
    
    def get_bgcolour(self):
        """Get bgcolour."""
        return self._bgcolour
        
    def set_bgcolour(self, value):
        """Set bgcolour and bgcurcolour as well if it is not selected."""
        self._bgcolour = value
        if not self.selected:
            self.bgcurcolour = value
    bgcolour=property(get_bgcolour, set_bgcolour, None, None)
    
    
    def get_fgcolour(self):
        """Get fgcolour."""
        return self._fgcolour
    
    def set_fgcolour(self, value):
        """Set fgcolour and fgcurcolour as well if it is not selected."""
        self._fgcolour = value
        if not self.selected:
            self.fgcurcolour = value
    fgcolour=property(get_fgcolour, set_fgcolour, None, None)
    
    
    def get_sidecolour(self):
        """Get sidecolour."""
        return self._sidecolour
    
    def set_sidecolour(self, value):
        """Set sidecolour and sidecurcolour as well if it is not selected."""
        self._sidecolour = value
        if not self.selected:
            self.sidecurcolour = value
    sidecolour=property(get_sidecolour, set_sidecolour, None, None)
    
    
    def get_bgcolourselected(self):
        """Get bgcolourselected."""
        return self._bgcolourselected
    
    def set_bgcolourselected(self, value):
        """Set bgcolourselected and bgcurcolour as well if it is selected."""
        self._bgcolourselected = value
        if self.selected:
            self.bgcurcolour = value
    bgcolourselected=property(get_bgcolourselected, set_bgcolourselected, None, None)
    
    
    def get_fgcolourselected(self):
        """Get fgcolourselected."""
        return self._fgcolourselected
    
    def set_fgcolourselected(self, value):
        """Set fgcolourselected and fgcurcolour as well if it is selected."""
        self._fgcolourselected = value
        if self.selected:
            self.fgcurcolour = value
    fgcolourselected=property(get_fgcolourselected, set_fgcolourselected, None, None)
    
    
    def get_sidecolourselected(self):
        """Get sidecolourselected."""
        return self._sidecolourselected
    
    def set_sidecolourselected(self, value):
        """Set sidecolourselected and sidecurcolour as well if it is selected."""
        self._sidecolourselected = value
        if self.selected:
            self.sidecurcolour = value
    sidecolourselected=property(get_sidecolourselected, set_sidecolourselected, None, None)
    
            
    def set_label(self, new_name):
        """Set text label."""
        if self.initSize == Vector():
            self.size = Vector()
        self.name = new_name
        self.buildCaption()        
        #  It's after buildCaption() because self.size is decided only after buildCaption() if size=(0,0,0)
        self.radius = self.size.length()/2
    
    
    def updateAttrs(self, **params):
        """Update attributes."""
        for key, value in params.iteritems():
            setattr(self, key, value)
        self.buildCaption()
        
                
    def draw(self):
        """\Stub method
        Override this method to draw concrete particles and links.
        """
        pass
    
        
    def readURLFile(self):
        """Read a string buffer of an object denoted by a URL."""
        fObject = urlopen(self.image)
        imageData = fObject.read()
        self.imageIO = StringIO(imageData)
        # Text label is not needed for picture texture
        self.set_label("Dummy")
    
            
    def buildCaption(self):
        """Pre-render the text to go on the label."""
        # Text is rendered to self.image
        if self.image is not None:
            if self.imageIO is not None:
                self.imageSurface = pygame.image.load(self.imageIO).convert()
                self.imageIO = None
            elif os.path.exists(self.image):
                self.imageSurface = pygame.image.load(self.image).convert()
            # Image texture is used instead of label texture if 'image' argument is specified
            elif self.image.find('://') != -1:
                # Use text label for notification of waiting before the picture is available
                pygame.font.init()
                font = pygame.font.Font(None, self.fontsize)
                self.imageSurface = font.render("Loading image...",True, self.fgcurcolour, )
                # Use thread to wrap urlopen in case urlopen is blocked
                import thread
                thread.start_new(self.readURLFile, ())
        else:
            # Label texture is used if 'image' argument is not specified
            pygame.font.init()
            font = pygame.font.Font(None, self.fontsize)
            self.imageSurface = font.render(self.name,True, self.fgcurcolour, )
        
        if self.size != Vector(0,0,0):
            texsize = (self.size.x*self.pixelscaling, self.size.y*self.pixelscaling)
        else:
            texsize = ( self.imageSurface.get_width()+2*self.margin, self.imageSurface.get_height()+2*self.margin )
            self.size=Vector(texsize[0]/float(self.pixelscaling), texsize[1]/float(self.pixelscaling), self.thickness)

        # create power of 2 dimensioned surface
        pow2size = (int(2**(math.ceil(math.log(texsize[0]+2*self.margin, 2)))), int(2**(math.ceil(math.log(texsize[1]+2*self.margin, 2)))))
        textureSurface = pygame.Surface(pow2size)
        textureSurface.fill( self.bgcurcolour )
        # determine texture coordinates
        self.tex_w = float(texsize[0])/pow2size[0]
        self.tex_h = float(texsize[1])/pow2size[1]
        # copy image data to pow2surface
        dest = ( max((texsize[0]-self.imageSurface.get_width())/2, 0), max((texsize[1]-self.imageSurface.get_height())/2, 0) )
        textureSurface.blit(self.imageSurface, dest)
        textureSurface = textureSurface.convert_alpha()

        # read pixel data
        textureData = pygame.image.tostring(textureSurface, "RGBX", 1)

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
        """Use the objects translation/rotation/scaling values to generate a new transformation Matrix if changes have happened."""
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
        self.selected = True
        self.sidecurcolour = self.sidecolourselected
        self.bgcurcolour = self.bgcolourselected
        self.fgcurcolour = self.fgcolourselected
        self.buildCaption()


    def deselect( self ):
        """Tell this particle it is deselected"""
        self.selected = False
        self.sidecurcolour = self.sidecolour
        self.bgcurcolour = self.bgcolour
        self.fgcurcolour = self.fgcolour
        self.buildCaption()



class CuboidParticle3D(Particle3D):
    """\
    Cuboid rendering particle
    """
    
    
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(CuboidParticle3D, self).__init__(**argd)


    def draw(self):
        """Draw CUBOID Particle."""
        hs = self.size/2
        
        # draw faces
        glBegin(GL_QUADS)
        glColor4f(self.sidecurcolour[0]/256.0, self.sidecurcolour[1]/256.0, self.sidecurcolour[2]/256.0, 0.5)

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
    Sphere rendering particle
    """
    
    
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SphereParticle3D, self).__init__(**argd)
        self.drotation = Vector(0,0,90)


    def draw(self):
        """Draw sphere particle."""
        hs = self.radius
        glColor4f(self.sidecurcolour[0]/256.0, self.sidecurcolour[1]/256.0, self.sidecurcolour[2]/256.0, 0.5)
        
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
    Teapot rendering particle
    """
    
    
    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(TeapotParticle3D, self).__init__(**argd)


    def draw(self):
        """Draw teapot particle."""
        hs = self.radius
        glColor4f(self.sidecurcolour[0]/256.0, self.sidecurcolour[1]/256.0, self.sidecurcolour[2]/256.0, 0.5)
        
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

# Licensed to the BBC under a Contributor Agreement: CL        