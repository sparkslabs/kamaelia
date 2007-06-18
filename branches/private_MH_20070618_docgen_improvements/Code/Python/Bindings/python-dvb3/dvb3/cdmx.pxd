cdef extern from *:
    ctypedef unsigned long long __u64
    ctypedef unsigned int __u32
    ctypedef unsigned short __u16
    ctypedef unsigned char __u8
    ctypedef long time_t

    enum:
        DMX_START
        DMX_STOP
        DMX_SET_FILTER
        DMX_SET_PES_FILTER
        DMX_SET_BUFFER_SIZE
        DMX_GET_EVENT
        DMX_GET_PES_PIDS
        DMX_GET_CAPS
        DMX_GET_SOURCE
        DMX_GET_STC

        DMX_FILTER_SIZE

    ctypedef enum dmx_output_t:
        DMX_OUT_DECODER
        DMX_OUT_TAP
        DMX_OUT_TS_TAP

    ctypedef enum dmx_input_t:
        DMX_IN_FRONTEND
        DMX_IN_DVR

    ctypedef enum dmx_pes_type_t:
        DMX_PES_AUDIO0
        DMX_PES_VIDEO0
        DMX_PES_TELETEXT0
        DMX_PES_SUBTITLE0
        DMX_PES_PCR0

        DMX_PES_AUDIO1
        DMX_PES_VIDEO1
        DMX_PES_TELETEXT1
        DMX_PES_SUBTITLE1
        DMX_PES_PCR1

        DMX_PES_AUDIO2
        DMX_PES_VIDEO2
        DMX_PES_TELETEXT2
        DMX_PES_SUBTITLE2
        DMX_PES_PCR2

        DMX_PES_AUDIO3
        DMX_PES_VIDEO3
        DMX_PES_TELETEXT3
        DMX_PES_SUBTITLE3
        DMX_PES_PCR3

        DMX_PES_OTHER

    enum:
        DMX_PES_AUDIO = DMX_PES_AUDIO0
        DMX_PES_VIDEO = DMX_PES_VIDEO0
        DMX_PES_TELETEXT = DMX_PES_TELETEXT0
        DMX_PES_SUBTITLE = DMX_PES_SUBTITLE0
        DMX_PES_PCR = DMX_PES_PCR0

#    ctypedef enum dmx_event_t:
#        DMX_SCRAMBLING_EV
#        DMX_FRONTEND_EV

#    ctypedef enum dmx_scrambling_status_t:
#        DMX_SCRAMBLING_OFF
#        DMX_SCRAMBLING_ON

    cdef struct dmx_filter:
        __u8            filter[DMX_FILTER_SIZE]
        __u8            mask[DMX_FILTER_SIZE]
        __u8            mode[DMX_FILTER_SIZE]

    cdef struct dmx_sct_filter_params:
        __u16           pid
        dmx_filter      filter
        __u32           timeout
        __u32           flags

    cdef enum:
        DMX_CHECK_CRC = 1
        DMX_ONESHOT = 2
        DMX_IMMEDIATE_START = 4
        DMX_KERNEL_CLIENT = 0x8000

    cdef struct dmx_pes_filter_params:
        __u16           pid
        dmx_input_t     input
        dmx_output_t    output
        dmx_pes_type_t  pes_type
        __u32           flags

#    cdef struct dmx_event__u:
#        dmx_scrambling_status_t scrambling

#    cdef struct dmx_event:
#        dmx_event_t     event
#        time_t          timeStamp
#        dmx_event__u    u

    ctypedef enum dmx_source_t:
        DMX_SOURCE_FRONT0 = 0
        DMX_SOURCE_FRONT1
        DMX_SOURCE_FRONT2
        DMX_SOURCE_FRONT3
        DMX_SOURCE_DVR0 = 16
        DMX_SOURCE_DVR1
        DMX_SOURCE_DVR2
        DMX_SOURCE_DVR3

    cdef struct dmx_stc:
        unsigned int    num     # input: which STC? 0..N
        unsigned int    base    # output: divisor for stc to get 90 kHz clock
        __u64           stc     # output: stc in 'base'*90 kHz units
