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

from math import sin, cos, pi

class Transform:
    def __init__(self):
        # load identity
        self.m = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]

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
#        print "mul", str(x.m)
        return x
        
    def getMatrix(self):
        return self.m
    
    def setIdentity(self):    
        self.m = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
    
    def applyRotation(self, xyzangle):
        global pi
        t = Transform()
        xyzangle = [x*2*pi/360 for x in xyzangle]
#        print "angles", str(xyzangle)
        #rotation around x axis
        if xyzangle[0] != 0:
            t.m[5] = cos(xyzangle[0])
            t.m[6] = sin(xyzangle[0])
            t.m[9] = -sin(xyzangle[0])
            t.m[10] = cos(xyzangle[0])
            self.m = (self*t).m
        #rotation around y axis
        if xyzangle[1] != 0:
            t.m[0] = cos(xyzangle[1])
            t.m[2] = -sin(xyzangle[1])
            t.m[8] = sin(xyzangle[1])
            t.m[10] = cos(xyzangle[1])
            self.m = (self*t).m
        #rotation around z axis
        if xyzangle[2] != 0:
            t.m[0] = cos(xyzangle[2])
            t.m[1] = sin(xyzangle[2])
            t.m[4] = -sin(xyzangle[2])
            t.m[5] = cos(xyzangle[2])
            self.m = (self*t).m
    
    def applyTranslation(self, vector):
        t = Transform()
        if (vector[0] != 0 and vector[1] != 0 and vector[2] != 0):
            t.m[12] = vector[0]
            t.m[13] = vector[1]
            t.m[14] = vector[2]
#            print "translation", str(t.m)
            self.m = (self*t).m
        
    def applyScaling(self, vector):
        t = Transform()
        if (vector[0] != 0 and vector[1] != 0 and vector[2] != 0):
            t.m[0] = vector[0]
            t.m[5] = vector[1]
            t.m[10] = vector[2]
            self.m = (self*t).m
        
    # Vector multiplication
    def transformVertex(self, v):
#        print "transform", str(self.m)
        return [self.m[0]*v[0] + self.m[4]*v[1] + self.m[8]*v[2] + self.m[12],
                     self.m[1]*v[0] + self.m[5]*v[1] + self.m[9]*v[2] + self.m[13],
                     self.m[2]*v[0] + self.m[6]*v[1] + self.m[10]*v[2] + self.m[14] ]


if __name__=='__main__':
    # Test for Transform (not very exhaustive :)
    print "Testing transform..."
    t = Transform()
    v = [0,0,0]
    t.applyTranslation([1,2,3])
    vt = t.transformVertex(v)
    print str(vt), "(1,2,3 expected)"
    t.setIdentity();
    t.applyRotation([90,0,0])
    print str(t.transformVertex(vt)), "(1,-3,2 expected)"
    v1 = [1,0,0]
    t.setIdentity();
    t.applyRotation([0,0,90])
    print str(t.transformVertex(v1)), "(0,1,0 expected)"
    v2 = [1, -2, 3]
    t.setIdentity();
    t.applyScaling([2,3,1])
    print str(t.transformVertex(v2)), "(2,-6,3 expected)"
    
