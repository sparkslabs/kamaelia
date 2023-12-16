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
#
# Pyrex wrapper for simple YUV422 to RGB conversion functions

cdef extern from "_PixFormatConvertCore.c":
    cdef int RGB_to_YUV420(unsigned char *rgb_input, unsigned char *y_output, unsigned char *u_output, unsigned char *v_output, int width, int height)
    
    cdef int YUV422_to_RGB(unsigned char *y_input, unsigned char *u_input, unsigned char *v_input, unsigned char *rgb_output, int width, int height)

    cdef int YUV420_to_RGB(unsigned char *y_input, unsigned char *u_input, unsigned char *v_input, unsigned char *rgb_output, int width, int height)



cdef extern from "Python.h": 
    object PyUnicode_FromStringAndSize(char *, int)
    cdef char* PyUnicode_AsUTF8(object)

#-------------------------------------------------------------------------------

def rgbi_to_yuv420p(rgb, width, height):
    cdef unsigned char *ychr
    cdef unsigned char *uchr
    cdef unsigned char *vchr
    cdef unsigned char *rgbchr

    y = PyUnicode_FromStringAndSize(NULL, (width*height))
    u = PyUnicode_FromStringAndSize(NULL, ((width>>1)*(height>>1)))
    v = PyUnicode_FromStringAndSize(NULL, ((width>>1)*(height>>1)))

    ychr = <unsigned char *>PyUnicode_AsUTF8(y)
    uchr = <unsigned char *>PyUnicode_AsUTF8(u)
    vchr = <unsigned char *>PyUnicode_AsUTF8(v)

    rgbchr = <unsigned char *>PyUnicode_AsUTF8(rgb)
    
    RGB_to_YUV420(rgbchr, ychr,uchr,vchr, width, height)

    return y,u,v

def yuv422p_to_rgbi(y,u,v, width, height):
    cdef unsigned char *ychr
    cdef unsigned char *uchr
    cdef unsigned char *vchr
    cdef unsigned char *rgbchr

    rgb = PyUnicode_FromStringAndSize(NULL, (width*height*3))

    ychr = <unsigned char *>PyUnicode_AsUTF8(y)
    uchr = <unsigned char *>PyUnicode_AsUTF8(u)
    vchr = <unsigned char *>PyUnicode_AsUTF8(v)

    rgbchr = <unsigned char *>PyUnicode_AsUTF8(rgb)
    
    YUV422_to_RGB(ychr,uchr,vchr, rgbchr, width, height)

    return rgb

def yuv420p_to_rgbi(y,u,v, width, height):
    cdef unsigned char *ychr
    cdef unsigned char *uchr
    cdef unsigned char *vchr
    cdef unsigned char *rgbchr

    rgb = PyUnicode_FromStringAndSize(NULL, (width*height*3))

    ychr = <unsigned char *>PyUnicode_AsUTF8(y)
    uchr = <unsigned char *>PyUnicode_AsUTF8(u)
    vchr = <unsigned char *>PyUnicode_AsUTF8(v)

    rgbchr = <unsigned char *>PyUnicode_AsUTF8(rgb)
    
    YUV420_to_RGB(ychr,uchr,vchr, rgbchr, width, height)

    return rgb
    
