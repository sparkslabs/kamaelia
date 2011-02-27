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
# Pyrex wrapper for Dirac video codec compressor (dirac_encoder)
#
# Dirac is an open source video codec.
# Obtain it from http://dirac.sourceforge.net/
#

cimport dirac_common 

from dirac_common cimport *

cdef extern from "limits.h":
    ctypedef enum __:
        INT_MAX

class DiracEncodeException(Exception):
    pass


cdef extern from "dirac/libdirac_encoder/dirac_encoder.h":
    ctypedef enum dirac_encoder_state_t:
        ENC_STATE_INVALID = -1
        ENC_STATE_BUFFER
        ENC_STATE_AVAIL
        ENC_STATE_EOS

    ctypedef PrefilterType dirac_prefilter_t

    ctypedef VideoFormat dirac_encoder_presets_t

    ctypedef MVPrecisionType dirac_mvprecision_t
    
    ctypedef struct dirac_encparams_t:
        int                 lossless
        float               qf
        int                 full_search
        int                 combined_me
        int                 x_range_me
        int                 y_range_me
        int                 L1_sep
        # The number of L1 frames before the next intra frame. Together
        # with L1_sep determines the GOP structure.
        int                 num_L1
        float               cpd
        int                 xblen
        int                 yblen
        int                 xbsep
        int                 ybsep
        int                 video_format
        dirac_wlt_filter_t  intra_wlt_filter
        dirac_wlt_filter_t  inter_wlt_filter
        unsigned int        wlt_depth
        unsigned int        spatial_partition
        dirac_prefilter_t   prefilter
        unsigned int        prefilter_strength
        unsigned int        multi_quants
        dirac_mvprecision_t mv_precision
        int                 trate
        unsigned int        picture_coding_mode
        int                 using_ac

    ctypedef struct dirac_encoder_context_t:
        dirac_sourceparams_t src_params
        dirac_encparams_t    enc_params
        int                  instr_flag
        int                  decode_flag

    cdef void dirac_encoder_context_init (dirac_encoder_context_t *enc_ctx, dirac_encoder_presets_t preset)

    ctypedef struct dirac_enc_data_t:
        unsigned char *buffer
        int size

    ctypedef struct dirac_enc_picstats_t:
        unsigned int mv_bits
        unsigned int ycomp_bits
        unsigned int ucomp_bits
        unsigned int vcomp_bits
        unsigned int pic_bits

    ctypedef struct dirac_enc_seqstats_t:
        int64_t mv_bits
        int64_t seq_bits
        int64_t ycomp_bits
        int64_t ucomp_bits
        int64_t vcomp_bits
        int64_t bit_rate

    ctypedef struct dirac_mv_t:
        int x
        int y

    ctypedef struct dirac_mv_cost_t:
        float SAD
        float mvcost

    ctypedef struct dirac_instr_t:
        dirac_picture_type_t   ptype
        dirac_reference_type_t rtype
        int                    pnum
        int                    num_refs
        int                    refs[2]
        int                    xbsep
        int                    ybsep
        int                    sb_xlen
        int                    sb_ylen
        int                    mv_xlen
        int                    mv_ylen
        int                    *sb_split_mode
        float                  *sb_costs
        int                    *pred_mode
        float                  *intra_costs
        dirac_mv_cost_t        *bipred_costs
        short                  *dc_ycomp
        short                  *dc_ucomp
        short                  *dc_vcomp
        dirac_mv_t             *mv[2]
        dirac_mv_cost_t        *pred_costs[2]

    ctypedef struct dirac_encoder_t:
        dirac_encoder_context_t enc_ctx
        int                     encoded_picture_avail
        dirac_enc_data_t        enc_buf
        dirac_picparams_t       enc_pparams
        dirac_enc_picstats_t    enc_pstats
        dirac_enc_seqstats_t    enc_seqstats
        int                     end_of_sequence
        int                     decoded_frame_avail
        dirac_framebuf_t        dec_buf
        dirac_picparams_t       dec_pparams
        dirac_instr_t           instr
        int                     instr_data_avail
        void                    *compressor # In C file this is const void*

    cdef dirac_encoder_t       *dirac_encoder_init (dirac_encoder_context_t *enc_ctx, int verbose)
    cdef int dirac_encoder_pts_offset (dirac_encoder_t *encoder)
    cdef int                    dirac_encoder_load (dirac_encoder_t *encoder, unsigned char *uncdata, int uncdata_size)
    cdef dirac_encoder_state_t  dirac_encoder_output (dirac_encoder_t *encoder)
    cdef void                   dirac_encoder_end_sequence (dirac_encoder_t *encoder)
    cdef void                   dirac_encoder_close (dirac_encoder_t *encoder)


