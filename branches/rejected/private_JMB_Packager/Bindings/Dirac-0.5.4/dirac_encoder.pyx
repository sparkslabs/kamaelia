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
from dirac_common cimport dirac_chroma_t, Yonly, format422, format444, format420, format411, formatNK
from dirac_common cimport dirac_frame_type_t, I_frame, L1_frame, L2_frame
from dirac_common cimport dirac_rational_t
from dirac_common cimport dirac_frame_rate_t
from dirac_common cimport dirac_seqparams_t
from dirac_common cimport dirac_frameparams_t
from dirac_common cimport dirac_framebuf_t


cdef extern from "limits.h":
    ctypedef enum __:
        INT_MAX

cdef extern from "dirac/libdirac_encoder/dirac_encoder.h":
    ctypedef enum dirac_encoder_state_t:
        ENC_STATE_INVALID = -1
        ENC_STATE_BUFFER
        ENC_STATE_AVAIL

    ctypedef enum dirac_encoder_presets_t:
        CIF
        SD576
        HD720
        HD1080

    ctypedef struct dirac_encparams_t:
        float qf
        int   L1_sep
        int   num_L1
        float cpd
        int  xblen
        int  yblen
        int  xbsep
        int  ybsep

    ctypedef struct dirac_encoder_context_t:
        dirac_seqparams_t seq_params
        dirac_encparams_t enc_params
        int               instr_flag
        int               decode_flag

    cdef void dirac_encoder_context_init(dirac_encoder_context_t *enc_ctx, dirac_encoder_presets_t preset)

    ctypedef struct dirac_enc_data_t:
        unsigned char *buffer
        int            size


    ctypedef struct dirac_enc_framestats_t:
        unsigned int mv_bits
        unsigned int mv_hdr_bits
        unsigned int ycomp_bits
        unsigned int ycomp_hdr_bits
        unsigned int ucomp_bits
        unsigned int ucomp_hdr_bits
        unsigned int vcomp_bits
        unsigned int vcomp_hdr_bits
        unsigned int frame_bits
        unsigned int frame_hdr_bits

    ctypedef struct dirac_enc_seqstats_t:
        unsigned int mv_bits
        unsigned int seq_bits
        unsigned int seq_hdr_bits
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



cdef class DiracEncoder:

    cdef dirac_encoder_t *encoder
    cdef dirac_encoder_context_t context
    cdef object inputframe
    cdef object outbuffer
    cdef object outbuffersize

    def __new__(self, preset=None, bufsize = 1024*1024, verbose=False, encParams = {}, seqParams = {}, instrumentation=False, localDecoded=False):
        cdef int cverbose
        cverbose = 0
        if verbose:
            cverbose = 1

        self.__presetContext(preset)
        self.__loadEncParams(**encParams)
        self.__loadSeqParams(**seqParams)

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
            print "z"
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
            print "y"
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

        if preset=="CIF":
            cpreset=CIF
        elif preset=="SD576":
            cpreset=SD576
        elif preset=="HD720":
            cpreset=HD720
        elif preset=="HD1080":
            cpreset=HD1080
        else:
            raise ValueError("Not valid preset")

        dirac_encoder_context_init( &self.context, cpreset)


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

        if "frame_rate" in params:
            self.context_seq_params.frame_rate.numerator   = params['frame_rate'][0]
            self.context_seq_params.frame_rate.denominator = params['frame_rate'][1]

        if "interlace" in params:
            if params['interlace']:
                self.context.seq_params.interlace = 1
            else:
                self.context.seq_params.interlace = 0

        if "topfieldfirst" in params:
            if params['topfieldfirst']:
                self.context.seq_params.topfieldfirst = 1
            else:
                self.context.seq_params.topfieldfirst = 0


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


    


cdef dirac_chroma_t __chromatypemap(object c):
    if c == "Yonly":
        return Yonly
    elif c == "422":
        return format422
    elif c == "444":
        return format444
    elif c == "420":
        return format420
    elif c == "411":
        return format411
    elif c == "NK":
        return formatNK
    else:
        raise ValueError("Unknown chroma type")



