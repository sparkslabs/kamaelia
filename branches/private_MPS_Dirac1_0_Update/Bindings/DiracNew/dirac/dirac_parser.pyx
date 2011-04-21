
cimport dirac_common 

DIRAC_RESEARCH_MAJOR_VERSION = dirac_common.DIRAC_RESEARCH_MAJOR_VERSION
DIRAC_RESEARCH_MINOR_VERSION = dirac_common.DIRAC_RESEARCH_MINOR_VERSION
DIRAC_RESEARCH_PATCH_VERSION = dirac_common.DIRAC_RESEARCH_PATCH_VERSION

NUM_WLT_FILTERS = dirac_common.NUM_WLT_FILTERS
version = DIRAC_RESEARCH_MAJOR_VERSION, DIRAC_RESEARCH_MINOR_VERSION, DIRAC_RESEARCH_PATCH_VERSION
dirac_version = version

def DIRAC_RESEARCH_VERSION(X, Y, Z):
    return (((X)<<16) + ((Y)<<8) + (Z))

DIRAC_RESEARCH_CURVERSION = DIRAC_RESEARCH_VERSION(DIRAC_RESEARCH_MAJOR_VERSION, DIRAC_RESEARCH_MINOR_VERSION, DIRAC_RESEARCH_PATCH_VERSION)


class DiracDecodeException(Exception):
    pass


cdef extern from "Python.h": 
    object PyString_FromStringAndSize(char *, int)
    cdef char* PyString_AsString(object)


cdef extern from "dirac/libdirac_decoder/decoder_types.h":
    #
    # Different states the parser is in
    #
    ctypedef enum DecoderState:
        STATE_BUFFER          # need more data input
        STATE_SEQUENCE        # start of sequence detected
        STATE_PICTURE_AVAIL   # decoded frame available
        STATE_SEQUENCE_END    # end of sequence detected
        STATE_INVALID         # invalid state. Stop further processing


cdef extern from "dirac/libdirac_decoder/dirac_parser.h":
    # Python wrapper around the C interface to Dirac decoder.
    # 

    ctypedef DecoderState dirac_decoder_state_t

    # Structure that holds the information returned by the parser
    ctypedef struct dirac_decoder_t:
        dirac_decoder_state_t state                    # parser state
        dirac_common.dirac_parseparams_t parse_params  # parse parameters
        dirac_common.dirac_sourceparams_t src_params   # source parameters
        unsigned int frame_num                         # frame (NOT picture) number
        void *parser                                   # void pointer to internal parser
        dirac_common.dirac_framebuf_t *fbuf            # frame (NOT picture) buffer to hold luma and chroma data
        int frame_avail                                # boolean flag that indicates if a decoded frame (NOT picture) is available
        int verbose                                    # verbose output


    cdef dirac_decoder_t *dirac_decoder_init(int verbose)
        # Decoder Init
        # Initialise the decoder. 
        #     \param  verbose boolean flag to set verbose output
        #     \return decoder handle


    cdef void dirac_decoder_close(dirac_decoder_t *decoder)
        # Release the decoder resources
        #     \param decoder  Decoder object


    cdef dirac_decoder_state_t dirac_parse (dirac_decoder_t *decoder)
        # Parses the data in the input buffer. This function returns the 
        # following values.
        #    STATE_BUFFER:         Not enough data in internal buffer to process 
        #    STATE_SEQUENCE:       Start of sequence detected. The seq_params member
        #                          in the decoder object is set to the details of the
        #                          next sequence to be processed.
        #    STATE_PICTURE_START:  Start of picture detected. The frame_params member
        #                          of the decoder object is set to the details of the
        #                          next frame to be processed.
        #    STATE_PICTURE_AVAIL:  Decoded picture available. The frame_aprams member
        #                          of the decoder object is set the the details of
        #                          the decoded frame available. The fbuf member of
        #                          the decoder object has the luma and chroma data of
        #                          the decompressed frame.
        #    STATE_SEQUENCE_END:   End of sequence detected.
        #    STATE_INVALID:        Invalid stream. Stop further processing.
        #
        #    \param decoder  Decoder object
        #    \return         Decoder state


    cdef void dirac_buffer (dirac_decoder_t *decoder, unsigned char *start, unsigned char *end)
        # Copy data into internal buffer
        #    \param decoder  Decoder object
        #    \param start    Start of data
        #    \param end      End of data


    cdef void dirac_set_buf (dirac_decoder_t *decoder, unsigned char *buf[3], void *id)
        # Set the output buffer into which the decoder copies the decoded data
        #    \param decoder  Decoder object
        #    \param buf      Array of char buffers to hold luma and chroma data
        #    \param id       User data


