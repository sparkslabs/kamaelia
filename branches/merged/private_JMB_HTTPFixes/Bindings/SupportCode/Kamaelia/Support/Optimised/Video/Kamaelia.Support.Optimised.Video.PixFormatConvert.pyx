# (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#
# Pyrex wrapper for simple YUV422 to RGB conversion functions

cdef extern from "_PixFormatConvertCore.c":
    cdef int RGB_to_YUV420(unsigned char *rgb_input, unsigned char *y_output, unsigned char *u_output, unsigned char *v_output, int width, int height)
    
    cdef int YUV422_to_RGB(unsigned char *y_input, unsigned char *u_input, unsigned char *v_input, unsigned char *rgb_output, int width, int height)

    cdef int YUV420_to_RGB(unsigned char *y_input, unsigned char *u_input, unsigned char *v_input, unsigned char *rgb_output, int width, int height)



cdef extern from "Python.h": 
    object PyString_FromStringAndSize(char *, int)
    cdef char* PyString_AsString(object)

#-------------------------------------------------------------------------------

def rgbi_to_yuv420p(rgb, width, height):
    cdef unsigned char *ychr
    cdef unsigned char *uchr
    cdef unsigned char *vchr
    cdef unsigned char *rgbchr

    y = PyString_FromStringAndSize(NULL, (width*height))
    u = PyString_FromStringAndSize(NULL, ((width>>1)*(height>>1)))
    v = PyString_FromStringAndSize(NULL, ((width>>1)*(height>>1)))

    ychr = <unsigned char *>PyString_AsString(y)
    uchr = <unsigned char *>PyString_AsString(u)
    vchr = <unsigned char *>PyString_AsString(v)

    rgbchr = <unsigned char *>PyString_AsString(rgb)
    
    RGB_to_YUV420(rgbchr, ychr,uchr,vchr, width, height)

    return y,u,v

def yuv422p_to_rgbi(y,u,v, width, height):
    cdef unsigned char *ychr
    cdef unsigned char *uchr
    cdef unsigned char *vchr
    cdef unsigned char *rgbchr

    rgb = PyString_FromStringAndSize(NULL, (width*height*3))

    ychr = <unsigned char *>PyString_AsString(y)
    uchr = <unsigned char *>PyString_AsString(u)
    vchr = <unsigned char *>PyString_AsString(v)

    rgbchr = <unsigned char *>PyString_AsString(rgb)
    
    YUV422_to_RGB(ychr,uchr,vchr, rgbchr, width, height)

    return rgb

def yuv420p_to_rgbi(y,u,v, width, height):
    cdef unsigned char *ychr
    cdef unsigned char *uchr
    cdef unsigned char *vchr
    cdef unsigned char *rgbchr

    rgb = PyString_FromStringAndSize(NULL, (width*height*3))

    ychr = <unsigned char *>PyString_AsString(y)
    uchr = <unsigned char *>PyString_AsString(u)
    vchr = <unsigned char *>PyString_AsString(v)

    rgbchr = <unsigned char *>PyString_AsString(rgb)
    
    YUV420_to_RGB(ychr,uchr,vchr, rgbchr, width, height)

    return rgb
    