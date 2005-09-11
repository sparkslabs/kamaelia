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
from dirac_common cimport dirac_chroma_t, Yonly, format422, format444, format420, format411, formatNK
from dirac_common cimport dirac_frame_type_t, I_frame, L1_frame, L2_frame
from dirac_common cimport dirac_rational_t
from dirac_common cimport dirac_frame_rate_t
from dirac_common cimport dirac_seqparams_t
from dirac_common cimport dirac_frameparams_t
from dirac_common cimport dirac_framebuf_t


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



cdef class DiracParser:

    cdef dirac_decoder_t *decoder
    cdef unsigned char *cbuffers[3]        # buffers dirac will build frames into
    cdef object inputbuffer
    cdef object seqdata
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
                self.__allocBuffers()
                raise "SEQINFO"
    
            elif state == STATE_PICTURE_START:
                parse = True
#                raise "FRAMEINFO"
    
            elif state == STATE_PICTURE_AVAIL:
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

        framerate = float(params.frame_rate.numerator) / float(params.frame_rate.denominator)

        self.seqdata = { "size"          : (int(params.width), int(params.height)),
                         "chroma_type"   :  __mapchromatype(params.chroma),
                         "chroma_size"   : (int(params.chroma_width), int(params.chroma_height)),
                         "frame_rate"    : framerate,
                         "interlaced"    : int(params.interlace),
                         "topfieldfirst" : int(params.topfieldfirst),
                       }

    def getSeqData(self):
        return self.seqdata

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
        frame['yuv'] = (self.ybuffer, self.vbuffer, self.ubuffer)
        return frame

        

cdef object __mapchromatype(dirac_chroma_t c):
    if c == Yonly:
        return "Yonly"
    elif c == format422:
        return "422"
    elif c == format444:
        return "444"
    elif c == format420:
        return "420"
    elif c == format411:
        return "411"
    elif c == formatNK:
        return "NK"
    else:
        raise "INTERNALFAULT"


