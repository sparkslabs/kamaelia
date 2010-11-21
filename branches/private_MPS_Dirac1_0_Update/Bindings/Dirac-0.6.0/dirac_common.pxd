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

cdef extern from "dirac/libdirac_common/common_types.h":

    ctypedef enum ChromaFormat:
        format444
        format422
        format420
        formatNK

    ctypedef enum WltFilter:
        DD9_7=0
        LEGALL5_3
        DD13_7
        HAAR0
        HAAR1
        FIDELITY
        DAUB9_7
        filterNK

    ctypedef enum PrefilterType:
        NO_PF=0
        DIAGLP
        RECTLP
        CWM

    static const int NUM_WLT_FILTERS = 8 ### FIXME

    ctypedef enum PictureType:
        INTRA_PICTURE = 0
        INTER_PICTURE

    ctypedef enum ReferenceType:
        REFERENCE_PICTURE = 0
        NON_REFERENCE_PICTURE

    ctypedef enum VideoFormat:
        VIDEO_FORMAT_CUSTOM=0
        VIDEO_FORMAT_QSIF525
        VIDEO_FORMAT_QCIF
        VIDEO_FORMAT_SIF525
        VIDEO_FORMAT_CIF
        VIDEO_FORMAT_4SIF525
        VIDEO_FORMAT_4CIF
        VIDEO_FORMAT_SD_480I60
        VIDEO_FORMAT_SD_576I50
        VIDEO_FORMAT_HD_720P60
        VIDEO_FORMAT_HD_720P50
        VIDEO_FORMAT_HD_1080I60
        VIDEO_FORMAT_HD_1080I50
        VIDEO_FORMAT_HD_1080P60
        VIDEO_FORMAT_HD_1080P50
        VIDEO_FORMAT_DIGI_CINEMA_2K24
        VIDEO_FORMAT_DIGI_CINEMA_4K24
        VIDEO_FORMAT_UHDTV_4K60
        VIDEO_FORMAT_UHDTV_4K50
        VIDEO_FORMAT_UHDTV_8K60
        VIDEO_FORMAT_UHDTV_8K50
        VIDEO_FORMAT_UNDEFINED

    # Types of Colour primaries
    ctypedef enum ColourPrimaries:
        CP_HDTV_COMP_INTERNET=0
        CP_SDTV_525
        CP_SDTV_625
        CP_DCINEMA
        CP_UNDEF

    ctypedef enum ColourMatrix:
        CM_HDTV_COMP_INTERNET=0
        CM_SDTV
        CM_REVERSIBLE
        CM_UNDEF

    ctypedef enum TransferFunction:
        TF_TV=0
        TF_EXT_GAMUT
        TF_LINEAR
        TF_DCINEMA
        TF_UNDEF

    ctypedef enum FrameRateType:
        FRAMERATE_CUSTOM=0
        FRAMERATE_23p97_FPS
        FRAMERATE_24_FPS
        FRAMERATE_25_FPS
        FRAMERATE_29p97_FPS
        FRAMERATE_30_FPS
        FRAMERATE_50_FPS
        FRAMERATE_59p94_FPS
        FRAMERATE_60_FPS
        FRAMERATE_14p98_FPS
        FRAMERATE_12p5_FPS
        FRAMERATE_UNDEFINED

    ctypedef enum PixelAspectRatioType:
        PIXEL_ASPECT_RATIO_CUSTOM=0
        PIXEL_ASPECT_RATIO_1_1
        PIXEL_ASPECT_RATIO_10_11
        PIXEL_ASPECT_RATIO_12_11
        PIXEL_ASPECT_RATIO_40_33
        PIXEL_ASPECT_RATIO_16_11
        PIXEL_ASPECT_RATIO_4_3
        PIXEL_ASPECT_RATIO_UNDEFINED

    ctypedef enum SignalRangeType:
        SIGNAL_RANGE_CUSTOM=0
        SIGNAL_RANGE_8BIT_FULL
        SIGNAL_RANGE_8BIT_VIDEO
        SIGNAL_RANGE_10BIT_VIDEO
        SIGNAL_RANGE_12BIT_VIDEO
        SIGNAL_RANGE_UNDEFINED

#
# APPEARS TO HAVE DISAPPEARED NOW
#
#    ctypedef enum InterlaceType: ### FIXME: Where is this now?
#        IT_PROGRESSIVE
#        IT_INTERLACED_TFF
#        IT_INTERLACED_BFF
#        IT_UNDEF

    ctypedef enum MVPrecisionType:
        MV_PRECISION_PIXEL=0
        MV_PRECISION_HALF_PIXEL
        MV_PRECISION_QUARTER_PIXEL
        MV_PRECISION_EIGHTH_PIXEL
        MV_PRECISION_UNDEFINED

    # Type of quantiser modes when spatial partitioning is enabled
    ctypedef enum CodeBlockMode:
        QUANT_SINGLE,
        QUANT_MULTIPLE,
        QUANT_UNDEF


cdef extern from "dirac/libdirac_common/dirac_types.h":

    ctypedef ChromaFormat dirac_chroma_t
    ctypedef PictureType dirac_picture_type_t
    ctypedef ReferenceType dirac_reference_type_t
    ctypedef WltFilter dirac_wlt_filter_t

    ctypedef struct dirac_rational_t:
        int numerator;
        int denominator;

    typedef dirac_rational_t dirac_frame_rate_t;
    typedef dirac_rational_t dirac_pix_asr_t;

    ctypedef struct dirac_parseparams_t:
        unsigned int major_ver
        unsigned int minor_ver
        unsigned int profile
        unsigned int level

#
# APPEARS TO HAVE DISAPPEARED NOW
#
#    ctypedef struct dirac_seqparams_t:  ### FIXME: Where is this now?
#        int                width
#        int                height
#        dirac_chroma_t     chroma
#        int                chroma_width
#        int                chroma_height
#        int                video_depth

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
        float kr;
        float kb;

    ctypedef ColourPrimaries dirac_col_primaries_t
    ctypedef TransferFunction dirac_transfer_func_t

    ctypedef struct dirac_colour_spec_t:
        dirac_col_primaries_t col_primary
        dirac_col_matrix_t col_matrix
        dirac_transfer_func_t trans_func

    # Structure that holds the source parameters
    ctypedef struct dirac_sourceparams_t:
        unsigned int         width
        unsigned int         height
        dirac_chroma_t       chroma
        unsigned int         chroma_width
        unsigned int         chroma_height
        unsigned int         source_sampling  # 0 - progressive; 1 - interlaced
        int                  topfieldfirst    # 0 - false; 1 - true (lib sets)
        dirac_frame_rate_t   frame_rate
        dirac_pix_asr_t      pix_asr          # pixel aspect ratio
        dirac_clean_area_t   clean_area
        dirac_signal_range_t signal_range
        dirac_colour_spec_t  colour_spec

    # Structure that holds the picture parameters
    ctypedef struct dirac_picparams_t:
        dirac_picture_type_t ptype
        dirac_reference_type_t rtype
        int pnum

    # Structure that holds the frame buffers into which data is written 
    # NB we have frame-oriented IO even though we code pictures
    ctypedef struct dirac_framebuf_t:
        # buffers to hold the luma and chroma data
        unsigned char  *buf[3]
        void  *id                # User data
