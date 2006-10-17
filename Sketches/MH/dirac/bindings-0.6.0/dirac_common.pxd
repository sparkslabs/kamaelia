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

cdef extern from "dirac/libdirac_common/common_types.h":

    ctypedef enum ChromaFormat:
        format444
        format422
        format420
        formatNK

    ctypedef enum WltFilter:
        APPROX97 = 0
        FIVETHREE
        THIRTEENFIVE
        HAAR
        RESERVED1
        RESERVED2
        DAUB97
        filterNK

    ctypedef enum FrameType:
        INTRA_FRAME = 0
        INTER_FRAME

    ctypedef enum ReferenceType:
        REFERENCE_FRAME = 0
        NON_REFERENCE_FRAME

    ctypedef enum VideoFormat:
        VIDEO_FORMAT_CUSTOM = 0
        VIDEO_FORMAT_QSIF
        VIDEO_FORMAT_QCIF
        VIDEO_FORMAT_SIF
        VIDEO_FORMAT_CIF
        VIDEO_FORMAT_4CIF
        VIDEO_FORMAT_4SIF
        VIDEO_FORMAT_SD_525_DIGITAL
        VIDEO_FORMAT_SD_625_DIGITAL
        VIDEO_FORMAT_HD_720
        VIDEO_FORMAT_HD_1080
        VIDEO_FORMAT_DIGI_CINEMA_2K
        VIDEO_FORMAT_DIGI_CINEMA_4K
        VIDEO_FORMAT_UNDEFINED

    # Types of Colour primaries
    ctypedef enum ColourPrimaries:
        CP_ITU_709 = 0
        CP_SMPTE_C
        CP_EBU_3213
        CP_CIE_XYZ
        CP_UNDEF

    ctypedef enum ColourMatrix:
        CM_HDTV_COMP_INTERNET = 0
        CM_SDTV
        CM_DCINEMA
        CM_UNDEF

    ctypedef enum TransferFunction:
        TF_TV=0
        TF_EXT_GAMUT
        TF_LINEAR
        TF_DCINEMA
        TF_UNDEF

    ctypedef enum FrameRateType:
        FRAMERATE_CUSTOM = 0
        FRAMERATE_23p97_FPS
        FRAMERATE_24_FPS
        FRAMERATE_25_FPS
        FRAMERATE_29p97_FPS
        FRAMERATE_30_FPS
        FRAMERATE_50_FPS
        FRAMERATE_59p94_FPS
        FRAMERATE_60_FPS
        FRAMERATE_UNDEFINED

    ctypedef enum AspectRatioType:
        ASPECT_RATIO_CUSTOM = 0
        ASPECT_RATIO_1_1
        ASPECT_RATIO_10_11
        ASPECT_RATIO_12_11
        ASPECT_RATIO_UNDEFINED

    ctypedef enum SignalRangeType:
        SIGNAL_RANGE_CUSTOM
        SIGNAL_RANGE_8BIT_FULL
        SIGNAL_RANGE_8BIT_VIDEO
        SIGNAL_RANGE_10BIT_VIDEO
        SIGNAL_RANGE_UNDEFINED

    ctypedef enum InterlaceType:
        IT_PROGRESSIVE
        IT_INTERLACED_TFF
        IT_INTERLACED_BFF
        IT_UNDEF

    ctypedef enum MVPrecisionType:
        MV_PRECISION_PIXEL
        MV_PRECISION_HALF_PIXEL
        MV_PRECISION_QUARTER_PIXEL
        MV_PRECISION_EIGHTH_PIXEL
        MV_PRECISION_UNDEFINED

    ctypedef enum CodeBlockMode:
        QUANT_SINGLE
        QUANT_MULTIPLE
        QUANT_UNDEF



cdef extern from "dirac/libdirac_common/dirac_types.h":

    ctypedef ChromaFormat dirac_chroma_t
    ctypedef FrameType dirac_frame_type_t
    ctypedef ReferenceType dirac_reference_type_t
    ctypedef WltFilter dirac_wlt_filter_t

    ctypedef struct dirac_rational_t:
        int numerator
        int denominator

    ctypedef dirac_rational_t dirac_frame_rate_t
    ctypedef dirac_rational_t dirac_asr_rate_t

    ctypedef struct dirac_parseparams_t:
        unsigned int au_pnum
        unsigned int major_ver
        unsigned int minor_ver
        unsigned int profile
        unsigned int level

    ctypedef struct dirac_seqparams_t:
        int                width
        int                height
        dirac_chroma_t     chroma
        int                chroma_width
        int                chroma_height
        int                video_depth

    ctypedef struct dirac_clean_area_t:
        unsigned int width
        unsigned int height
        unsigned int left_offset
        unsigned int top_offset

    ctypedef struct dirac_signal_range_t:
        unsigned int luma_offset
        unsigned int luma_excursion
        unsigned int chroma_offset
        unsigned int chroma_excursion

    ctypedef struct dirac_col_matrix_t:
        float kr
        float kb

    ctypedef ColourPrimaries  dirac_col_primaries_t
    ctypedef TransferFunction dirac_transfer_func_t

    ctypedef struct dirac_colour_spec_t:
        dirac_col_primaries_t col_primary
        dirac_col_matrix_t    col_matrix
        dirac_transfer_func_t trans_func


    # Structure that holds the source parameters
    ctypedef struct dirac_sourceparams_t:
        int                  interlace
        int                  topfieldfirst
        int                  seqfields
        dirac_frame_rate_t   frame_rate
        dirac_frame_rate_t   pix_asr
        dirac_clean_area_t   clean_area
        dirac_signal_range_t signal_range
        dirac_colour_spec_t  colour_spec

    # Structure that holds the frame parameters
    ctypedef struct dirac_frameparams_t:
        dirac_frame_type_t     ftype
        dirac_reference_type_t rtype
        int                    fnum

    ctypedef struct dirac_framebuf_t:
        unsigned char *buf[3]
        void          *id

