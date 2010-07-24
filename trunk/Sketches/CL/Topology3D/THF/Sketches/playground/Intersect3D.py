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

from math import *

# ==================================
# Intersect3D: provides a set of static 3D intersection functions
# ==================================
class Intersect3D:
    """ Collection of intersection functions, """
    # very small value
    epsilon = 0.000000001
    
    def ray_OBB(r_origin, r_dir, b_pos, b_orientation, b_halflengths):
        """ Intersects a ray with an oriented bounding box. 
            r_origin = origin of the ray
            r_dir = normalized direction of the ray
            b_pos = position of the box
            b_orientation = list of normalised half length vectors of the box
            b_halflengths = list of positive half lengths of the box
            returns the distance from r_origin to the point of intersection
        """
        tmin = -10000
        tmax = 10000
        
        p = b_pos-r_origin
        for i in range(3):
            print "pos", str(p)
            a = b_orientation[i]-p
            print "a", a, a.length()
            h = b_halflengths[i]
            print "h", h
            e = a.dot(p)
            print "e", e
            f = a.dot(r_dir)
            print "f", f
            if abs(f)>Intersect3D.epsilon:
                t1 = (e+h)/f
                t2 = (e-h)/f
                if t1 > t2:
                    x = t1
                    t1 = t2
                    t2 = x
                print "t1", t1
                print "t2", t2
                if t1 > tmin: tmin = t1
                if t2 < tmax: tmax = t2
                print "tmin", tmin
                print "tmax", tmax
                if tmin > tmax: return 0
                if tmax < 0: return 0
            elif -e-h > 0 or -e+h < 0: return 0
        if tmin > 0: return tmin
        else: return tmax
    ray_OBB = staticmethod(ray_OBB)

    def ray_Plane(r_origin, r_dir, p_points):
        """ Intersects a ray with a plane.
            r_origin = origin of the ray
            r_dir = normalized direction of the ray
            points = list of 3 Vectors that represent non collinear points on the plane
            returns the distance from r_origin to the point of intersection
        """
        #determine the implicit equation of the plane
        p = p_points[0]
        n = (p_points[0]-p_points[2]).cross(p_points[1]-p_points[2])
        d = -n.dot(p)
        
        # test if the ray is parallel
        den = n.dot(r_dir)
        if abs(den)<Intersect3D.epsilon:
            return 0
        
        # calc distance to point of intersection
        nom = -d - n.dot(r_origin)
        return nom/den
    ray_Plane = staticmethod(ray_Plane)
    
    def ray_Polygon(r_origin, r_dir, p_points):
        """ Intersects a ray with a polygon.
            r_origin = origin of the ray
            r_dir = normalized direction of the ray
            points = list of Vectors that represent the points of the polygon
            returns the distance from r_origin to the point of intersection
        """
        #determine the implicit equation of the corresponding plane
        p = p_points[0]
        n = (p_points[0]-p_points[2]).cross(p_points[1]-p_points[2])
        d = -n.dot(p)
        
        # test if the ray is parallel
        den = n.dot(r_dir)
        if abs(den)<Intersect3D.epsilon:
            t = 0
        else:        
            # calc distance to point of intersection
            nom = -d - n.dot(r_origin)
            t = nom/den

        # determine point of intersection p
        if t==0:
            return 0
        p3d = r_origin+r_dir*t

        # project points of polyon to axis plane where polygon area is maximized
        maxn = max(abs(n.x), abs(n.y), abs(n.z))
        if abs(n.x) == maxn:
            points = [[point.y, point.z] for point in p_points]
            p = [p3d.y, p3d.z]
        elif abs(n.y) == maxn:
            points = [[point.x, point.z] for point in p_points]
            p = [p3d.x, p3d.z]
        elif abs(n.z) == maxn:
            points = [[point.x, point.y] for point in p_points]
            p = [p3d.x, p3d.y]
            
        # do crossings test
        inside = False
        e0 = points[-1]
        e1 = points[0]
        y0 = e0[1] >= p[1]
        for i in range(1, len(points)+1):
            y1 = e1[1] >= p[1]
            if y0 != y1:
                y2 = (e1[1]-p[1])*(e0[0]-e1[0]) >= (e1[0]-p[0])*(e0[1]-e1[1])
                if y2 == y1:
                    inside = not inside
            if i < len(points):
                y0 = y1
                e0 = e1
                e1 = points[i]
        
        # if inside return intersection distance
        if inside:
            return t
        else: return 0
    ray_Polygon = staticmethod(ray_Polygon)

    
    def ray_Sphere():
        pass
    
    def plane_OOB():    
        pass
    
    def OOB_OOB():
        pass