cdef extern from "Python.h": 
    object PyString_FromStringAndSize(char *, int)
    cdef char* PyString_AsString(object)

dirac_version = (1, 0, 2)

cdef class DiracEncoder:

    cdef dirac_encoder_t *encoder
    cdef dirac_encoder_context_t context
    cdef object inputframe
    cdef object outbuffer
    cdef object outbuffersize

    def __cinit__(self, preset=None, bufsize = 1024*1024, verbose=False, allParams = {}, instrumentation=False, localDecoded=False):
        cdef int cverbose
        cverbose = 0
        if verbose:
            cverbose = 1

        self.__presetContext(preset)
        self.__loadEncParams(**allParams)
        self.__loadSrcParams(**allParams)
        self.__loadSeqParams(**allParams)

        if instrumentation:
            self.context.instr_flag = 1
        else:
            self.context.instr_flag = 0

        if localDecoded:
            self.context.decode_flag = 1
        else:
            self.context.decode_flag = 0

        self.encoder = dirac_encoder_init( &self.context, cverbose )
        if self.encoder == NULL:
            raise DiracEncodeException("FAILURE")

        self.outbuffersize = bufsize
        self.__allocOutBuffer()
        self.__setOutBuffer()


    def __dealloc__(self):
        dirac_encoder_close(self.encoder)


    def getCompressedData(self):
        cdef dirac_encoder_state_t state

        self.__setOutBuffer()
        state = dirac_encoder_output(self.encoder)

        if state == ENC_STATE_INVALID:
            raise DiracEncodeException("ENCODERERROR")

        elif state == ENC_STATE_BUFFER:
            raise DiracEncodeException("NEEDDATA")

        elif state == ENC_STATE_AVAIL:
            data = self.outbuffer[:self.encoder.enc_buf.size]
            self.__allocOutBuffer()
            return data

        else:
            raise DiracEncodeException("INTERNALFAULT")

    def sendFrameForEncode(self, yuvdata):
        cdef unsigned char *bytes
        cdef int size
        cdef int result

        self.inputframe = yuvdata

        bytes = <unsigned char*>PyString_AsString(yuvdata)
        size = int(len(self.inputframe))

        result = dirac_encoder_load(self.encoder, bytes, size)

        if result == -1:
            raise DiracEncodeException("ENCODERERROR")

    def getEndSequence(self):
        cdef int result
        self.__setOutBuffer()
        dirac_encoder_end_sequence(self.encoder)

        # Assume OK. 
        data = self.outbuffer[:self.encoder.enc_buf.size]
        return data


    def getFrameStats(self):
        ##############################################
        pass

    def getSeqStats(self):
        ##############################################
        pass

    def getInstrumentation(self):
        ##############################################
        pass

    def getLocallyDecodedFrame(self):
        ##############################################
        pass

    def __allocOutBuffer(self):
        self.outbuffer = PyString_FromStringAndSize(NULL, self.outbuffersize)

    def __setOutBuffer(self):
        self.encoder.enc_buf.buffer = <unsigned char*>PyString_AsString(self.outbuffer)
        self.encoder.enc_buf.size   = self.outbuffersize

    def __presetContext(self, preset=None):
        cdef dirac_encoder_presets_t cpreset
        
        cpreset = __mapping_videoformat(preset)
        dirac_encoder_context_init( &self.context, cpreset)

    def __loadEncParams(self, **params):
        if "qf" in params:
            self.context.enc_params.qf = float(params['qf'])

        if "L1_sep" in params:
            self.context.enc_params.L1_sep = int(params['L1_sep'])

        if "num_L1" in params:
            self.context.enc_params.num_L1 = int(params['num_L1'])

        if "cpd" in params:
            self.context.enc_params.cpd = float(params['cpd'])

        if "xblen" in params:
            self.context.enc_params.xblen = int(params['xblen'])

        if "yblen" in params:
            self.context.enc_params.yblen = int(params['yblen'])

        if "xbsep" in params:
            self.context.enc_params.xbsep = int(params['xbsep'])

        if "ybsep" in params:
            self.context.enc_params.ybsep = int(params['ybsep'])

