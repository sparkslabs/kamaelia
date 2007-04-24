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

