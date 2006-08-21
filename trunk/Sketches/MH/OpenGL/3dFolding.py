#!/usr/bin/env python

from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.Vector import Vector
from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.Transform import Transform

from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.OpenGLComponent import OpenGLComponent

import Axon
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


import time,math

class Simple3dFold(OpenGLComponent):
    
    def __init__(self, **argd):
        super(Simple3dFold, self).__init__(**argd)
        self.radius = argd.get("radius", 1.0)
        self.segments = argd.get("segments", 15)
    
    def setup(self):
        self.tex = "../../CE/characters/OLIVIA.jpg"
        self.loadTexture()
        
        size = self.size/2.0
        print self.tex_w, self.tex_h
        #              vertex coord        texture coord
        self.poly = [ ((-size.x, -size.y), (0.0,        1.0-self.tex_h)),
                      ((-size.x, +size.y), (0.0,        1.0           )),
                      ((+size.x, +size.y), (self.tex_w, 1.0           )),
                      ((+size.x, -size.y), (self.tex_w, 1.0-self.tex_h)),
                    ]
                    
        self.starttime = time.time()
        self.foldpoint = (size.x*+0.8, size.y*-0.8)
        self.folddelta = (0.5, 1.0)
                    

    def draw(self):
        
        polys = [ self.poly ]
        oldpoly = self.poly[:]
        
        distance = self.radius*math.pi
        for slicenum in range(0,self.segments):
            
            folddist = distance/self.segments*slicenum
            slicepoint = right90(normalise(self.folddelta, folddist))
            slicepoint = ( slicepoint[0] + self.foldpoint[0],
                           slicepoint[1] + self.foldpoint[1] )
            
            if len(oldpoly):
                oldpoly, newpoly = slicepoly(oldpoly, (slicepoint,self.folddelta))
            else:
                oldpoly, newpoly = oldpoly, []
            polys[-1] = oldpoly
            oldpoly = newpoly
        
            polys.append(newpoly)

        
        # tag each point with vector-from-start-of-folding
        # first part (non folded part) will be zero distance
        polys[0] = [ (point,(0,0),texpoint) for point,texpoint in polys[0] ]
        i=1
        while i<len(polys):
            polys[i] = [ (point,
                          vector_from_fold(point,(self.foldpoint,self.folddelta)),
                          texpoint)
                         for point,texpoint in polys[i] ]
            i+=1
        
        # now curl the polys
        polys3d = []
        for poly in polys:
            poly3d = []
            for (point,vec,texpoint) in poly:
                if vec==(0,0):
                    x,y,z = (point[0],point[1], 0.0)
                else:
                    angle = dist(vec) / self.radius  # goes 0..pi over a half circle
                    if angle <= math.pi:
                        cos = math.cos(angle)
                        sin = math.sin(angle)
                        nvec = normalise(vec,self.radius)
                        x = point[0]-vec[0] + sin*nvec[0]
                        y = point[1]-vec[1] + sin*nvec[1]
                        z = self.radius - self.radius*cos 
                    else:
                        z = 2.0*self.radius
                        fpv = normalise(right90(self.folddelta), (math.pi*self.radius/2.0))
                        fpx = self.foldpoint[0] + fpv[0]
                        fpy = self.foldpoint[1] + fpv[1]
                        x,y = reflect(point, ((fpx,fpy), self.folddelta))
                poly3d.append(((x,y,z),texpoint))
                    
            polys3d.append(poly3d)
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        
        val=0
        for poly in polys3d:
            glBegin(GL_POLYGON)
            for ((x,y,z),(tx,ty)) in poly:
                fade = abs(self.radius-z)/self.radius
                glColor3f(fade,fade,fade)
                glTexCoord2f(tx,ty)
                glVertex3f(x, y, z)
            glEnd()
                
        glDisable(GL_TEXTURE_2D)
        
    def frame(self):
        size = self.size/2.0
        
        angle = (time.time()-self.starttime) / 2.0
        self.folddelta = math.cos(angle), math.sin(angle)
        
        self.redraw()

    def loadTexture(self):
        """ Loads texture from specified image file. """
        from math import ceil, log
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

