cdef extern from *:
    ctypedef unsigned int __u32
    ctypedef unsigned char __u8

    enum:
        FE_GET_INFO

        FE_DISEQC_RESET_OVERLOAD
        FE_DISEQC_SEND_MASTER_CMD
        FE_DISEQC_RECV_SLAVE_REPLY
        FE_DISEQC_SEND_BURST

        FE_SET_TONE
        FE_SET_VOLTAGE
        FE_ENABLE_HIGH_LNB_VOLTAGE

        FE_READ_STATUS
        FE_READ_BER
        FE_READ_SIGNAL_STRENGTH
        FE_READ_SNR
        FE_READ_UNCORRECTED_BLOCKS

        FE_SET_FRONTEND
        FE_GET_FRONTEND
        FE_GET_EVENT


    # frontend type
    ctypedef enum fe_type_t:
        FE_QPSK     # DVB-S
        FE_QAM      # DVB-C
        FE_OFDM     # DVB-T

    # frontend capabilities
    ctypedef enum fe_caps_t:
        FE_IS_STUPID                  = 0x00000000
        FE_CAN_INVERSION_AUTO         = 0x00000001
        FE_CAN_FEC_1_2                = 0x00000002
        FE_CAN_FEC_2_3                = 0x00000004
        FE_CAN_FEC_3_4                = 0x00000008
        FE_CAN_FEC_4_5                = 0x00000010
        FE_CAN_FEC_5_6                = 0x00000020
        FE_CAN_FEC_6_7                = 0x00000040
        FE_CAN_FEC_7_8                = 0x00000080
        FE_CAN_FEC_8_9                = 0x00000100
        FE_CAN_FEC_AUTO               = 0x00000200
        FE_CAN_QPSK                   = 0x00000400
        FE_CAN_QAM_16                 = 0x00000800
        FE_CAN_QAM_32                 = 0x00001000
        FE_CAN_QAM_64                 = 0x00002000
        FE_CAN_QAM_128                = 0x00004000
        FE_CAN_QAM_256                = 0x00008000
        FE_CAN_QAM_AUTO               = 0x00010000
        FE_CAN_TRANSMISSION_MODE_AUTO = 0x00020000
        FE_CAN_BANDWIDTH_AUTO         = 0x00040000
        FE_CAN_GUARD_INTERVAL_AUTO    = 0x00080000
        FE_CAN_HIERARCHY_AUTO         = 0x00100000
        FE_CAN_8VSB                   = 0x00200000
        FE_CAN_16VSB                  = 0x00400000
        FE_NEEDS_BENDING              = 0x20000000
        FE_CAN_RECOVER                = 0x40000000
        FE_CAN_MUTE_TS                = 0x80000000

    # frontend information
    cdef struct dvb_frontend_info:
        char        name[128]
        fe_type_t   type
        __u32       frequency_min
        __u32       frequency_max
        __u32       frequency_stepsize
        __u32       frequency_tolerance
        __u32       symbol_rate_min
        __u32       symbol_rate_max
        __u32       symbol_rate_tolerance   # ppm
        __u32       notifier_delay          # ms [DEPRECATED]
        fe_caps_t   caps

    # diseqc master command
    cdef struct dvb_diseqc_master_cmd:
        __u8        msg[6]      # { framing, address, command, data[3] }
        __u8        msg_len     # valid values are 3...6

    # diseqc slave reply
    cdef struct dvb_diseqc_slave_reply:
        __u8        msg[4]      # { framing, data[3] }
        __u8        msg_len     # valid values are 0...4, 0 means no msg
        int         timeout     # return from ioctl after timeout ms with
                                # errorcode when no message was received

    # SEC voltage
    ctypedef enum fe_sec_voltage_t:
        SEC_VOLTAGE_13
        SEC_VOLTAGE_18
        SEC_VOLTAGE_OFF

    # SEC continuous tone
    ctypedef enum fe_sec_tone_mode_t:
        SEC_TONE_ON
        SEC_TONE_OFF

    # SEC tone burst
    ctypedef enum fe_sec_mini_cmd_t:
        SEC_MINI_A
        SEC_MINI_B

    # frontend status
    ctypedef enum fe_status_t:
        FE_HAS_SIGNAL   = 0x01      # found something above the noise level
        FE_HAS_CARRIER  = 0x02      # found a DVB signal
        FE_HAS_VITERBI  = 0x04      # FEC is stable
        FE_HAS_SYNC     = 0x08      # found sync bytes
        FE_HAS_LOCK     = 0x10      # everything's working...
        FE_TIMEDOUT     = 0x20      # no lock within the last ~2 seconds
        FE_REINIT       = 0x40      # frontend was reinitialized,
                                    # application is recommended to reset

    # frontend parameters
    ctypedef enum fe_spectral_inversion_t:
        INVERSION_OFF
        INVERSION_ON
        INVERSION_AUTO

    ctypedef enum fe_code_rate_t:
        FEC_NONE = 0
        FEC_1_2
        FEC_2_3
        FEC_3_4
        FEC_4_5
        FEC_5_6
        FEC_6_7
        FEC_7_8
        FEC_8_9
        FEC_AUTO

    ctypedef enum fe_modulation_t:
        QPSK
        QAM_16
        QAM_32
        QAM_64
        QAM_128
        QAM_256
        QAM_AUTO

    ctypedef enum fe_transmit_mode_t:
        TRANSMISSION_MODE_2K
        TRANSMISSION_MODE_8K
        TRANSMISSION_MODE_AUTO

    ctypedef enum fe_bandwidth_t:
        BANDWIDTH_8_MHZ
        BANDWIDTH_7_MHZ
        BANDWIDTH_6_MHZ
        BANDWIDTH_AUTO

    ctypedef enum fe_guard_interval_t:
        GUARD_INTERVAL_1_32
        GUARD_INTERVAL_1_16
        GUARD_INTERVAL_1_8
        GUARD_INTERVAL_1_4
        GUARD_INTERVAL_AUTO

    ctypedef enum fe_hierarchy_t:
        HIERARCHY_NONE
        HIERARCHY_1
        HIERARCHY_2
        HIERARCHY_4
        HIERARCHY_AUTO

    cdef struct dvb_qpsk_parameters:
        __u32           symbol_rate # symbol rate in Symbols per second
        fe_code_rate_t  fec_inner   # forward error correction

    cdef struct dvb_qam_parameters:
        __u32           symbol_rate # symbol rate in Symbols per second
        fe_code_rate_t  fec_inner   # forward error correction
        fe_modulation_t modulation  # modulation type

    cdef struct dvb_ofdm_parameters:
        fe_bandwidth_t  bandwidth
        fe_code_rate_t  code_rate_HP    # high priority stream code rate
        fe_code_rate_t  code_rate_LP    # low priority stream code rate
        fe_modulation_t constellation   # modulation type
        fe_transmit_mode_t transmission_mode
        fe_guard_interval_t guard_interval
        fe_hierarchy_t  hierarchy_information

    cdef union dvb_frontend_parameters__u:
        dvb_qpsk_parameters qpsk
        dvb_qam_parameters  qam
        dvb_ofdm_parameters ofdm

    cdef struct dvb_frontend_parameters:
        __u32           frequency   # (absolute) frequency in Hz for QAM/OFDM
                                    # intermediate frequency in kHz for QPSK
        fe_spectral_inversion_t inversion
        dvb_frontend_parameters__u u

    # frontend events
    cdef struct dvb_frontend_event:
        fe_status_t     status
        dvb_frontend_parameters parameters
