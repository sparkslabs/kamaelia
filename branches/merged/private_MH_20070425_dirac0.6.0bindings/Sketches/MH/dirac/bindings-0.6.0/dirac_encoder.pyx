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
# Pyrex wrapper for Dirac video codec compressor (dirac_encoder)
#
# Dirac is an open source video codec.
# Obtain it from http://dirac.sourceforge.net/
#

cimport dirac_common 

from dirac_common cimport dirac_chroma_t
from dirac_common cimport     format444
from dirac_common cimport     format422
from dirac_common cimport     format420
from dirac_common cimport     formatNK
from dirac_common cimport dirac_frame_type_t
from dirac_common cimport     INTRA_FRAME
from dirac_common cimport     INTER_FRAME
from dirac_common cimport dirac_reference_type_t
from dirac_common cimport     REFERENCE_FRAME
from dirac_common cimport     NON_REFERENCE_FRAME
from dirac_common cimport dirac_wlt_filter_t
from dirac_common cimport     APPROX97
from dirac_common cimport     FIVETHREE
from dirac_common cimport     THIRTEENFIVE
from dirac_common cimport     HAAR
from dirac_common cimport     RESERVED1
from dirac_common cimport     RESERVED2
from dirac_common cimport     DAUB97
from dirac_common cimport     filterNK
from dirac_common cimport dirac_rational_t
from dirac_common cimport dirac_frame_rate_t
from dirac_common cimport dirac_asr_rate_t
from dirac_common cimport dirac_parseparams_t
from dirac_common cimport dirac_seqparams_t
from dirac_common cimport dirac_clean_area_t
from dirac_common cimport dirac_signal_range_t
from dirac_common cimport dirac_col_matrix_t
from dirac_common cimport ColourMatrix
from dirac_common cimport     CM_HDTV_COMP_INTERNET
from dirac_common cimport     CM_SDTV
from dirac_common cimport     CM_DCINEMA
from dirac_common cimport     CM_UNDEF
from dirac_common cimport dirac_col_primaries_t
from dirac_common cimport     CP_ITU_709
from dirac_common cimport     CP_SMPTE_C
from dirac_common cimport     CP_EBU_3213
from dirac_common cimport     CP_CIE_XYZ
from dirac_common cimport     CP_UNDEF
from dirac_common cimport dirac_transfer_func_t
from dirac_common cimport     TF_TV
from dirac_common cimport     TF_EXT_GAMUT
from dirac_common cimport     TF_LINEAR
from dirac_common cimport     TF_DCINEMA
from dirac_common cimport     TF_UNDEF
from dirac_common cimport dirac_colour_spec_t
from dirac_common cimport dirac_sourceparams_t
from dirac_common cimport dirac_frameparams_t
from dirac_common cimport dirac_framebuf_t
from dirac_common cimport VideoFormat
from dirac_common cimport     VIDEO_FORMAT_CUSTOM
from dirac_common cimport     VIDEO_FORMAT_QSIF
from dirac_common cimport     VIDEO_FORMAT_QCIF
from dirac_common cimport     VIDEO_FORMAT_SIF
from dirac_common cimport     VIDEO_FORMAT_CIF
from dirac_common cimport     VIDEO_FORMAT_4CIF
from dirac_common cimport     VIDEO_FORMAT_4SIF
from dirac_common cimport     VIDEO_FORMAT_SD_525_DIGITAL
from dirac_common cimport     VIDEO_FORMAT_SD_625_DIGITAL
from dirac_common cimport     VIDEO_FORMAT_HD_720
from dirac_common cimport     VIDEO_FORMAT_HD_1080
from dirac_common cimport     VIDEO_FORMAT_DIGI_CINEMA_2K
from dirac_common cimport     VIDEO_FORMAT_DIGI_CINEMA_4K
from dirac_common cimport     VIDEO_FORMAT_UNDEFINED
from dirac_common cimport MVPrecisionType
from dirac_common cimport     MV_PRECISION_PIXEL
from dirac_common cimport     MV_PRECISION_HALF_PIXEL
from dirac_common cimport     MV_PRECISION_QUARTER_PIXEL
from dirac_common cimport     MV_PRECISION_EIGHTH_PIXEL
from dirac_common cimport     MV_PRECISION_UNDEFINED



