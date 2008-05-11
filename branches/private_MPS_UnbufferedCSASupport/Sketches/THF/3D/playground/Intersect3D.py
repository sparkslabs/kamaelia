#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