cdef class DiracDecoder:
    cdef dirac_decoder_t *decoder_handle
    cdef int c_verbose 
    cdef object source_params
    cdef object parse_params
    cdef unsigned char *cbuffers[3]        # buffers dirac will build frames into
    cdef object ybuffer
    cdef object ubuffer
    cdef object vbuffer

    def __cinit__(self, verbose=None):
        self.c_verbose = 0
        if verbose:
            self.c_verbose = 1
        self.decoder_handle = dirac_decoder_init(self.c_verbose)


    def verbose(self):
        return self.c_verbose


    def bufferData(self, data):
        cdef unsigned char *raw_data
        cdef unsigned char *raw_data_end
        cdef long int temp

        raw_data = <unsigned char*>PyString_AsString(data)
        temp = <long int>raw_data + len(data)
        raw_data_end = <unsigned char*>temp

        dirac_buffer(self.decoder_handle, raw_data, raw_data_end)


    def getFrame(self):
        cdef dirac_decoder_state_t state = dirac_parse(self.decoder_handle)

        if state == STATE_BUFFER:
            #  case STATE_BUFFER:
            #      read more data.
            #      Pass data to the decoder.
            #      dirac_buffer (decoder_handle, data_start, data_end)
            #      break;
            print "STATE_BUFFER"
            help = ( "    You need to read some data from a file\n"
                     "    You then need to pass in to the buffer:\n"
                     "        handle.bufferData(somedata)\n"
                     "    And then call getFrame() again" )
            raise DiracDecodeException("STATE_BUFFER", help)

        if state == STATE_SEQUENCE:
            #  case STATE_SEQUENCE:
            #      handle start of sequence.
            #      The decoder returns the sequence parameters in the seq_params member of the decoder handle.
            #      Allocate space for the frame data buffers and pass this to the decoder.
            #      dirac_set_buf (decoder_handle, buf, NULL);
            #      break;
            print "STATE_SEQUENCE"

            self.extract_source_params()
            self.extract_parse_params()
            self.allocate_buffers()
            raise DiracDecodeException("STATE_SEQUENCE", " no help yet ")


        if state == STATE_SEQUENCE_END:
            #  case STATE_SEQUENCE_END:
            #      Deallocate frame data buffers
            #      break;
            print "STATE_SEQUENCE_END"
            self.ybuffer = None
            self.ubuffer = None
            self.vbuffer = None
            raise DiracDecodeException("STATE_SEQUENCE_END", " no help yet ")


        if state == STATE_PICTURE_AVAIL:
            #  case STATE_PICTURE_AVAIL:
            #      Handle picture data.
            #      The decoder sets the fbuf member in the decoder handle to the frame decoded.
            #      break;
            print "STATE_PICTURE_AVAIL:"
            frame = {}
            frame.update(self.extract_source_params())
            frame["yuv"] = (self.ybuffer, self.ubuffer, self.vbuffer)
            return frame

        if state == STATE_INVALID:
            #  case STATE_INVALID:
            #      Unrecoverable error. Stop all processing
            #      break;
            print "STATE_INVALID:"
            raise DiracDecodeException("STATE_INVALID", " no help yet ")


    def extract_parse_params(self):
        cdef dirac_common.dirac_parseparams_t parse_params
        parse_params = self.decoder_handle.parse_params

        # Structure that holds the parase parameters */
        self.parse_params = {
            "major_ver" : int( parse_params.major_ver ),  # Major version
            "minor_ver" : int( parse_params.minor_ver ),  # Minor version
            "profile" : int( parse_params.profile ),      # Profile
            "level" : int( parse_params.level ),          # level
        }
        return self.parse_params


    def ParseParams(self):
        return self.parse_params


    def extract_source_params(self):
        cdef dirac_common.dirac_sourceparams_t params
        params = self.decoder_handle.src_params

        width = int(params.width)                                     #        unsigned int width                # numper of pixels per line
        height = int(params.height)                                   #        unsigned int height               # number of lines per frame
        chroma_width = int(params.chroma_width)                       #        unsigned int chroma_width         # numper of pixels of chroma per line
        chroma_height = int(params.chroma_height)                     #        unsigned int chroma_height        # number of lines of chroma per frame
        source_sampling = int(params.source_sampling)                 #        unsigned int source_sampling      # source sampling field: 0 - progressive; 1 - interlaced
        topfieldfirst = int(params.topfieldfirst)                     #        int topfieldfirst                 # top field comes first : 0 - false; 1 - true. Set by Dirac library.
        chroma = chroma_to_object(params.chroma)                      #        dirac_chroma_t chroma             # chroma type
        frame_rate = frame_rate_to_object(params.frame_rate)          #        dirac_frame_rate_t frame_rate     # frame rate
        pix_asr = pix_asr_to_object(params.pix_asr)                   #        dirac_pix_asr_t pix_asr           # pixel aspect ratio
        clean_area = clean_area_to_object(params.clean_area)          #        dirac_clean_area_t clean_area     # clean area
        signal_range = signal_range_to_object(params.signal_range)    #        dirac_signal_range_t signal_range # signal range
        colour_spec = dirac_colour_spec_to_object(params.colour_spec) #        dirac_colour_spec_t colour_spec   # colour specification

        self.source_params = {
            "width": width,
            "height": height,
            "chroma_width": chroma_width,
            "chroma_height": chroma_height,
            "source_sampling": source_sampling,
            "topfieldfirst": topfieldfirst,
            "chroma": chroma,
            "frame_rate": frame_rate,
            "pix_asr": pix_asr,
            "clean_area": clean_area,
            "signal_range": signal_range,
            "colour_spec": colour_spec
        }
        return self.source_params


    def SourceParams(self):
        # Accessor to enable source_params to be accessible from normal python code
        return self.source_params


    def allocate_buffers(self):
            #      handle start of sequence.
            #      The decoder returns the sequence parameters in the seq_params member of the decoder handle.
            #      Allocate space for the frame data buffers and pass this to the decoder.
            #      dirac_set_buf (decoder_handle, buf, NULL);
            #      break;
        ysize = self.source_params['width'] * self.source_params['height']
        usize = self.source_params['chroma_width'] * self.source_params['chroma_height']
        vsize = usize

        # new allocate uninitialised string buffers ... safe to modify
        self.ybuffer = PyString_FromStringAndSize(NULL, ysize)
        self.ubuffer = PyString_FromStringAndSize(NULL, usize)
        self.vbuffer = PyString_FromStringAndSize(NULL, vsize)

        self.cbuffers[0] = <unsigned char *>PyString_AsString(self.ybuffer)
        self.cbuffers[1] = <unsigned char *>PyString_AsString(self.ubuffer)
        self.cbuffers[2] = <unsigned char *>PyString_AsString(self.vbuffer)

        dirac_set_buf(self.decoder_handle, self.cbuffers, NULL)

    def __dealloc__(self):
        dirac_decoder_close(self.decoder_handle)