# Unsupported in 1.0.2 - split apart
#        if "wlt_filter" in params:
#            self.context.enc_params.wlt_filter = __mapping_wlt_filter(params['wlt_filter'])
        
        if "wlt_depth" in params:
            self.context.enc_params.wlt_depth = int(params['wl_depth'])
        
        if "spatial_partition" in params:
            self.context.enc_params.spatial_partition = int(params['spatial_partition'])

        if "def_spatial_partition" in params:
            self.context.enc_params.def_spatial_partition = int(params['def_spatial_partition'])

        if "multi_quants" in params:
            self.context.enc_params.multi_quants = int(params['multi_quants'])

        if "mv_precision" in params:
            self.context.enc_params.mv_precision = __mapping_mv_precision(params['mv_precision'])


    def __loadSrcParams(self, **params):
        if "interlace" in params:
            if params['interlace']:
                self.context.src_params.interlace = 1
            else:
                self.context.src_params.interlace = 0

        if "topfieldfirst" in params:
            if params['topfieldfirst']:
                self.context.src_params.topfieldfirst = 1
            else:
                self.context.src_params.topfieldfirst = 0
        
        if "seqfields" in params:
            self.context.src_params.seqfields = int(params['seqfields'])
        
        if "frame_rate" in params:
            self.context_src_params.frame_rate.numerator   = params['frame_rate'][0]
            self.context_src_params.frame_rate.denominator = params['frame_rate'][1]

        if "pix_asr" in params:
            self.context.src_params.pix_asr.numerator   = params['pix_asr'][0]
            self.context.src_params.pix_asr.denominator = params['pix_asr'][1]
    
        if "clean_area" in params:
            self.context.src_params.clean_area = __mapping_clean_area(params['clean_area'])
        if "signal_range" in params:
            self.context.src_params.signal_range = __mapping_signalrange(params['signal_range'])
            
        if "colour_spec" in params:
            self.context.src_params.colour_spec = __mapping_colour_spec(params['colour_spec'])
    
    
    def __loadSeqParams(self, **params):
        if "width" in params:
            self.context.seq_params.width = int(params['width'])

        if "height" in params:
            self.context.seq_params.height = int(params['height'])

        if "chroma" in params:
            self.context.seq_params.chroma = __chromatypemap(params['chroma'])

        if "chroma_width" in params:
            self.context.seq_params.chroma_width = int(params['chroma_width'])

        if "chroma_height" in params:
            self.context.seq_params.chroma_height = int(params['chroma_height'])

# ALL Named Mapping Functions -------------------------------------------------------------

# Better : __mapping_named_chromaformat
#
cdef dirac_chroma_t __chromatypemap(object c):
    if c == "444":
        return format444
    elif c == "422":
        return format422
    elif c == "420":
        return format420
    elif c == "NK":
        return formatNK
    else:
        raise ValueError("Unknown chroma type")

