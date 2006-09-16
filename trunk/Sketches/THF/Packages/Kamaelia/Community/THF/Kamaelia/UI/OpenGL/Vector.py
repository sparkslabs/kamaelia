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
===============
3D Vector class
===============

A class for 3 dimensional vectors providing several methods for common
vector operations.
"""

from math import *


# =====================
# Vector: used for handling 3D Vectors
# =====================
class Vector:
    """\
    Vector([x][,y][,z]) -> A new Vector object.
    
    Keyword arguments:
    
    - x,y,z -- Initial values.
    """
    def __init__(self, x=0.0, y=0.0, z=0.0):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def zero(self):
        """ Set all values to zero. """
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        return self
        
    def invert(self):
        """ Changes the sign of each vector component. """
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

    def copy(self):
        """ Returns a copy of the Vector object. """
        return Vector(self.x,self.y,self.z)
        
    def toTuple(self):
        """ Returns a tuple (x,y,z). """
        return (self.x,self.y,self.z)
    
    def length(self):
        """ Returns the length of the vector. """
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def dot(self, other):
        """ Returns the dot product between self and other. """
        return self.x*other.x + self.y*other.y + self.z*other.z
        
    def cross(self, other):
        """ Returns the cross product between self and other. """
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)
         
    def norm(self):
        """ Returns a normalised version of the vector. """
        l = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        return Vector(self.x / l, self.y / l, self.z / l)
        
    def __str__(self):
        return str([self.x,self.y,self.z])

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False

    def __ne__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return False
        return True
        
    def __mul__(self, factor):
        return Vector(self.x * factor, self.y * factor, self.z * factor)

    def __div__(self, factor):
        return Vector(self.x / factor, self.y / factor, self.z / factor)

    def __mod__(self, factor):
        return Vector(self.x % factor, self.y % factor, self.z % factor)

    def __add__(self, other):
        return Vector(self.x +other.x, self.y +other.y, self.z +other.z)  

    def __sub__(self, other):
        return Vector(self.x -other.x, self.y -other.y, self.z-other.z)

    def __imul__(self, factor):
        return Vector(self.x * factor, self.y * factor, self.z * factor)

    def __idiv__(self, factor):
        return Vector(self.x / factor, self.y / factor, self.z / factor)

    def __imod__(self, factor):
        return Vector(self.x % factor, self.y % factor, self.z % factor)

    def __iadd__(self, other):
        return Vector(self.x +other.x, self.y +other.y, self.z +other.z)  

    def __isub__(self, other):
        return Vector(self.x -other.x, self.y -other.y, self.z-other.z)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
# Licensed to the BBC under a Contributor Agreement: THF
