from clib cimport O_RDONLY, O_RDWR, O_NONBLOCK, F_SETFL
from clib cimport errno
from clib cimport strerror, ioctl, fcntl, open, close

cimport cfrontend

import exceptions
import errno as py_errno

cdef extern from "errno.h": pass
cdef extern from "string.h": pass
cdef extern from "sys/types.h": pass
cdef extern from "sys/stat.h": pass
cdef extern from "sys/ioctl.h": pass
cdef extern from "fcntl.h": pass
cdef extern from "unistd.h": pass

cdef extern from "linux/dvb/frontend.h": pass

ctypedef unsigned int __u32


# ==============================================================================


FE_QPSK = cfrontend.FE_QPSK
FE_QAM = cfrontend.FE_QAM
FE_OFDM = cfrontend.FE_OFDM

SEC_VOLTAGE_13 = cfrontend.SEC_VOLTAGE_13
SEC_VOLTAGE_18 = cfrontend.SEC_VOLTAGE_18
SEC_VOLTAGE_OFF = cfrontend.SEC_VOLTAGE_OFF

SEC_TONE_ON = cfrontend.SEC_TONE_ON
SEC_TONE_OFF = cfrontend.SEC_TONE_OFF

SEC_MINI_A = cfrontend.SEC_MINI_A
SEC_MINI_B = cfrontend.SEC_MINI_B

FE_HAS_SIGNAL = cfrontend.FE_HAS_SIGNAL
FE_HAS_CARRIER = cfrontend.FE_HAS_CARRIER
FE_HAS_VITERBI = cfrontend.FE_HAS_VITERBI
FE_HAS_SYNC = cfrontend.FE_HAS_SYNC
FE_HAS_LOCK = cfrontend.FE_HAS_LOCK
FE_TIMEDOUT = cfrontend.FE_TIMEDOUT
FE_REINIT = cfrontend.FE_REINIT

INVERSION_OFF = cfrontend.INVERSION_OFF
INVERSION_ON = cfrontend.INVERSION_ON
INVERSION_AUTO = cfrontend.INVERSION_AUTO

FEC_NONE = cfrontend.FEC_NONE
FEC_1_2 = cfrontend.FEC_1_2
FEC_2_3 = cfrontend.FEC_2_3
FEC_3_4 = cfrontend.FEC_3_4
FEC_4_5 = cfrontend.FEC_4_5
FEC_5_6 = cfrontend.FEC_5_6
FEC_6_7 = cfrontend.FEC_6_7
FEC_7_8 = cfrontend.FEC_7_8
FEC_8_9 = cfrontend.FEC_8_9
FEC_AUTO = cfrontend.FEC_AUTO

QPSK = cfrontend.QPSK
QAM_16 = cfrontend.QAM_16
QAM_32 = cfrontend.QAM_32
QAM_64 = cfrontend.QAM_64
QAM_128 = cfrontend.QAM_128
QAM_256 = cfrontend.QAM_256
QAM_AUTO = cfrontend.QAM_AUTO