cdef dirac_wlt_filter_t __mapping_wlt_filter(object c):
    if c == "DD9_7":
        return DD9_7
    elif c == "LEGALL5_3":
        return LEGALL5_3
    elif c == "DD13_7":
        return DD13_7
    elif c == "HAAR0":
        return HAAR0
    elif c == "HAAR1":
        return HAAR1
    elif c == "FIDELITY":
        return FIDELITY
    elif c == "DAUB9_7":
        return DAUB9_7
    elif c == "filterNK":
        return filterNK
    else:
        raise ValueError("Unknown filter type")

cdef dirac_prefilter_t __mapping_pre_filter(object c):
    if c == "NO_PF":
        return NO_PF
    elif c == "DIAGLP":
        return DIAGLP
    elif c == "RECTLP":
        return RECTLP
    elif c == "CWM":
        return CWM
    else:
        raise ValueError("Unknown pre filter type")

cdef dirac_picture_type_t __mapping_picture_type(object c):
    if c == "INTRA_PICTURE":
        return INTRA_PICTURE
    elif c == "INTER_PICTURE":
        return INTER_PICTURE
    else:
        raise ValueError("Unknown pre filter type")

cdef dirac_reference_type_t __mapping_reference_type(object c):
    if c == "REFERENCE_PICTURE":
        return REFERENCE_PICTURE
    elif c == "NON_REFERENCE_PICTURE":
        return NON_REFERENCE_PICTURE
    else:
        raise ValueError("Unknown pre filter type")

cdef dirac_encoder_presets_t __mapping_videoformat(object preset):
    if preset=="CUSTOM":
        return VIDEO_FORMAT_CUSTOM
    elif preset=="QSIF525":
        return VIDEO_FORMAT_QSIF525
    elif preset=="QCIF":
        return VIDEO_FORMAT_QCIF
    elif preset=="SIF525":
        return VIDEO_FORMAT_SIF525
    elif preset=="CIF":
        return VIDEO_FORMAT_CIF
    elif preset=="4SIF525":
        return VIDEO_FORMAT_4SIF525
    elif preset=="4CIF":
        return VIDEO_FORMAT_4CIF
    elif preset=="SD_480I60":
        return VIDEO_FORMAT_SD_480I60
    elif preset=="SD_576I50":
        return VIDEO_FORMAT_SD_576I50
    elif preset=="HD_720P60":
        return VIDEO_FORMAT_HD_720P60
    elif preset=="HD_720P50":
        return VIDEO_FORMAT_HD_720P50
    elif preset=="HD_1080I60":
        return VIDEO_FORMAT_HD_1080I60
    elif preset=="HD_1080I50":
        return VIDEO_FORMAT_HD_1080I50
    elif preset=="HD_1080P60":
        return VIDEO_FORMAT_HD_1080P60
    elif preset=="HD_1080P50":
        return VIDEO_FORMAT_HD_1080P50
    elif preset=="DIGI_CINEMA_2K24":
        return VIDEO_FORMAT_DIGI_CINEMA_2K24
    elif preset=="DIGI_CINEMA_4K24":
        return VIDEO_FORMAT_DIGI_CINEMA_4K24
    elif preset=="UHDTV_4K60":
        return VIDEO_FORMAT_UHDTV_4K60
    elif preset=="UHDTV_4K50":
        return VIDEO_FORMAT_UHDTV_4K50
    elif preset=="UHDTV_8K60":
        return VIDEO_FORMAT_UHDTV_8K60
    elif preset=="UHDTV_8K50":
        return VIDEO_FORMAT_UHDTV_8K50
    elif preset=="UNDEFINED":
        return VIDEO_FORMAT_UNDEFINED
    else:
        raise ValueError("Not valid video format")

cdef dirac_col_primaries_t __mapping_col_primaries(object cprim):
    if cprim=="CP_HDTV_COMP_INTERNET":
        return CP_HDTV_COMP_INTERNET
    if cprim=="CP_SDTV_525":
        return CP_SDTV_525
    if cprim=="CP_SDTV_625":
        return CP_SDTV_625
    if cprim=="CP_DCINEMA":
        return CP_DCINEMA
    elif cprim=="CP_UNDEF":
        return CP_UNDEF
    else:
        raise ValueError("Not valid colour primaries set")