cdef extern from "limits.h":
    ctypedef enum __:
        INT_MAX

cdef extern from "dirac/libdirac_encoder/dirac_encoder.h":
    ctypedef enum dirac_encoder_state_t:
        ENC_STATE_INVALID = -1
        ENC_STATE_BUFFER
        ENC_STATE_AVAIL

    ctypedef VideoFormat dirac_encoder_presets_t

    ctypedef MVPrecisionType dirac_mvprecision_t
    
    ctypedef struct dirac_encparams_t:
        int   lossless
        float qf
        int   L1_sep
        int   num_L1
        float cpd
        int   xblen
        int   yblen
        int   xbsep
        int   ybsep
        int   video_format
        dirac_wlt_filter_t  wlt_filter
        unsigned int        wlt_depth
        unsigned int        spatial_partition
        unsigned int        def_spatial_partition
        unsigned int        multi_quants
        dirac_mvprecision_t mv_precision

    ctypedef struct dirac_encoder_context_t:
        dirac_seqparams_t    seq_params
        dirac_sourceparams_t src_params
        dirac_encparams_t    enc_params
        int                  instr_flag
        int                  decode_flag

    cdef void dirac_encoder_context_init(dirac_encoder_context_t *enc_ctx, dirac_encoder_presets_t preset)

    ctypedef struct dirac_enc_data_t:
        unsigned char *buffer
        int            size


    ctypedef struct dirac_enc_framestats_t:
        unsigned int mv_bits
        unsigned int ycomp_bits
        unsigned int ucomp_bits
        unsigned int vcomp_bits
        unsigned int frame_bits

    ctypedef struct dirac_enc_seqstats_t:
        unsigned int mv_bits
        unsigned int seq_bits
        unsigned int ycomp_bits
        unsigned int ucomp_bits
        unsigned int vcomp_bits
        unsigned int bit_rate

    ctypedef struct dirac_mv_t:
        int x
        int y

    ctypedef struct dirac_mv_cost_t:
        float SAD
        float mvcost

    ctypedef struct dirac_instr_t:
        dirac_frame_type_t ftype
        dirac_reference_type_t rtype
        int             fnum
        int             num_refs
        int             refs[2]
        int             xbsep
        int             ybsep
        int             mb_xlen
        int             mb_ylen
        int             mv_xlen
        int             mv_ylen
        int             *mb_split_mode
        int             *mb_common_mode
        float           *mb_costs
        int             *pred_mode
        float           *intra_costs
        dirac_mv_cost_t *bipred_costs
        short           *dc_ycomp
        short           *dc_ucomp
        short           *dc_vcomp
        dirac_mv_t      *mv[2]
        dirac_mv_cost_t *pred_costs[2]


    ctypedef struct dirac_encoder_t:
        dirac_encoder_context_t enc_ctx
        int                     encoded_frame_avail
        dirac_enc_data_t        enc_buf
        dirac_frameparams_t     enc_fparams
        dirac_enc_framestats_t  enc_fstats
        dirac_enc_seqstats_t    enc_seqstats
        int                     end_of_sequence
        int                     decoded_frame_avail
        dirac_framebuf_t        dec_buf
        dirac_frameparams_t     dec_fparams
        dirac_instr_t           instr
        int                     instr_data_avail
        void                   *compressor

    cdef dirac_encoder_t       *dirac_encoder_init (dirac_encoder_context_t *enc_ctx, int verbose)
    cdef int                    dirac_encoder_load (dirac_encoder_t *encoder, unsigned char *uncdata, int uncdata_size)
    cdef dirac_encoder_state_t  dirac_encoder_output (dirac_encoder_t *encoder)
    cdef int                    dirac_encoder_end_sequence (dirac_encoder_t *encoder)
    cdef void                   dirac_encoder_close (dirac_encoder_t *encoder)



