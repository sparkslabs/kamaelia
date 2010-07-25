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
#
# Pyrex wrapper for Dirac video codec 'common' header files
#
# Dirac is an open source video codec.
# Obtain it from http://dirac.sourceforge.net/
#

cdef extern from "dirac/libdirac_common/dirac_types.h":

    ctypedef enum dirac_chroma_t:
        Yonly
        format422
        format444
        format420
        format411
        formatNK

    ctypedef enum dirac_frame_type_t:
        I_frame
        L1_frame
        L2_frame

    ctypedef struct dirac_rational_t:
        int numerator
        int denominator

    ctypedef dirac_rational_t dirac_frame_rate_t

    ctypedef struct dirac_seqparams_t:
        int                width
        int                height
        dirac_chroma_t     chroma
        int                chroma_width
        int                chroma_height
        dirac_frame_rate_t frame_rate
        int                interlace
        int                topfieldfirst

    ctypedef struct dirac_frameparams_t:
        dirac_frame_type_t ftype
        int                fnum

    ctypedef struct dirac_framebuf_t:
        unsigned char *buf[3]
        void          *id

