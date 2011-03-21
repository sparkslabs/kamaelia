
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

#
# The follow declaration short circuits the contents of both of these two files:
#     cdef extern from "dirac/libdirac_common/dirac-stdint.h":
#     cdef extern from "dirac/libdirac_common/dirac_inttypes.h":
#
cdef extern from "stdint.h":
    ctypedef long int                int64_t
    ctypedef unsigned long int       uint64_t



#  This file contains common enumerated types used throughout the encoder and
#  the end user interfaces to the encoder and decoder
# ---------------------------------------------------------------------------------
cdef extern from "dirac/libdirac_common/common_types.h":
    pass

    #
    # Some basic enumeration types used throughout the codec and by end user ...//
    #

    # Types of chroma formatting (formatNK=format not known) */
    ctypedef enum ChromaFormat:
        format444
        format422
        format420
        formatNK

    # Types of Wavelet filters supported. filterNK -  not known)
    ctypedef enum WltFilter:
        DD9_7=0      # Deslauriers-Dubuc (9,7)
        LEGALL5_3    # LeGall (5,3)
        DD13_7       # Deslauriers-Dubuc (13,7)
        HAAR0        # Haar, no shift per level
        HAAR1        # Haar, one shift per level
        FIDELITY     # Fidelity wavelet
        DAUB9_7      # Integer approximation to Daubechies 97
        filterNK

    # Enumerated type that defines prefiltering types supported by the encoder
    ctypedef enum PrefilterType:
        NO_PF = 0
        DIAGLP
        RECTLP
        CWM

    cdef int NUM_WLT_FILTERS = 8

    # Types of picture
    ctypedef enum PictureType:
        INTRA_PICTURE=0
        INTER_PICTURE

    # Types of referencing
    ctypedef enum ReferenceType:
        REFERENCE_PICTURE=0
        NON_REFERENCE_PICTURE

    # Types for video-format
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

    # Types of Colour Matrices
    ctypedef enum ColourMatrix:
        CM_HDTV_COMP_INTERNET=0
        CM_SDTV
        CM_REVERSIBLE
        CM_UNDEF

    # Types of Transfer functions
    ctypedef enum TransferFunction:
        TF_TV=0
        TF_EXT_GAMUT
        TF_LINEAR
        TF_DCINEMA
        TF_UNDEF

    # Types of Picture-rate
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

    # Types of Aspect Ratio
    ctypedef enum PixelAspectRatioType:
        PIXEL_ASPECT_RATIO_CUSTOM=0
        PIXEL_ASPECT_RATIO_1_1
        PIXEL_ASPECT_RATIO_10_11
        PIXEL_ASPECT_RATIO_12_11
        PIXEL_ASPECT_RATIO_40_33
        PIXEL_ASPECT_RATIO_16_11
        PIXEL_ASPECT_RATIO_4_3
        PIXEL_ASPECT_RATIO_UNDEFINED

    # Types of signal range
    ctypedef enum SignalRangeType:
        SIGNAL_RANGE_CUSTOM=0
        SIGNAL_RANGE_8BIT_FULL
        SIGNAL_RANGE_8BIT_VIDEO
        SIGNAL_RANGE_10BIT_VIDEO
        SIGNAL_RANGE_12BIT_VIDEO
        SIGNAL_RANGE_UNDEFINED

    # Types of motion-vector precision
    ctypedef enum MVPrecisionType:
        MV_PRECISION_PIXEL=0
        MV_PRECISION_HALF_PIXEL
        MV_PRECISION_QUARTER_PIXEL
        MV_PRECISION_EIGHTH_PIXEL
        MV_PRECISION_UNDEFINED

    # Type of quantiser modes when spatial partitioning is enabled
    ctypedef enum CodeBlockMode:
        QUANT_SINGLE
        QUANT_MULTIPLE
        QUANT_UNDEF

# ---------------------------------------------------------------------------------
cdef extern from "dirac/libdirac_common/dirac_types.h":

    #
    # Major version corresponds to major version of the software.
    # Minor version corresponds to minor version of the software. Bump
    #   this up by one whenever there are  major feature changes to the software.
    # Patch version corresponds to changes in the API. It should be
    #   bumped up by 1 for every committed change to the API
    #
    cdef int DIRAC_RESEARCH_MAJOR_VERSION=1   # 0..255
    cdef int DIRAC_RESEARCH_MINOR_VERSION=0   # 0..255
    cdef int DIRAC_RESEARCH_PATCH_VERSION=2   # 0..255

    #
    # Some basic enumeration types used by end user encoder and decoder ...//
    #
    ctypedef ChromaFormat  dirac_chroma_t
    ctypedef PictureType   dirac_picture_type_t
    ctypedef ReferenceType dirac_reference_type_t
    ctypedef WltFilter     dirac_wlt_filter_t

    ctypedef struct dirac_rational_t:
        int numerator
        int denominator

    ctypedef dirac_rational_t dirac_frame_rate_t
    ctypedef dirac_rational_t dirac_pix_asr_t

    # Structure that holds the parase parameters
    ctypedef struct dirac_parseparams_t:
        unsigned int major_ver   # Major version
        unsigned int minor_ver   # Minor version
        unsigned int profile     # Profile
        unsigned int level       # level

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

    ctypedef ColourPrimaries dirac_col_primaries_t
    ctypedef TransferFunction dirac_transfer_func_t

    ctypedef struct dirac_colour_spec_t:
        dirac_col_primaries_t col_primary
        dirac_col_matrix_t col_matrix
        dirac_transfer_func_t trans_func

    # Structure that holds the source parameters
    ctypedef struct dirac_sourceparams_t:
        unsigned int width                # numper of pixels per line
        unsigned int height               # number of lines per frame
        dirac_chroma_t chroma             # chroma type
        unsigned int chroma_width         # numper of pixels of chroma per line
        unsigned int chroma_height        # number of lines of chroma per frame
        unsigned int source_sampling      # source sampling field: 0 - progressive; 1 - interlaced
        int topfieldfirst                 # top field comes first : 0 - false; 1 - true. Set by Dirac library.
        dirac_frame_rate_t frame_rate     # frame rate
        dirac_pix_asr_t pix_asr           # pixel aspect ratio
        dirac_clean_area_t clean_area     # clean area
        dirac_signal_range_t signal_range # signal range
        dirac_colour_spec_t colour_spec   # colour specification

    # Structure that holds the picture parameters
    ctypedef struct dirac_picparams_t:
        dirac_picture_type_t ptype       # picture type
        dirac_reference_type_t rtype     # reference type
        int pnum                         # picture number in decoded order

    #  Structure that holds the frame buffers into which data is written 
    # (NB we have frame-oriented IO even though we code pictures)
    ctypedef struct dirac_framebuf_t:
        unsigned char  *buf[3]           # buffers to hold the luma and chroma data
        void  *id                        # user data


















