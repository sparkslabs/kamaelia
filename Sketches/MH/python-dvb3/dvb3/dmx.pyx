from clib cimport O_RDONLY, O_RDWR, O_NONBLOCK, F_SETFL
from clib cimport errno
from clib cimport strerror, ioctl, fcntl, open, close, memset

cimport cdmx

import exceptions
import errno as py_errno

cdef extern from "errno.h": pass
cdef extern from "string.h": pass
cdef extern from "sys/types.h": pass
cdef extern from "sys/stat.h": pass
cdef extern from "sys/ioctl.h": pass
cdef extern from "fcntl.h": pass
cdef extern from "unistd.h": pass

cdef extern from "linux/dvb/dmx.h": pass

ctypedef unsigned int __u32


# ==============================================================================


DMX_FILTER_SIZE = cdmx.DMX_FILTER_SIZE

DMX_OUT_DECODER = cdmx.DMX_OUT_DECODER
DMX_OUT_TAP = cdmx.DMX_OUT_TAP
DMX_OUT_TS_TAP = cdmx.DMX_OUT_TS_TAP

DMX_IN_FRONTEND = cdmx.DMX_IN_FRONTEND
DMX_IN_DVR = cdmx.DMX_IN_DVR

DMX_PES_AUDIO = cdmx.DMX_PES_AUDIO
DMX_PES_VIDEO = cdmx.DMX_PES_VIDEO
DMX_PES_TELETEXT = cdmx.DMX_PES_TELETEXT
DMX_PES_SUBTITLE = cdmx.DMX_PES_SUBTITLE
DMX_PES_PCR = cdmx.DMX_PES_PCR
DMX_PES_OTHER = cdmx.DMX_PES_OTHER

DMX_SCRAMBLING_EV = cdmx.DMX_SCRAMBLING_EV
DMX_FRONTEND_EV = cdmx.DMX_FRONTEND_EV

DMX_SCRAMBLING_OFF = cdmx.DMX_SCRAMBLING_OFF
DMX_SCRAMBLING_ON = cdmx.DMX_SCRAMBLING_ON

DMX_CHECK_CRC = cdmx.DMX_CHECK_CRC
DMX_ONESHOT = cdmx.DMX_ONESHOT
DMX_IMMEDIATE_START = cdmx.DMX_IMMEDIATE_START


# ==============================================================================


cdef int get_ioctl_int(int fd, int cmd):
    cdef __u32 value
    value = 0
    if ioctl(fd, cmd, &value) == -1:
        raise IOError(errno, strerror(errno))
    return value

cdef void set_ioctl_int(int fd, int cmd, int value):
    if ioctl(self.fd, cmd, value) == -1:
        raise_ioerror()

cdef raise_ioerror():
    raise IOError(errno, strerror(errno))


cdef class Demux:
    cdef int fd

    def __new__(self, card, blocking=1, *args, **kwargs):
        cdef int flags

        filename = "/dev/dvb/adapter" + str(card) + "/demux0"
        if not blocking:
            flags = O_NONBLOCK | O_RDWR
        else:
            flags = O_RDWR
        self.fd = open(filename, flags)
        if self.fd == -1:
            raise_ioerror()

    def __dealloc__(self):
        close(self.fd)

    def fileno(self):
        return self.fd

    def set_blocking(self, blocking):
        if blocking:
            fcntl(self.fd, F_SETFL, 0)
        else:
            fcntl(self.fd, F_SETFL, O_NONBLOCK)


    def start(self):
        """Start the filtering operation defined via calls to set_filter or
        set_pes_filter."""
        global cdmx
        if ioctl(self.fd, cdmx.DMX_START) == -1:
            raise_ioerror()

    def stop(self):
        """Stop the filtering operation defined via calls to set_filter or
        set_pes_filter."""
        global cdmx
        if ioctl(self.fd, cdmx.DMX_STOP) == -1:
            raise_ioerror()

    def set_filter(self, pid, filter, mask, mode, timeout, flags):
        """Set up a filter according to the filter and mask arguments."""
        global cdmx
        cdef cdmx.dmx_sct_filter_params p
        cdef int i

        if len(filter) != len(mask) or len(filter) > cdmx.DMX_FILTER_SIZE:
            raise IOError(py_errno.EINVAL, strerror(py_errno.EINVAL))
        if mode is not None and len(mode) != len(filter):
            raise IOError(py_errno.EINVAL, strerror(py_errno.EINVAL))

        p.pid = pid
        p.timeout = timeout
        p.flags = flags
        memset(&p.filter.filter, 0, cdmx.DMX_FILTER_SIZE)
        memset(&p.filter.mask, 0, cdmx.DMX_FILTER_SIZE)
        memset(&p.filter.mode, 0, cdmx.DMX_FILTER_SIZE)
        for i from 0 <= i < len(filter):
            p.filter.filter[i] = filter[i]
            p.filter.mask[i] = mask[i]
            if mode is not None:
                p.filter.mode[i] = mode[i]

        if ioctl(self.fd, cdmx.DMX_SET_FILTER, &p) == -1:
            raise_ioerror()

    def set_pes_filter(self, pid, input, output, pes_type, flags):
        """Setup up a PES filter according to the parameters provided."""
        global cdmx
        cdef cdmx.dmx_pes_filter_params p

        p.pid = pid
        p.input = input
        p.output = output
        p.pes_type = pes_type
        p.flags = flags

        if ioctl(self.fd, cdmx.DMX_SET_PES_FILTER, &p) == -1:
            raise_ioerror()

    def set_buffer_size(self, size):
        """Set the size of the circular buffer used for filtered data."""
        global cdmx
        set_ioctl_int(self.fd, cdmx.DMX_SET_BUFFER_SIZE, size)

    def get_event(self):
        """Returns an event, if available."""
        global cdmx
        cdef cdmx.dmx_event e

        e.event = 0
        e.u.scrambling = 0
        if ioctl(self.fd, cdmx.DMX_GET_EVENT, &e) == -1:
            raise_ioerror()
        return e.event, e.timeStamp, e.u.scrambling

    def get_stc(self, num):
        global cdmx
        cdef cdmx.dmx_stc stc

        stc.num = num
        if ioctl(self.fd, cdmx.DMX_GET_STC, &stc) == -1:
            raise_ioerror()
        return stc.base, stc.stc