cdef ColourMatrix __mapping_colour_matrix(object cmatrix):   # FIXME: type checked - maybe ok
    if cmatrix=="CM_HDTV_COMP_INTERNET":
        return CM_HDTV_COMP_INTERNET
    elif cmatrix=="CM_SDTV":
        return CM_SDTV
    elif cmatrix=="CM_REVERSIBLE":
        return CM_REVERSIBLE
    elif cmatrix=="CM_UNDEF":
        return CM_UNDEF
    else:
        raise ValueError("Not valid colour matrix set")

cdef dirac_transfer_func_t __mapping_trans_func(object transf):
    if transf=="TF_TV":
        return TF_TV
    elif transf=="TF_EXT_GAMUT":
        return TF_EXT_GAMUT
    elif transf=="TF_LINEAR":
        return TF_LINEAR
    elif transf=="TF_DCINEMA":
        return TF_DCINEMA
    elif transf=="TF_UNDEF":
        return TF_UNDEF
    else:
        raise ValueError("Not valid transfer function")

cdef FrameRateType __mapping_named_frame_rate(object named_frate):  # FIXME: type checked - maybe ok
    if named_frate=="FRAMERATE_CUSTOM":
        return FRAMERATE_CUSTOM
    elif named_frate=="FRAMERATE_23p97_FPS":
        return FRAMERATE_23p97_FPS
    elif named_frate=="FRAMERATE_24_FPS":
        return FRAMERATE_24_FPS
    elif named_frate=="FRAMERATE_25_FPS":
        return FRAMERATE_25_FPS
    elif named_frate=="FRAMERATE_29p97_FPS":
        return FRAMERATE_29p97_FPS
    elif named_frate=="FRAMERATE_30_FPS":
        return FRAMERATE_30_FPS
    elif named_frate=="FRAMERATE_50_FPS":
        return FRAMERATE_50_FPS
    elif named_frate=="FRAMERATE_59p94_FPS":
        return FRAMERATE_59p94_FPS
    elif named_frate=="FRAMERATE_60_FPS":
        return FRAMERATE_60_FPS
    elif named_frate=="FRAMERATE_14p98_FPS":
        return FRAMERATE_14p98_FPS
    elif named_frate=="FRAMERATE_12p5_FPS":
        return FRAMERATE_12p5_FPS
    elif named_frate=="FRAMERATE_UNDEFINED":
        return FRAMERATE_UNDEFINED
    else:
        raise ValueError("Not valid named frame rate")

cdef PixelAspectRatioType __mapping_named_pixel_aspect_ratio(object asr):  # FIXME: type checked - maybe ok
    if asr=="PIXEL_ASPECT_RATIO_CUSTOM":
        return PIXEL_ASPECT_RATIO_CUSTOM
    elif asr=="PIXEL_ASPECT_RATIO_1_1":
        return PIXEL_ASPECT_RATIO_1_1
    elif asr=="PIXEL_ASPECT_RATIO_1_1":
        return PIXEL_ASPECT_RATIO_1_1
    elif asr=="PIXEL_ASPECT_RATIO_10_11":
        return PIXEL_ASPECT_RATIO_10_11
    elif asr=="PIXEL_ASPECT_RATIO_12_11":
        return PIXEL_ASPECT_RATIO_12_11
    elif asr=="PIXEL_ASPECT_RATIO_40_33":
        return PIXEL_ASPECT_RATIO_40_33
    elif asr=="PIXEL_ASPECT_RATIO_16_11":
        return PIXEL_ASPECT_RATIO_16_11
    elif asr=="PIXEL_ASPECT_RATIO_4_3":
        return PIXEL_ASPECT_RATIO_4_3
    elif asr=="PIXEL_ASPECT_RATIO_UNDEFINED":
        return PIXEL_ASPECT_RATIO_UNDEFINED
    else:
        raise ValueError("Not valid named pixel aspect ratio type")