cdef object chroma_to_object(dirac_common.dirac_chroma_t chroma):
    # Convert the C-Space chroma type to a python-space chroma-type
    if chroma == dirac_common.format444:
        return "444"
    if chroma == dirac_common.format422:
        return "422"
    if chroma == dirac_common.format420:
        return "420"
    if chroma == dirac_common.formatNK:
        return "NK"
    raise DiracDecodeException("INTERNAL ERROR", "Chroma conversion failure")


cdef object frame_rate_to_object(dirac_common.dirac_frame_rate_t frame_rate):
    result = ( int(frame_rate.numerator) , int(frame_rate.denominator) )
    return result


cdef object pix_asr_to_object(dirac_common.dirac_pix_asr_t pix_asr):
    result = ( int(pix_asr.numerator) , int(pix_asr.denominator) )
    return result


cdef object clean_area_to_object(dirac_common.dirac_clean_area_t clean_area):
    result = {
        "width" : int( clean_area.width ),
        "height" : int( clean_area.height ),
        "left_offset" : int( clean_area.left_offset ),
        "top_offset" : int( clean_area.top_offset )
    }
    return result


cdef object signal_range_to_object(dirac_common.dirac_signal_range_t signal_range):
    result = {
        "luma_offset": int( signal_range.luma_offset ),
        "luma_excursion": int( signal_range.luma_excursion ),
        "chroma_offset": int( signal_range.chroma_offset ),
        "chroma_excursion": int( signal_range.chroma_excursion ),
    }
    return result


cdef object dirac_colour_spec_to_object(dirac_common.dirac_colour_spec_t colour_spec):
    result = {
        "col_primary" : dirac_col_primaries_to_object(colour_spec.col_primary),
        "col_matrix" : dirac_col_matrix_to_object(colour_spec.col_matrix),
        "trans_func" : dirac_transfer_func_to_object(colour_spec.trans_func)
    }
    return result


cdef object dirac_col_primaries_to_object(dirac_common.dirac_col_primaries_t col_primary):
    if col_primary == dirac_common.CP_HDTV_COMP_INTERNET:
        return "CP_HDTV_COMP_INTERNET"
    if col_primary == dirac_common.CP_SDTV_525:
        return "CP_SDTV_525"
    if col_primary == dirac_common.CP_SDTV_625:
        return "CP_SDTV_625"
    if col_primary == dirac_common.CP_DCINEMA:
        return "CP_DCINEMA"
    if col_primary == dirac_common.CP_UNDEF:
        return "CP_UNDEF"
    raise DiracDecodeException("INTERNAL ERROR", "colour primaries conversion failure")


cdef object dirac_col_matrix_to_object(dirac_common.dirac_col_matrix_t col_matrix):
    result = {
        "kr" : float(col_matrix.kr),
        "kb" : float(col_matrix.kb)
    }
    return result

cdef object dirac_transfer_func_to_object(dirac_common.dirac_transfer_func_t trans_func):
    if trans_func == dirac_common.TF_TV:
        return "TF_TV"
    if trans_func == dirac_common.TF_EXT_GAMUT:
        return "TF_EXT_GAMUT"
    if trans_func == dirac_common.TF_LINEAR:
        return "TF_LINEAR"
    if trans_func == dirac_common.TF_DCINEMA:
        return "TF_DCINEMA"
    if trans_func == dirac_common.TF_UNDEF:
        return "TF_UNDEF"
    raise DiracDecodeException("INTERNAL ERROR", "transfer function conversion failure")
