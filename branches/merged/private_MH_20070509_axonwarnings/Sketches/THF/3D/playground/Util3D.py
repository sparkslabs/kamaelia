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
=====================
3D Utility library
=====================
TODO
"""

from math import *


# =========================
# Control3D contains movement commands
# =========================
class Control3D:
    POSITION, REL_POSITION, ROTATION, REL_ROTATION, SCALING, REL_SCALING = range(6)
    def __init__(self, type, amount):
        # Command types
        self.type = type
        self.amount = amount

# =====================
# Vector: used for handling 3D Vectors
# =====================
class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def zero(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        return self
        
    def invert(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

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
        
    def copy(self):
        return Vector(self.x,self.y,self.z)
        
    def getTuple():
        return (self.x,self.y,self.z)
    
    def length(self):
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z
        
    def cross(self, other):
         return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)
         
    def norm(self):
        l = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        self.x /= l
        self.y /= l
        self.z /= l
        return self
        
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

        
# =============================
# Transform: for generating transformation matrices
# =============================
class Transform:
    def __init__(self):
        # load identity
        self.m = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]

    # return transformation matrix
    def getMatrix(self):
        return self.m
    
    # reset to identity matrix
    def reset(self):    
        self.m = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
    
    def applyRotation(self, xyzangle):
        global pi
        t = Transform()
        # convert degrees to radiant
        xyzangle *= pi/180.0
        #rotation around x axis
        if xyzangle.x != 0:
            t.m[5] = cos(xyzangle.x)
            t.m[6] = sin(xyzangle.x)
            t.m[9] = -sin(xyzangle.x)
            t.m[10] = cos(xyzangle.x)
            self.m = (self*t).m
        #rotation around y axis
        t.reset()
        if xyzangle.y != 0:
            t.m[0] = cos(xyzangle.y)
            t.m[2] = -sin(xyzangle.y)
            t.m[8] = sin(xyzangle.y)
            t.m[10] = cos(xyzangle.y)
            self.m = (self*t).m
        #rotation around z axis
        t.reset()
        if xyzangle.z != 0:
            t.m[0] = cos(xyzangle.z)
            t.m[1] = sin(xyzangle.z)
            t.m[4] = -sin(xyzangle.z)
            t.m[5] = cos(xyzangle.z)
            self.m = (self*t).m
    
    def applyTranslation(self, vector):
        t = Transform()
        if (vector.x != 0 or vector.y != 0 or vector.z != 0):
            t.m[12] = vector.x
            t.m[13] = vector.y
            t.m[14] = vector.z
            self.m = (self*t).m
        
    def applyScaling(self, vector):
        t = Transform()
        if (vector.x != 0 or vector.y != 0 or vector.z != 0):
            t.m[0] = vector.x
            t.m[5] = vector.y
            t.m[10] = vector.z
            self.m = (self*t).m
        
    # Vector multiplication
    def transformVector(self, v):
        return Vector(self.m[0]*v.x + self.m[4]*v.y + self.m[8]*v.z + self.m[12],
                                self.m[1]*v.x + self.m[5]*v.y + self.m[9]*v.z + self.m[13],
                                self.m[2]*v.x + self.m[6]*v.y + self.m[10]*v.z + self.m[14])

    # Matrix multiplication
    def __mul__(self,other):
        x = Transform()
        
        x.m[0] = self.m[0]*other.m[0] + self.m[1]*other.m[4] + self.m[2]*other.m[8] + self.m[3]*other.m[12];
        x.m[1] = self.m[0]*other.m[1] + self.m[1]*other.m[5] + self.m[2]*other.m[9] + self.m[3]*other.m[13];
        x.m[2] = self.m[0]*other.m[2] + self.m[1]*other.m[6] + self.m[2]*other.m[10] + self.m[3]*other.m[14];
        x.m[3] = self.m[0]*other.m[3] + self.m[1]*other.m[7] + self.m[2]*other.m[11] + self.m[3]*other.m[15];

        x.m[4] = self.m[4]*other.m[0] + self.m[5]*other.m[4] + self.m[6]*other.m[8] + self.m[7]*other.m[12];
        x.m[5] = self.m[4]*other.m[1] + self.m[5]*other.m[5] + self.m[6]*other.m[9] + self.m[7]*other.m[13];
        x.m[6] = self.m[4]*other.m[2] + self.m[5]*other.m[6] + self.m[6]*other.m[10] + self.m[7]*other.m[14];
        x.m[7] = self.m[4]*other.m[3] + self.m[5]*other.m[7] + self.m[6]*other.m[11] + self.m[7]*other.m[15];

        x.m[8] = self.m[8]*other.m[0] + self.m[9]*other.m[4] + self.m[10]*other.m[8] + self.m[11]*other.m[12];
        x.m[9] = self.m[8]*other.m[1] + self.m[9]*other.m[5] + self.m[10]*other.m[9] + self.m[11]*other.m[13];
        x.m[10] = self.m[8]*other.m[2] + self.m[9]*other.m[6] + self.m[10]*other.m[10] + self.m[11]*other.m[14];
        x.m[11] = self.m[8]*other.m[3] + self.m[9]*other.m[7] + self.m[10]*other.m[11] + self.m[11]*other.m[15];

        x.m[12] = self.m[12]*other.m[0] + self.m[13]*other.m[4] + self.m[14]*other.m[8] + self.m[15]*other.m[12];
        x.m[13] = self.m[12]*other.m[1] + self.m[13]*other.m[5] + self.m[14]*other.m[9] + self.m[15]*other.m[13];
        x.m[14] = self.m[12]*other.m[2] + self.m[13]*other.m[6] + self.m[14]*other.m[10] + self.m[15]*other.m[14];
        x.m[15] = self.m[12]*other.m[3] + self.m[13]*other.m[7] + self.m[14]*other.m[11] + self.m[15]*other.m[15];
        return x

    # Immediate matrix multiplication
    def __imul__(self,other):
        x = Transform()
        
        x.m[0] = self.m[0]*other.m[0] + self.m[1]*other.m[4] + self.m[2]*other.m[8] + self.m[3]*other.m[12];
        x.m[1] = self.m[0]*other.m[1] + self.m[1]*other.m[5] + self.m[2]*other.m[9] + self.m[3]*other.m[13];
        x.m[2] = self.m[0]*other.m[2] + self.m[1]*other.m[6] + self.m[2]*other.m[10] + self.m[3]*other.m[14];
        x.m[3] = self.m[0]*other.m[3] + self.m[1]*other.m[7] + self.m[2]*other.m[11] + self.m[3]*other.m[15];

        x.m[4] = self.m[4]*other.m[0] + self.m[5]*other.m[4] + self.m[6]*other.m[8] + self.m[7]*other.m[12];
        x.m[5] = self.m[4]*other.m[1] + self.m[5]*other.m[5] + self.m[6]*other.m[9] + self.m[7]*other.m[13];
        x.m[6] = self.m[4]*other.m[2] + self.m[5]*other.m[6] + self.m[6]*other.m[10] + self.m[7]*other.m[14];
        x.m[7] = self.m[4]*other.m[3] + self.m[5]*other.m[7] + self.m[6]*other.m[11] + self.m[7]*other.m[15];

        x.m[8] = self.m[8]*other.m[0] + self.m[9]*other.m[4] + self.m[10]*other.m[8] + self.m[11]*other.m[12];
        x.m[9] = self.m[8]*other.m[1] + self.m[9]*other.m[5] + self.m[10]*other.m[9] + self.m[11]*other.m[13];
        x.m[10] = self.m[8]*other.m[2] + self.m[9]*other.m[6] + self.m[10]*other.m[10] + self.m[11]*other.m[14];
        x.m[11] = self.m[8]*other.m[3] + self.m[9]*other.m[7] + self.m[10]*other.m[11] + self.m[11]*other.m[15];

        x.m[12] = self.m[12]*other.m[0] + self.m[13]*other.m[4] + self.m[14]*other.m[8] + self.m[15]*other.m[12];
        x.m[13] = self.m[12]*other.m[1] + self.m[13]*other.m[5] + self.m[14]*other.m[9] + self.m[15]*other.m[13];
        x.m[14] = self.m[12]*other.m[2] + self.m[13]*other.m[6] + self.m[14]*other.m[10] + self.m[15]*other.m[14];
        x.m[15] = self.m[12]*other.m[3] + self.m[13]*other.m[7] + self.m[14]*other.m[11] + self.m[15]*other.m[15];
        self.m = x.m


if __name__=='__main__':
    # Test for Transform (not very exhaustive :)
    print "Testing transform..."
    t = Transform()
    v = Vector(0,0,0)
    t.applyTranslation(Vector(1,2,3))
    vt = t.transformVector(v)
    print str(vt), "(1,2,3 expected)"
    t.reset();
    t.applyRotation(Vector(90,0,0))
    print str(t.transformVector(vt)), "(1,-3,2 expected)"
    t.reset();
    v1 = Vector(1,0,0)
    t.applyRotation(Vector(0,0,90))
    print str(t.transformVector(v1)), "(0,1,0 expected)"
    t.reset();
    v2 = Vector(1,-2,3)
    t.applyScaling(Vector(2,3,1))
    print str(t.transformVector(v2)), "(2,-6,3 expected)"
    print     
    
