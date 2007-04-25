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
# Pyrex wrapper for Dirac video codec decompressor (dirac_parser)
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
from dirac_common cimport     DD9_3
from dirac_common cimport     LEGALL5_3
from dirac_common cimport     DD13_5
from dirac_common cimport     HAAR0
from dirac_common cimport     HAAR1
from dirac_common cimport     HAAR2
from dirac_common cimport     FIDELITY
from dirac_common cimport     DAUB9_7
from dirac_common cimport     filterNK
from dirac_common cimport dirac_rational_t
from dirac_common cimport dirac_frame_rate_t
from dirac_common cimport dirac_asr_t
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

cdef enum:
    NUM_WLT_FILTERS = 8



cdef extern from "dirac/libdirac_decoder/decoder_types.h":
    ctypedef enum DecoderState:
        STATE_BUFFER
        STATE_SEQUENCE
        STATE_PICTURE_START
        STATE_PICTURE_DECODE
        STATE_PICTURE_AVAIL
        STATE_SEQUENCE_END
        STATE_INVALID


cdef extern from "dirac/libdirac_decoder/dirac_parser.h":
    ctypedef DecoderState dirac_decoder_state_t

    ctypedef struct dirac_decoder_t:
        dirac_decoder_state_t  state
        dirac_seqparams_t      seq_params
        dirac_sourceparams_t   src_params
        dirac_frameparams_t    frame_params
        void                  *parser
        dirac_framebuf_t      *fbuf
        int                    frame_avail
        int                    verbose


    cdef dirac_decoder_t *dirac_decoder_init(int verbose)
    cdef void             dirac_decoder_close(dirac_decoder_t *decoder)

    cdef dirac_decoder_state_t dirac_parse(dirac_decoder_t *decoder)

    cdef void dirac_buffer(dirac_decoder_t *decoder, unsigned char *start, unsigned char *end)
    cdef void dirac_set_buf(dirac_decoder_t *decoder, unsigned char *buf[3], void *id)
    cdef void dirac_skip(dirac_decoder_t *decoder, int skip)



cdef extern from "Python.h": 
    object PyString_FromStringAndSize(char *, int)
    cdef char* PyString_AsString(object)


dirac_version = (0, 6, 0)

cdef class DiracParser:

    cdef dirac_decoder_t *decoder
    cdef unsigned char *cbuffers[3]        # buffers dirac will build frames into
    cdef object inputbuffer
    cdef object seqdata
    cdef object srcdata
    cdef object framedata
    cdef object ybuffer
    cdef object ubuffer
    cdef object vbuffer

    def __new__(self, verbose = None):
        cdef int vflag
        vflag = 0
        if verbose:
            vflag = 1
        self.decoder = dirac_decoder_init(vflag)
        self.inputbuffer = ""

    def __dealloc__(self):
        dirac_decoder_close(self.decoder)

    # time to do a more intelligent wrap of actual decoding!

    # dirac asks for data when its ready,

    def getFrame(self):
#        """Parse the current buffer.
#           Returns:
#             frame dictionary,
#           Or raises:
#             "NEEDDATA" - use sendBytesForDecode
#             "SEQINFO"
#             "END"
#             "STREAMERROR"
#             "INTERNALFAULT"
#        """
        cdef dirac_decoder_state_t state

        parse = True
        while parse:
            state = dirac_parse(self.decoder)
            parse = False

            if state == STATE_BUFFER:
                self.inputbuffer = ""
                raise "NEEDDATA"
    
            elif state == STATE_SEQUENCE:
                self.__extractSequenceData()
                self.__extractSourceData()
                self.__allocBuffers()
                raise "SEQINFO"
    
            elif state == STATE_PICTURE_START:
                parse = True
#                raise "FRAMEINFO"
    
            elif state == STATE_PICTURE_AVAIL:
                self.__extractFrameData()
                frame =  self.__buildFrame()
                self.__allocBuffers()
                return frame
    
            elif state == STATE_SEQUENCE_END:
                raise "END"
    
            elif state == STATE_INVALID:
                raise "STREAMERROR"
    
            else:
                raise "INTERNALFAULT"


    def sendBytesForDecode(self, bytes):
