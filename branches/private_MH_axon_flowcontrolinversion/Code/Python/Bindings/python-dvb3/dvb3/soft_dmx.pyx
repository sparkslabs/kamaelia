# software demultiplexing of transport stream packets
# implemented here for efficiency

cdef extern from "Python.h": 
    object PyString_FromStringAndSize(char *, int)
    cdef char* PyString_AsString(object)


cdef class SoftDemux:

    cdef object         frag_buffer
    cdef unsigned char *cfrag

    cdef long int cfrag_remaining
    cdef long int length

    def __new__(self):
        self.frag_buffer = []
        self.cfrag_remaining = 0
        self.length = 0


    def insert(self, fragment):
#        """Insert a fragment of transport stream into the demuxer.
#           You should then call pop() repeatedly to fetch TS packets
#           until it returns None
#        """
        fraglen = len(fragment)

        self.frag_buffer.append(fragment)

        if self.length == 0:
            self.cfrag = <unsigned char*>PyString_AsString(self.frag_buffer[0])
            self.cfrag_remaining = len(self.frag_buffer[0])

        self.length = self.length + fraglen


    def pop(self):
#        """Returns (pid,error_flag,scrambled_flag,packet) or None.
#           Call repeatedly to get packets, until None is returned.
#        """
        while self.length >= 188:
            if self.cfrag[0] == 0x47:                    # start of TS packet
                return self.extractPacket()
            else:
                self.cfrag = self.cfrag + 1
                self.cfrag_remaining = self.cfrag_remaining - 1
                if self.cfrag_remaining == 0:
                    self.cfrag = <unsigned char*>PyString_AsString(self.frag_buffer[0])
                    self.cfrag_remaining = len(self.frag_buffer[0])
                    del self.frag_buffer[0]
                self.length = self.length - 1

    cdef extractPacket(self):
        cdef int i
        cdef unsigned char *cbytes

        packet = PyString_FromStringAndSize(NULL, 188)
        cbytes = <unsigned char*>PyString_AsString(packet)

        # copy the 188 bytes of packet out of the buffer and into the new string
        for i from 0 <= i < 188:
            cbytes[i] = self.cfrag[0]

            self.cfrag = self.cfrag + 1
            self.cfrag_remaining = self.cfrag_remaining - 1
            if self.cfrag_remaining == 0:
                self.cfrag = <unsigned char*>PyString_AsString(self.frag_buffer[0])
                self.cfrag_remaining = len(self.frag_buffer[0])
                del self.frag_buffer[0]

        self.length = self.length - 188

        pid       = ((cbytes[1] << 8) + cbytes[2]) & 0x1fff
        error     = cbytes[1] & 0x80
        scrambled = cbytes[3] & 0xc0

        return (pid, error, scrambled, packet)
