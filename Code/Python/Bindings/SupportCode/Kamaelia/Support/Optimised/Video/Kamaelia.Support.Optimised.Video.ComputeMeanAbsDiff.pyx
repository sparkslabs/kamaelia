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


cdef extern from "Python.h": 
    object PyString_FromStringAndSize(char *, int)
    cdef char* PyString_AsString(object)


cdef double ComputeMAD(unsigned char *prev, unsigned char *curr, int size):
    cdef unsigned int total

    cdef unsigned char *prevpixel
    cdef unsigned char *currpixel

    total=0
    prevpixel = prev + size
    currpixel = curr + size

    while (prevpixel > prev):
        currpixel=currpixel-1
        prevpixel=prevpixel-1

        if prevpixel[0] > currpixel[0]:
            total = total + (prevpixel[0] - currpixel[0])
        else:
            total = total + (currpixel[0] - prevpixel[0])
    
    return (<double>total) / (<double>(size))
    

def ComputeMeanAbsDiff(ydata1,ydata2):
    cdef unsigned char *y1
    cdef unsigned char *y2

    y1 = <unsigned char *>PyString_AsString(ydata1)
    y2 = <unsigned char *>PyString_AsString(ydata2)

    return ComputeMAD(y1, y2, len(ydata1))
