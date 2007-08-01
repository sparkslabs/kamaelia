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

class SimpleFold(OpenGLComponent):

    def setup(self):
        size = self.size/2.0
        
        self.poly = [ (-size.x, -size.y),
                      (-size.x, +size.y),
                      (+size.x, +size.y),
                      (+size.x, -size.y),
                    ]
                    
        self.starttime = time.time()
        self.foldpoint = (size.x*+0.8, size.y*-0.8)
        self.foldline = ( self.foldpoint, (0.5, 1.0) )
                    

    def draw(self):
        
        normalpoly, foldedpoly = fold(self.poly, self.foldline)
        
        glBegin(GL_POLYGON)
        glColor3f(1.0, 1.0, 1.0)
        for (x,y) in normalpoly:
            glVertex3f(x, y, 0.0)
        glEnd()
        
        glBegin(GL_POLYGON)
        glColor3f(0.75, 0.75, 0.75)
        for (x,y) in foldedpoly:
            glVertex3f(x, y, 0.0)
        glEnd()
        
    def frame(self):
        size = self.size/2.0
        
        angle = (time.time()-self.starttime) / 2.0
        delta = math.cos(angle), math.sin(angle)
        
        self.foldline = ( self.foldpoint, delta)
        
        self.redraw()


def fold(poly, foldline):
    """\
    Folds a 2d poly CONVEX (not concave) across a line.

    Takes in a list of (X,Y) points reresenting a poly and a line (point_on_line, delta)
    and returns a list of [poly,poly]
    (second poly is the folded one)
    """
    foldpoint = foldline[0]
    folddelta = foldline[1]
    
    prev = poly[-1]
    
    normpoly = []
    foldpoly = []
    
    subpoly = []
    currentside = whichSide(prev, foldline)
    
    for point in poly:
        
        intersect = bisect(prev, point, foldline)
        pointside = whichSide(point, foldline)
        
        print ">",point, intersect
        if intersect>=0.0 and intersect<=1.0:
            ipoint = interpolate(prev,point,intersect)
        else:
            ipoint = tuple(point)
        subpoly.append( ipoint )
        
        print subpoly
        print currentside, pointside
        
        if currentside==0:
            currentside = pointside
        print currentside, pointside
        
        if pointside * currentside < 0.0:  # different signs, we've switched sides
            print "switching", currentside, pointside, subpoly
            if currentside<0.0:
                normpoly.extend(subpoly)
                print "N",normpoly
            else:
                foldpoly.extend(subpoly)
                print "F",foldpoly
                
            subpoly = [ipoint,point]
            currentside = pointside
        
        prev=point

    if currentside<0.0:
        normpoly.extend(subpoly)
    else:
        foldpoly.extend(subpoly)
    
    print
    print "N=",normpoly
    print "F=",foldpoly
        
    for i in range(0,len(foldpoly)):
        foldpoly[i] = reflect(foldpoly[i],foldline)

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



if __name__ == '__main__':
    from Kamaelia.Community.THF.Kamaelia.UI.OpenGL.SkyGrassBackground import SkyGrassBackground

    SkyGrassBackground(size=(5000,5000,0), position=(0,0,-100)).activate()
    SimpleFold(position=(0,0,-22), size=(10,10,2)).run()