#        """Call only immediately after initialisation or in reponse to
#           "NEED DATA" exception from getFrame()
#        """
        cdef unsigned char *cbytes
        cdef unsigned char *cbytes_end
        cdef long int temp

        if self.inputbuffer == "":
            self.inputbuffer = bytes
            cbytes = <unsigned char*>PyString_AsString(bytes)
            temp = <long int>cbytes + len(bytes)
            cbytes_end = <unsigned char*>temp
            dirac_buffer(self.decoder, cbytes, cbytes_end)
        else:
            raise "NOTREADY"

    def __extractSequenceData(self):
        cdef dirac_seqparams_t params

        params = self.decoder.seq_params

        self.seqdata = { "size"          : (int(params.width), int(params.height)),
                         "chroma_type"   :  __mapchromatype(params.chroma),
                         "chroma_size"   : (int(params.chroma_width), int(params.chroma_height)),
                         "bitdepth"      : int(params.video_depth),
                       }
                       
    def __extractSourceData(self):
        cdef dirac_sourceparams_t params
        
        params = self.decoder.src_params
        
        if params.frame_rate.denominator:
            framerate = float(params.frame_rate.numerator) / float(params.frame_rate.denominator)
        else:
            framerate = 0.0
            
        if params.pix_asr.denominator:
            pixelaspect = float(params.pix_asr.numerator) / float(params.pix_asr.denominator)
        else:
            pixelaspect = 1.0

        self.srcdata = { "interlaced"    : int(params.interlace),
                         "topfieldfirst" : int(params.topfieldfirst),
                         "fieldsequencing" : int(params.seqfields),
                         "frame_rate"    : framerate,
                         "pixel_aspect"  : pixelaspect,
                        # not bothering with
                        #    clean_area
                        #    signal_range
                        #    colour_spec
                       }
                       
    def __extractFrameData(self):
        cdef dirac_frameparams_t params
        
        params = self.decoder.frame_params
        
        self.framedata = {
            "frametype" : __mapping_frame_type(params.ftype),
            "reference_type" : __mapping_rframe_type(params.rtype),
            "frame number" : int(params.fnum),
        }

    def getSeqData(self):
        return self.seqdata
    
    def getSrcData(self):
        return self.srcdata
    
    def getFrameData(self):
        return self.framedata

    def __allocBuffers(self):
        ysize = self.seqdata['size'][0] * self.seqdata['size'][1]
        usize = self.seqdata['chroma_size'][0] * self.seqdata['chroma_size'][1]
        vsize = usize

        # new allocate uninitialised string buffers ... safe to modify
        self.ybuffer = PyString_FromStringAndSize(NULL, ysize)
        self.ubuffer = PyString_FromStringAndSize(NULL, usize)
        self.vbuffer = PyString_FromStringAndSize(NULL, vsize)

        self.cbuffers[0] = <unsigned char *>PyString_AsString(self.ybuffer)
        self.cbuffers[1] = <unsigned char *>PyString_AsString(self.ubuffer)
        self.cbuffers[2] = <unsigned char *>PyString_AsString(self.vbuffer)

        dirac_set_buf(self.decoder, self.cbuffers, NULL)

    def __buildFrame(self):
        frame = {}
        frame.update(self.getSeqData())
        frame.update(self.getSrcData())
        frame.update(self.getFrameData())
        frame['yuv'] = (self.ybuffer, self.ubuffer, self.vbuffer)
        return frame


cdef object __mapchromatype(dirac_chroma_t c):
    if c == format444:
        return "444"
    elif c == format422:
        return "422"
    elif c == format420:
        return "420"
    elif c == formatNK:
        return "NK"
    else:
        raise "INTERNALFAULT"

cdef object __mapping_frame_type(dirac_frame_type_t ftype):
    if ftype == INTRA_FRAME:
        return "INTRA"
    else:
        return "INTER"

cdef object __mapping_rframe_type(dirac_reference_type_t rtype):
    if rtype == REFERENCE_FRAME:
        return "REFERENCE"
    else:
        return "NON_REFERENCE"

