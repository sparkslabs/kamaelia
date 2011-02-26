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
# Pyrex wrapper for Dirac video codec decompressor (dirac_parser)
#
# Dirac is an open source video codec.
# Obtain it from http://dirac.sourceforge.net/
#

cimport dirac_common 
from dirac_common cimport *

class DiracException(Exception):
    pass

cdef extern from "dirac/libdirac_decoder/decoder_types.h":
    ctypedef enum DecoderState:
        STATE_BUFFER
        STATE_SEQUENCE
        STATE_PICTURE_AVAIL
        STATE_SEQUENCE_END
        STATE_INVALID


cdef extern from "dirac/libdirac_decoder/dirac_parser.h":
    ctypedef DecoderState dirac_decoder_state_t

    ctypedef struct dirac_decoder_t:
        dirac_decoder_state_t  state
        dirac_parseparams_t    parse_params
        dirac_sourceparams_t   src_params
        unsigned int           frame_num
        void                  *parser
        dirac_framebuf_t      *fbuf
        int                    frame_avail
        int                    verbose


    cdef dirac_decoder_t *dirac_decoder_init(int verbose)
    cdef void             dirac_decoder_close(dirac_decoder_t *decoder)

    cdef dirac_decoder_state_t dirac_parse(dirac_decoder_t *decoder)

    cdef void dirac_buffer(dirac_decoder_t *decoder, unsigned char *start, unsigned char *end)
    cdef void dirac_set_buf(dirac_decoder_t *decoder, unsigned char *buf[3], void *id)

#
#   APPEARS REMOVED
#
#    cdef void dirac_skip(dirac_decoder_t *decoder, int skip)


cdef extern from "Python.h": 
    object PyString_FromStringAndSize(char *, int)
    cdef char* PyString_AsString(object)

dirac_version = (1, 0, 2)


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
        while parse: # This looks un-necessary actually
            state = dirac_parse(self.decoder)

            if state == STATE_BUFFER:
                self.inputbuffer = "" # HMM
                raise DiracException("NEEDDATA")
 
            elif state == STATE_SEQUENCE:
                self.__extractSequenceData()
                self.__extractSourceData()
                self.__allocBuffers()
                raise DiracException("SEQINFO")

            elif state == STATE_PICTURE_AVAIL:
                parse = True
#                self.__extractFrameData()
                frame =  self.__buildFrame()
                self.__allocBuffers()
                return frame
    
            elif state == STATE_SEQUENCE_END:
                parse = False
                raise DiracException("END")
    
            elif state == STATE_INVALID:
                raise DiracException("STREAMERROR")
    
            else:
                raise DiracException("INTERNALFAULT")


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
            raise DiracException("NOTREADY")

    def __extractSequenceData(self):
#        cdef dirac_parseparams_t params
#        params        = self.decoder.parse_params
        cdef dirac_sourceparams_t params
        params = self.decoder.src_params


        width         = int(params.width)
        height        = int(params.height)
        chroma_width  = int(params.chroma_width)
        chroma_height = int(params.chroma_height)

        self.seqdata = { "size"          : (width, height),
                         "chroma_type"   :  __mapchromatype(params.chroma),
                         "chroma_size"   : (chroma_width, chroma_height),
#                         "bitdepth"      : int(params.video_depth),
                       }
                       
    def __extractSourceData(self):
        cdef dirac_sourceparams_t params
        
        params = self.decoder.src_params
        if params.frame_rate.denominator:
            numerator = params.frame_rate.numerator
            denominator = params.frame_rate.denominator
            framerate = float(numerator) / float(denominator)
        else:
            framerate = 0.0
            
        if params.pix_asr.denominator:
            numerator = params.pix_asr.numerator
            denominator = params.pix_asr.denominator
            pixelaspect = float(numerator) / float(denominator)
        else:
            pixelaspect = 1.0

        self.srcdata = { "interlaced"      : int(params.source_sampling), # 0 - progressive; 1 - interlaced
                         "topfieldfirst"   : int(params.topfieldfirst),
#                         "fieldsequencing" : int(params.seqfields),
                         "frame_rate"      : framerate,
                         "pixel_aspect"    : pixelaspect,

                        # FIXME ADD IN: these fields
                        # FIXME ADD IN:    clean_area
                        # FIXME ADD IN:    signal_range
                        # FIXME ADD IN:    colour_spec
                       }
                       
    def __extractFrameData(self):
        cdef dirac_parseparams_t parse_params
        cdef dirac_decoder_t decoder_params
#        print "parse_params", parse_params
#        print "decoder_params", decoder_params.frame_num

#        params = self.decoder.parse_params
#        
#        
        self.framedata = {
#            "frametype"      : __mapping_frame_type(params.ptype),
#            "reference_type" : __mapping_rframe_type(params.rtype),
            "frame number"   : int(decoder_params.frame_num),
#            "frame number"   : int(params.pnum),
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
#        frame.update(self.getFrameData())
        frame['yuv'] = (self.ybuffer, self.ubuffer, self.vbuffer)
#        print "HERE WE ARE"
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
        raise DiracException("INTERNALFAULT")

cdef object __mapping_frame_type(dirac_picture_type_t ftype):
    if ftype == INTRA_PICTURE:
        return "INTRA"
    else:
        return "INTER"

cdef object __mapping_rframe_type(dirac_reference_type_t rtype):
    if rtype == REFERENCE_PICTURE:
        return "REFERENCE"
    else:
        return "NON_REFERENCE"