FE_IS_STUPID = cfrontend.FE_IS_STUPID
FE_CAN_INVERSION_AUTO = cfrontend.FE_CAN_INVERSION_AUTO
FE_CAN_FEC_1_2 = cfrontend.FE_CAN_FEC_1_2
FE_CAN_FEC_2_3 = cfrontend.FE_CAN_FEC_2_3
FE_CAN_FEC_3_4 = cfrontend.FE_CAN_FEC_3_4
FE_CAN_FEC_4_5 = cfrontend.FE_CAN_FEC_4_5
FE_CAN_FEC_5_6 = cfrontend.FE_CAN_FEC_5_6
FE_CAN_FEC_6_7 = cfrontend.FE_CAN_FEC_6_7
FE_CAN_FEC_7_8 = cfrontend.FE_CAN_FEC_7_8
FE_CAN_FEC_8_9 = cfrontend.FE_CAN_FEC_8_9
FE_CAN_FEC_AUTO = cfrontend.FE_CAN_FEC_AUTO
FE_CAN_QPSK = cfrontend.FE_CAN_QPSK
FE_CAN_QAM_16 = cfrontend.FE_CAN_QAM_16
FE_CAN_QAM_32 = cfrontend.FE_CAN_QAM_32
FE_CAN_QAM_64 = cfrontend.FE_CAN_QAM_64
FE_CAN_QAM_128 = cfrontend.FE_CAN_QAM_128
FE_CAN_QAM_256 = cfrontend.FE_CAN_QAM_256
FE_CAN_QAM_AUTO = cfrontend.FE_CAN_QAM_AUTO
FE_CAN_TRANSMISSION_MODE_AUTO = cfrontend.FE_CAN_TRANSMISSION_MODE_AUTO
FE_CAN_BANDWIDTH_AUTO = cfrontend.FE_CAN_BANDWIDTH_AUTO
FE_CAN_GUARD_INTERVAL_AUTO = cfrontend.FE_CAN_GUARD_INTERVAL_AUTO
FE_CAN_HIERARCHY_AUTO = cfrontend.FE_CAN_HIERARCHY_AUTO
FE_NEEDS_BENDING = cfrontend.FE_NEEDS_BENDING
FE_CAN_RECOVER = cfrontend.FE_CAN_RECOVER
FE_CAN_MUTE_TS = cfrontend.FE_CAN_MUTE_TS

TRANSMISSION_MODE_2K = cfrontend.TRANSMISSION_MODE_2K
TRANSMISSION_MODE_8K = cfrontend.TRANSMISSION_MODE_8K
TRANSMISSION_MODE_AUTO = cfrontend.TRANSMISSION_MODE_AUTO

BANDWIDTH_8_MHZ = cfrontend.BANDWIDTH_8_MHZ
BANDWIDTH_7_MHZ = cfrontend.BANDWIDTH_7_MHZ
BANDWIDTH_6_MHZ = cfrontend.BANDWIDTH_6_MHZ
BANDWIDTH_AUTO = cfrontend.BANDWIDTH_AUTO

GUARD_INTERVAL_1_32 = cfrontend.GUARD_INTERVAL_1_32
GUARD_INTERVAL_1_16 = cfrontend.GUARD_INTERVAL_1_16
GUARD_INTERVAL_1_8 = cfrontend.GUARD_INTERVAL_1_8
GUARD_INTERVAL_1_4 = cfrontend.GUARD_INTERVAL_1_4
GUARD_INTERVAL_AUTO = cfrontend.GUARD_INTERVAL_AUTO

HIERARCHY_NONE = cfrontend.HIERARCHY_NONE
HIERARCHY_1 = cfrontend.HIERARCHY_1
HIERARCHY_2 = cfrontend.HIERARCHY_2
HIERARCHY_4 = cfrontend.HIERARCHY_4
HIERARCHY_AUTO = cfrontend.HIERARCHY_AUTO


# ==============================================================================


class ParameterError(exceptions.Exception):
    pass


class QPSKParameters:

    def __init__(self, frequency=0, inversion=0, symbol_rate=0, fec_inner=0):
        self.frequency = frequency
        self.inversion = inversion
        self.symbol_rate = symbol_rate
        self.fec_inner = fec_inner

class QAMParameters:

    def __init__(self, frequency=0, inversion=0, symbol_rate=0, fec_inner=0,
            modulation=0):
        self.frequency = frequency
        self.inversion = inversion
        self.symbol_rate = symbol_rate
        self.fec_inner = fec_inner
        self.modulation = modulation

    def __repr__(self):
        return "<%s frequency=%d Hz, inversion=%s, symbol_rate=%d sym/s, fec_inner=%s, modulation=%s>" % (
                self.__class__.__name__,
                self.frequency,
                inversion2str(self.inversion),
                self.symbol_rate,
                fec2str(self.fec_inner),
                modulation2str(self.modulation)
        )

