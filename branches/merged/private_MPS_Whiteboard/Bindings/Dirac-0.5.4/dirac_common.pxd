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

