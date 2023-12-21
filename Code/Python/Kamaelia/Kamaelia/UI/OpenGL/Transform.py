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
==================
3D Transform class
==================

A class containing a transformation matrix and providing several methods
to use/alter it. Transform uses Vector objects for most of its methods
arguments.
"""

import math
from .Vector import Vector

# =============================
# Transform: for generating transformation matrices
# =============================
class Transform:
    """\
    Transform([matrix]) -> new Transform object.
    
    Keyword arguments:
    
    - m   -- A matrix containing values to be initially set
    """

    def __init__(self, m = None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        # load identity
        if m is not None:
            self.m = m
        else:
            self.m = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]

    def getMatrix(self):
        """ Returns the transformation matrix. """
        return self.m
    
    def reset(self):    
        """ Resets to identity matrix. """
        self.m = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
    
    def applyRotation(self, xyzangle):
        """\
        Apply a rotation.

        Arguments:
        - xyzangle -- A Vector containing the amount of rotation around each axis.
        """

        t = Transform()
        # convert degrees to radiant
        xyzangle *= math.pi/180.0
        #rotation around x axis
        if xyzangle.x != 0:
            t.m[5] = math.cos(xyzangle.x)
            t.m[6] = math.sin(xyzangle.x)
            t.m[9] = -math.sin(xyzangle.x)
            t.m[10] = math.cos(xyzangle.x)
            self.m = (self*t).m
        #rotation around y axis
        t.reset()
        if xyzangle.y != 0:
            t.m[0] = math.cos(xyzangle.y)
            t.m[2] = -math.sin(xyzangle.y)
            t.m[8] = math.sin(xyzangle.y)
            t.m[10] = math.cos(xyzangle.y)
            self.m = (self*t).m
        #rotation around z axis
        t.reset()
        if xyzangle.z != 0:
            t.m[0] = math.cos(xyzangle.z)
            t.m[1] = math.sin(xyzangle.z)
            t.m[4] = -math.sin(xyzangle.z)
            t.m[5] = math.cos(xyzangle.z)
            self.m = (self*t).m
    
    def applyTranslation(self, vector):
        """\
        Apply a translation.

        Arguments:
        - vector -- A Vector containing the amount of translation.
        """
        t = Transform()
        if (vector.x != 0 or vector.y != 0 or vector.z != 0):
            t.m[12] = vector.x
            t.m[13] = vector.y
            t.m[14] = vector.z
            self.m = (self*t).m
        
    def applyScaling(self, vector):
        """\
        Apply scaling.

        Arguments:
        - vector -- A Vector containing the amount of scaling for each axis.
        """
        t = Transform()
        if (vector.x != 0 or vector.y != 0 or vector.z != 0):
            t.m[0] = vector.x
            t.m[5] = vector.y
            t.m[10] = vector.z
            self.m = (self*t).m
            
    def setLookAtRotation(self, eye, center, up):
        """\
        Generates a "look at" transform.

        Arguments:
        - eye       -- A Vector with viewer origin.
        - center    -- A Vector with point the viewer looks at.
        - up        -- The viewers up Vector.
        """

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
        """\
        Transforms a Vector v.
        
        Returns the transformed Vector.
        """
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
# Licensed to the BBC under a Contributor Agreement: THF