def slicepoly(poly, foldline):
    """\
    Slice a 2d poly CONVEX (not concave) across a line.

    Takes in a list of (X,Y) points reresenting a poly and a line (point_on_line, delta)
    and returns a list of [poly,poly]
    first poly is the poly for the left side of the line. 2nd slice is the right side.
    """
    foldpoint = foldline[0]
    folddelta = foldline[1]
    
    (prev, prevtex) = poly[-1]
    
    normpoly = []
    foldpoly = []
    
    subpoly = []
    currentside = whichSide(prev, foldline)
    
    for (point,texpoint) in poly:
        
        intersect = bisect(prev, point, foldline)
        pointside = whichSide(point, foldline)
        
        if intersect>=0.0 and intersect<=1.0:
            ipoint = interpolate(prev,point,intersect)
            itexpoint = interpolate(prevtex,texpoint,intersect)
        else:
            ipoint = tuple(point)
            itexpoint = tuple(texpoint)
        subpoly.append( (ipoint,itexpoint) )
        
        if currentside==0:
            currentside = pointside
        
        if pointside * currentside < 0.0:  # different signs, we've switched sides
            if currentside<0.0:
                normpoly.extend(subpoly)
            else:
                foldpoly.extend(subpoly)
                
            subpoly = [(ipoint,itexpoint),(point,texpoint)]
            currentside = pointside
        
        prev,prevtex = point,texpoint

    if currentside<0.0:
        normpoly.extend(subpoly)
    else:
        foldpoly.extend(subpoly)
    
    return normpoly,foldpoly


def whichSide(point,line):
    """Returns -ve, 0, +ve if point is on LHS, ontop, or RHS of line"""
    
    linepoint, linedelta = line
    
    # determine which side of the fold line this initial point is on
    # which side of the line is it on? right hand side, or left?
    pdx = point[0]-linepoint[0]
    pdy = point[1]-linepoint[1]
    
    if linedelta[0]==0:
        return pdx
    elif linedelta[0]>0:
        return (linedelta[1]/linedelta[0])*pdx - pdy
    elif linedelta[0]<0:
        return pdy - (linedelta[1]/linedelta[0])*pdx
    
    


def bisect(start,end,line):
    """Returns the point of intersection of a line between start and end
    and an infinite line (defined by a point and delta vector).
    0 = intersects at start
    0.5 = intersects half way between start and end
    1 = intersects at end
    <0 or >1 = intersects outside of those bounds
    None = lines are parallel
    """
    point,delta = line
    
    divisor = ( (end[1]-start[1])*delta[0] - (end[0]-start[0])*delta[1] )
    if divisor != 0.0:
        intersect = ( (point[1]-start[1])*delta[0] - (point[0]-start[0])*delta[1] ) / divisor
    else:
        return None
                
    return intersect
    
def interpolate(start,end,val):
    return [ start*(1.0-val) + end*val for (start,end) in zip(start,end) ]
    
def reflect(point,foldline):
    foldpoint = foldline[0]
    dx,dy = foldline[1]
    
    # move line (and therefore the point) so the line passes through (0,0)
    px = point[0]-foldpoint[0]
    py = point[1]-foldpoint[1]

    # find closest point on the line
    if dx == 0.0:
        cx = 0
        cy = py
    elif dy == 0.0:
        cx = px
        cy = 0
    else:
        cx = (py + px*dx/dy)/(dy/dx + dx/dy)
        cy = py + (dx/dy)*(px-cx)
        
    # reflect
    rx = point[0] - 2.0*(px-cx)
    ry = point[1] - 2.0*(py-cy)

    return rx,ry

def vector_from_fold(point,foldline):
    """returns the shortest vector from the foldline to the point"""
    foldpoint = foldline[0]
    dx,dy = foldline[1]
    
    # move line (and therefore the point) so the line passes through (0,0)
    px = point[0] - foldpoint[0]
    py = point[1] - foldpoint[1]

    # find closest point on the line
    if dx == 0.0:
        cx = 0
        cy = py
    elif dy == 0.0:
        cx = px
        cy = 0
    else:
        cx = (py + px*dx/dy)/(dy/dx + dx/dy)
        cy = py + (dx/dy)*(px-cx)
        
    return px-cx,py-cy

def normalise(vector, toLen=1.0):
    lenSquared = sum([v*v for v in vector])
    scaling = toLen/(lenSquared**0.5)
    return [v*scaling for v in vector]

def left90(vector):
    return (-vector[1],vector[0])

def right90(vector):
    return (vector[1],-vector[0])

def dist(vector):
    return (vector[0]*vector[0] + vector[1]*vector[1])**0.5

if __name__ == '__main__':
    import Axon
    
    from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
    from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.SimpleRotationInteractor import SimpleRotationInteractor

    display = OpenGLDisplay(background_colour=(0.75, 0.75, 1.0)).activate()
    OpenGLDisplay.setDisplayService(display)

    FOLD = Simple3dFold(position=(0,0,-22), size=(10,10,2), rotation=(-45,0,0)).activate()
    SimpleRotationInteractor(target=FOLD).activate()
    
    Axon.Scheduler.scheduler.run.runThreads()
    