class OFDMParameters:

    def __init__(self, frequency=0, inversion=0, bandwidth=0, code_rate_HP=0,
            code_rate_LP=0, constellation=0, transmission_mode=0,
            guard_interval=0, hierarchy_information=0):
        self.frequency = frequency
        self.inversion = inversion
        self.bandwidth = bandwidth
        self.code_rate_HP = code_rate_HP
        self.code_rate_LP = code_rate_LP
        self.constellation = constellation
        self.transmission_mode = transmission_mode
        self.guard_interval = guard_interval
        self.hierarchy_information = hierarchy_information

    def __repr__(self):
        return "<%s frequency=%d Hz, inversion=%s, bandwidth=%s, code_rate_HP=%s, code_rate_LP=%s, constellation=%s, transmission_mode=%s, guard_interval=%s, hierarchy_information=%s>" % (
                self.__class__.__name__,
                self.frequency,
                inversion2str(self.inversion),
                bandwidth2str(self.bandwidth),
                fec2str(self.code_rate_HP),
                fec2str(self.code_rate_LP),
                constellation2str(self.constellation),
                transmission2str(self.transmission_mode),
                guard2str(self.guard_interval),
                hierarchy2str(self.hierarchy_information)
        )


cdef object inversion2str(i):
    if i == 0:
        return "off"
    elif i == 1:
        return "on"
    elif i == 2:
        return "auto"
    return "?"

cdef object fec2str(fec):
    if fec == 0:
        return "FEC_NONE"
    elif fec < 9:
        return "FEC_" + str(fec) + "_" + str(fec + 1)
    elif self.fec_inner == 9:
        return "FEC_AUTO"
    else:
        return "?"

cdef object modulation2str(m):
    if m == 0:
        return "QPSK"
    elif m == 6:
        return "QAM_AUTO"
    elif m > 6:
        return "?"
    else:
        return "QAM_" + str(8 << m)

cdef object bandwidth2str(b):
    if b == 3:
        return "BANDWIDTH_AUTO"
    elif b < 3:
        return "BANDWIDTH_" + str(8 - b) + "_MHZ"
    else:
        return "?"

cdef object constellation2str(c):
    if c == 0:
        return "QPSK"
    elif c == 1:
        return "QAM_16"
    elif c == 3:
        return "QAM_64"
    else:
        return "?"

cdef object transmission2str(t):
    if t == 0:
        return "TRANSMISSION_MODE_2K"
    elif t == 1:
        return "TRANSMISSION_MODE_8K"
    else:
        return "?"

cdef object guard2str(g):
    if g < 4:
        return "GUARD_INTERVAL_" + str(4 << (3 - g))
    else:
        return "?"

cdef object hierarchy2str(h):
    if h == 0:
        return "HIERARCHY_NONE"
    elif h < 4:
        return "HIERARCHY_" + str(1 << (h - 1))
    else:
        return "?"


cdef object unpack_parameters(cfrontend.dvb_frontend_parameters *p, object t):
    global cfrontend
    if t is QPSKParameters:
        return QPSKParameters(
            frequency=p.frequency,
            inversion=p.inversion,
            symbol_rate=p.u.qpsk.symbol_rate,
            fec_inner=p.u.qpsk.fec_inner
        )
    elif t is QAMParameters:
        return QAMParameters(
            frequency=p.frequency,
            inversion=p.inversion,
            symbol_rate=p.u.qam.symbol_rate,
            fec_inner=p.u.qam.fec_inner,
            modulation=p.u.qam.modulation
        )
    else:
        return OFDMParameters(
            frequency=p.frequency,
            inversion=p.inversion,
            bandwidth=p.u.ofdm.bandwidth,
            code_rate_HP=p.u.ofdm.code_rate_HP,
            code_rate_LP=p.u.ofdm.code_rate_LP,
            transmission_mode=p.u.ofdm.transmission_mode,
            guard_interval=p.u.ofdm.guard_interval,
            hierarchy_information=p.u.ofdm.hierarchy_information
        )