cdef extern from "Python.h": 
    object PyString_FromStringAndSize(char *, int)
    cdef char* PyString_AsString(object)

dirac_version = (0, 6, 0)

cdef class DiracEncoder:

    cdef dirac_encoder_t *encoder
    cdef dirac_encoder_context_t context
    cdef object inputframe
    cdef object outbuffer
    cdef object outbuffersize

    def __new__(self, preset=None, bufsize = 1024*1024, verbose=False, allParams = {}, instrumentation=False, localDecoded=False):
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
            raise "FAILURE"

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
            raise "ENCODERERROR"

        elif state == ENC_STATE_BUFFER:
            raise "NEEDDATA"

        elif state == ENC_STATE_AVAIL:
            data = self.outbuffer[:self.encoder.enc_buf.size]
            self.__allocOutBuffer()
            return data

        else:
            raise "INTERNALFAULT"


    def sendFrameForEncode(self, yuvdata):
        cdef unsigned char *bytes
        cdef int size
        cdef int result

        self.inputframe = yuvdata

        bytes = <unsigned char*>PyString_AsString(yuvdata)
        size = int(len(self.inputframe))

        result = dirac_encoder_load(self.encoder, bytes, size)

        if result == -1:
            raise "ENCODERERROR"


    def getEndSequence(self):
        cdef int result
        self.__setOutBuffer()
        result = dirac_encoder_end_sequence(self.encoder)
        if result == -1:
            raise "ENCODERERROR"
        else:
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

        if "wlt_filter" in params:
            self.context.enc_params.wlt_filter = __mapping_wlt_filter(params['wlt_filter'])
        
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


cdef dirac_encoder_presets_t __mapping_videoformat(object preset):
    if preset=="CUSTOM":
        return VIDEO_FORMAT_CUSTOM
    elif preset=="QSIF":
        return VIDEO_FORMAT_QSIF
    elif preset=="QCIF":
        return VIDEO_FORMAT_QCIF
    elif preset=="SIF":
        return VIDEO_FORMAT_SIF
    elif preset=="CIF":
        return VIDEO_FORMAT_CIF
    elif preset=="4CIF":
        return VIDEO_FORMAT_4CIF
    elif preset=="4SIF":
        return VIDEO_FORMAT_4SIF
    elif preset=="SD_525_DIGITAL":
        return VIDEO_FORMAT_SD_525_DIGITAL
    elif preset=="SD_625_DIGITAL":
        return VIDEO_FORMAT_SD_625_DIGITAL
    elif preset=="HD_720":
        return VIDEO_FORMAT_HD_720
    elif preset=="HD_1080":
        return VIDEO_FORMAT_HD_1080
    elif preset=="DIGI_CINEMA_2K":
        return VIDEO_FORMAT_DIGI_CINEMA_2K
    elif preset=="DIGI_CINEMA_4K":
        return VIDEO_FORMAT_DIGI_CINEMA_4K
    elif preset=="UNDEFINED":
        return VIDEO_FORMAT_UNDEFINED
    else:
        raise ValueError("Not valid video format")


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
    
cdef dirac_col_primaries_t __mapping_col_primaries(object cprim):
    if cprim=="CP_ITU_709":
        return CP_ITU_709
    elif cprim=="CP_SMPTE_C":
        return CP_SMPTE_C
    elif cprim=="CP_EBU_3213":
        return CP_EBU_3213
    elif cprim=="CP_CIE_XYZ":
        return CP_CIE_XYZ
    elif cprim=="CP_UNDEF":
        return CP_UNDEF
    else:
        raise ValueError("Not valid colour primaries set")

cdef dirac_col_matrix_t __mapping_col_matrix(object cmat):
    cdef dirac_col_matrix_t m
    
    if "kr" in cmat:
        m.kr = float(cmat['kr'])
    if "kb" in cmat:
        m.kb = float(cmat['kb'])
    
    return m
    
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
    