cdef SignalRangeType  __mapping_named_signal_range(object nsr):   # FIXME: type checked - maybe ok
    if nsr=="SIGNAL_RANGE_CUSTOM":
        return SIGNAL_RANGE_CUSTOM
    elif nsr=="SIGNAL_RANGE_8BIT_FULL":
        return SIGNAL_RANGE_8BIT_FULL
    elif nsr=="SIGNAL_RANGE_8BIT_VIDEO":
        return SIGNAL_RANGE_8BIT_VIDEO
    elif nsr=="SIGNAL_RANGE_10BIT_VIDEO":
        return SIGNAL_RANGE_10BIT_VIDEO
    elif nsr=="SIGNAL_RANGE_12BIT_VIDEO":
        return SIGNAL_RANGE_12BIT_VIDEO
    elif nsr=="SIGNAL_RANGE_UNDEFINED":
        return SIGNAL_RANGE_UNDEFINED
    else:
        raise ValueError("Not valid named signal range type")

cdef dirac_mvprecision_t __mapping_mv_precision(object mv):
    if mv=="MV_PRECISION_PIXEL":
        return MV_PRECISION_PIXEL
    elif mv=="MV_PRECISION_HALF_PIXEL":
        return MV_PRECISION_HALF_PIXEL
    elif mv=="MV_PRECISION_QUARTER_PIXEL":
        return MV_PRECISION_QUARTER_PIXEL
    elif mv=="MV_PRECISION_EIGHTH_PIXEL":
        return MV_PRECISION_EIGHTH_PIXEL
    elif mv=="MV_PRECISION_UNDEFINED":
        return MV_PRECISION_UNDEFINED
    else:
        raise ValueError("Not valid motion vector precision")

cdef CodeBlockMode __mapping_named_codeblockmode(object cbm):  # FIXME: type checked - maybe ok
    if cbm=="QUANT_SINGLE":
        return QUANT_SINGLE
    elif cbm=="QUANT_MULTIPLE":
        return QUANT_MULTIPLE
    elif cbm=="QUANT_UNDEF":
        return QUANT_UNDEF
    else:
        raise ValueError("Not valid named code block mode")

# Argument Conversion functions ----------------------------------------------------

cdef dirac_clean_area_t __mapping_clean_area(object carea):
    cdef dirac_clean_area_t c
    
    if "width" in carea:
        c.width = int(carea['width'])
    if "height" in carea:
        c.height = int(carea['height'])
    if "left_offset" in carea:
        c.left_offset = int(carea['left_offset'])
    if "top_offset" in carea:
        c.top_offset = int(carea['top_offset'])
        
    return c

cdef dirac_signal_range_t __mapping_signalrange(object srange):
    cdef dirac_signal_range_t s
    
    if "luma_offset" in srange:
        s.luma_offset = int(srange['luma_offset'])
    if "luma_excursion" in srange:
        s.luma_excursion = int(srange['luma_excursion'])
    if "chroma_offset" in srange:
        s.chroma_offset = int(srange['chroma_offset'])
    if "chroma_excursion" in srange:
        s.chroma_excursion = int(srange['chroma_excursion'])
        
    return s

cdef dirac_colour_spec_t __mapping_colour_spec(object cspec):
    cdef dirac_colour_spec_t c
    
    if "col_primary" in cspec:
        c.col_primary = __mapping_col_primaries(cspec['col_primary'])
    if "col_matrix" in cspec:
        c.col_matrix = __mapping_col_matrix(cspec['col_matrix'])
    if "trans_func" in cspec:
        c.trans_func = __mapping_trans_func(cspec['trans_func'])
    
    return c

cdef dirac_col_matrix_t __mapping_col_matrix(object cmat):  # FIXME: Relation to mapping?
    cdef dirac_col_matrix_t m
    
    if "kr" in cmat:
        m.kr = float(cmat['kr'])
    if "kb" in cmat:
        m.kb = float(cmat['kb'])
    
    return m
    