cdef int pack_parameters(cfrontend.dvb_frontend_parameters *p, object o):
    if o is None:
        return 0
    if isinstance(o, QPSKParameters):
        p.frequency = o.frequency
        p.inversion = o.inversion
        p.u.qpsk.symbol_rate = o.symbol_rate
        p.u.qpsk.fec_inner = o.fec_inner
        return 1
    elif isinstance(o, QAMParameters):
        p.frequency = o.frequency
        p.inversion = o.inversion
        p.u.qam.symbol_rate = o.symbol_rate
        p.u.qam.fec_inner = o.fec_inner
        p.u.qam.modulation = o.modulation
        return 1
    elif isinstance(o, OFDMParameters):
        p.frequency = o.frequency
        p.inversion = o.inversion
        p.u.ofdm.bandwidth = o.bandwidth
        p.u.ofdm.code_rate_HP = o.code_rate_HP
        p.u.ofdm.code_rate_LP = o.code_rate_LP
        p.u.ofdm.constellation = o.constellation
        p.u.ofdm.transmission_mode = o.transmission_mode
        p.u.ofdm.guard_interval = o.guard_interval
        p.u.ofdm.hierarchy_information = o.hierarchy_information
        return 1
    else:
        return 0


# ==============================================================================


class FrontendInfo:

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.type = kwargs.get("type", 0)
        self.frequency_min = kwargs.get("frequency_min", 0)
        self.frequency_max = kwargs.get("frequency_max", 0)
        self.frequency_stepsize = kwargs.get("frequency_stepsize", 0)
        self.frequency_tolerance = kwargs.get("frequency_tolerance", 0)
        self.symbol_rate_min = kwargs.get("symbol_rate_min", 0)
        self.symbol_rate_max = kwargs.get("symbol_rate_max", 0)
        self.symbol_rate_tolerance = kwargs.get("symbol_rate_tolerance", 0)
        self.notifier_delay = kwargs.get("notifier_delay", 0)
        self.caps = kwargs.get("caps", 0)


cdef unpack_info(cfrontend.dvb_frontend_info *i):
    return FrontendInfo(
        name=i.name,
        type=i.type,
        frequency_min=i.frequency_min,
        frequency_max=i.frequency_max,
        frequency_stepsize=i.frequency_stepsize,
        frequency_tolerance=i.frequency_tolerance,
        symbol_rate_min=i.symbol_rate_min,
        symbol_rate_max=i.symbol_rate_max,
        symbol_rate_tolerance=i.symbol_rate_tolerance,
        notifier_delay=i.notifier_delay,
        caps=i.caps
    )


# ==============================================================================


cdef int get_ioctl_int(int fd, int cmd):
    cdef __u32 value
    value = 0
    if ioctl(fd, cmd, &value) == -1:
        raise IOError(errno, strerror(errno))
    return value

cdef void set_ioctl_int(int fd, int cmd, int value):
    if ioctl(fd, cmd, value) == -1:
        raise_ioerror()

cdef raise_ioerror():
    raise IOError(errno, strerror(errno))


