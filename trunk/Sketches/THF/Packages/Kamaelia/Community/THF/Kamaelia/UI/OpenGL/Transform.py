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
3D Transform class
=====================
TODO
"""

from math import *
from Vector import Vector

# =============================
# Transform: for generating transformation matrices
# =============================
class Transform:
    def __init__(self, m = None):
        # load identity
        if m is not None:
            self.m = m
        else:
            self.m = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]

    # return transformation matrix
    def getMatrix(self):
        return self.m
    
    # reset to identity matrix
    def reset(self):    
        self.m = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
    
#    def copy(self):
#        return Transform(self.m)
    
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
            
    def setLookAtRotation(self, eye, center, up):
        # apply rotation
        z = -(center-eye).norm()
        x = up.cross(z).norm()
        y = z.cross(x)
        
        t = Transform()
        
        t.m[0] = x.x
        t.m[1] = y.x
        t.m[2] = z.x
        t.m[3] = 0.0
        
        t.m[4] = x.y
        t.m[5] = y.y
        t.m[6] = z.y
        t.m[7] = 0.0
        
        t.m[8] = x.z
        t.m[9] = y.z
        t.m[10] = z.z
        t.m[11] = 0.0

        t.m[12] = 0.0
        t.m[13] = 0.0
        t.m[14] = 0.0
        t.m[15] = 1.0

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
