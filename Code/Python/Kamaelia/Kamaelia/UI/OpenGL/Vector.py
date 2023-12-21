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
===============
3D Vector class
===============

A class for 3 dimensional vectors providing several methods for common
vector operations.
"""

import math

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
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def dot(self, other):
        """ Returns the dot product between self and other. """
        return self.x*other.x + self.y*other.y + self.z*other.z
        
    def cross(self, other):
        """ Returns the cross product between self and other. """
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)
         
    def norm(self):
        """ Returns a normalised version of the vector. """
        l = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
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