cdef class Frontend:
    cdef int fd
    cdef object t

    def __new__(self, card, rw=1, blocking=1, *args, **kwargs):
        global cfrontend
        cdef int flags
        cdef cfrontend.dvb_frontend_info info

        filename = "/dev/dvb/adapter" + str(card) + "/frontend0"
        flags = 0
        if rw:
            flags = flags | O_RDWR
        else:
            flags = flags | O_RDONLY
        if not blocking:
            flags = flags | O_NONBLOCK
        self.fd = open(filename, flags)
        if self.fd == -1:
            raise_ioerror()

        if ioctl(self.fd, cfrontend.FE_GET_INFO, &info) == -1:
            raise IOError(errno, strerror(errno))
        if info.type == cfrontend.FE_QPSK:
            self.t = QPSKParameters
        elif info.type == cfrontend.FE_QAM:
            self.t = QAMParameters
        else:
            self.t = OFDMParameters

    def __dealloc__(self):
        close(self.fd)

    def fileno(self):
        return self.fd

    def set_blocking(self, blocking):
        if blocking:
            fcntl(self.fd, F_SETFL, 0)
        else:
            fcntl(self.fd, F_SETFL, O_NONBLOCK)


    def read_status(self):
        """Returns status information about the front-end."""
        global cfrontend
        return get_ioctl_int(self.fd, cfrontend.FE_READ_STATUS)

    def read_ber(self):
        """Return the bit error rate for the signal currently received by the
        front-end."""
        global cfrontend
        return get_ioctl_int(self.fd, cfrontend.FE_READ_BER)

    def read_snr(self):
        """Returns the signal-to-noise ratio for the signal current received by
        the front-end."""
        global cfrontend
        return get_ioctl_int(self.fd, cfrontend.FE_READ_SNR)

    def read_signal_strength(self):
        """Returns the signal strength value for the signal currently received
        by the front-end."""
        global cfrontend
        return get_ioctl_int(self.fd, cfrontend.FE_READ_SIGNAL_STRENGTH)

    def read_uncorrected_blocks(self):
        """Returns the number of uncorrected blocks detected by the device
        driver during its lifetime.  The counter will wrap to zero after
        reaching its upper bound."""
        global cfrontend
        return get_ioctl_int(self.fd, cfrontend.FE_READ_UNCORRECTED_BLOCKS)

    def set_frontend(self, parameters):
        global cfrontend
        cdef cfrontend.dvb_frontend_parameters p
        if pack_parameters(&p, parameters) == 0:
            raise ParameterError, "Incorrect parameter type"
        if ioctl(self.fd, cfrontend.FE_SET_FRONTEND, &p) == -1:
            raise_ioerror()

    def get_frontend(self):
        global cfrontend
        cdef cfrontend.dvb_frontend_parameters p
        if ioctl(self.fd, cfrontend.FE_GET_FRONTEND, &p) == -1:
            raise_ioerror()
        return unpack_parameters(&p, self.t)

    def get_event(self):
        global cfrontend
        cdef cfrontend.dvb_frontend_event e
        if ioctl(self.fd, cfrontend.FE_GET_EVENT, &e) == -1:
            raise_ioerror()
        return e.status, unpack_parameters(&e.parameters, self.t)

    def get_info(self):
        global cfrontend
        cdef cfrontend.dvb_frontend_info i
        if ioctl(self.fd, cfrontend.FE_GET_INFO, &i) == -1:
            raise_ioerror()
        return unpack_info(&i)

    def diseqc_reset_overload(self):
        global cfrontend
        if ioctl(self.fd, cfrontend.FE_DISEQC_RESET_OVERLOAD) == -1:
            raise_ioerror()

    def diseqc_send_master_cmd(self, framing, address, command, data=[]):
        global cfrontend
        cdef cfrontend.dvb_diseqc_master_cmd c
        cdef int i
        if len(data) > 3:
            raise IOError(py_errno.EINVAL, strerror(py_errno.EINVAL))
        c.msg[0] = framing
        c.msg[1] = address
        c.msg[2] = command
        for i from 0 <= i < len(data):
            c.msg[3 + i] = data[i]
        c.msg_len = 3 + len(data)
        if ioctl(self.fd, cfrontend.FE_DISEQC_SEND_MASTER_CMD, &c) == -1:
            raise_ioerror()

    def diseqc_recv_slave_reply(self, timeout=0):
        global cfrontend
        cdef cfrontend.dvb_diseqc_slave_reply r
        r.timeout = timeout
        if ioctl(self.fd, cfrontend.FE_DISEQC_RECV_SLAVE_REPLY, &r) == -1:
            raise_ioerror()
        if r.msg_len == 0:
            return None, None
        framing = <int> r.msg[0]
        data = []
        for i from 1 <= i < r.msg_len:
            data.append(r.msg[i])
        return framing, data

    def diseqc_send_burst(self, burst):
        global cfrontend
        set_ioctl_int(self.fd, cfrontend.FE_DISEQC_SEND_BURST, burst)

    def set_tone(self, tone):
        global cfrontend
        set_ioctl_int(self.fd, cfrontend.FE_SET_TONE, tone)

    def set_voltage(self, voltage):
        global cfrontend
        set_ioctl_int(self.fd, cfrontend.FE_SET_VOLTAGE, voltage)

    def enable_high_lnb_voltage(self, high):
        global cfrontend
        set_ioctl_int(self.fd, cfrontend.FE_ENABLE_HIGH_LNB_VOLTAGE, high)
