# software demultiplexing of transport stream packets
# implemented here for efficiency

cdef extern from "Python.h": 
    object PyString_FromStringAndSize(char *, int)
    cdef char* PyString_AsString(object)

cdef extern from "string.h":
    cdef void *memcpy(void *, void *, int)

cdef class SoftDemux:
    """\
    Fast software demuxer for MPEG TS packets.
    """

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
#           Call pop() repeatedly to fetch TS packets extracted.
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
            if self.cfrag[0] == 0x47:
                # we are at start of TS packet and have whole packet (length >= 188)
                return self.extractPacket()
            else:
                # not yet found start of TS packet, move onto next byte in buffers
                self.cfrag = self.cfrag + 1
                self.cfrag_remaining = self.cfrag_remaining - 1
                self.length = self.length - 1
                
                # if reached end of fragment, get rid of it, then if one is buffered, move onto next
                if self.cfrag_remaining == 0:
                    del self.frag_buffer[0]
                    if self.length > 0:
                        self.cfrag = <unsigned char*>PyString_AsString(self.frag_buffer[0])
                        self.cfrag_remaining = len(self.frag_buffer[0])


    cdef extractPacket(self):
        cdef int remaining
        cdef unsigned char *cbytes
        cdef int amount

        packet = PyString_FromStringAndSize(NULL, 188)
        cbytes = <unsigned char*>PyString_AsString(packet)

        # copy the 188 bytes of packet out of the buffer and into the new string
        remaining = 188
        while remaining > 0:
            amount = min(self.cfrag_remaining, remaining)
            memcpy(cbytes, self.cfrag, amount)
            
            remaining = remaining - amount
            cbytes = cbytes + amount
            self.cfrag = self.cfrag + amount
            self.cfrag_remaining = self.cfrag_remaining - amount
            self.length = self.length - amount
            
            # if reached end of fragment, get rid of it, then if one is buffered, move onto next
            if self.cfrag_remaining == 0:
                del self.frag_buffer[0]
                if self.length > 0:
                    self.cfrag = <unsigned char*>PyString_AsString(self.frag_buffer[0])
                    self.cfrag_remaining = len(self.frag_buffer[0])


        # go back to beginning of packet and extract pid and flags
        pid       = ((cbytes[1-188] << 8) + cbytes[2-188]) & 0x1fff
        error     = cbytes[1-188] & 0x80
        scrambled = cbytes[3-188] & 0xc0

        return (pid, error, scrambled, packet)
