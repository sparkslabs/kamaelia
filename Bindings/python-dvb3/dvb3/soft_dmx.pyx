# software demultiplexing of transport stream packets
# implemented here for efficiency

cdef extern from "Python.h": 
    object PyString_FromStringAndSize(char *, int)
    cdef char* PyString_AsString(object)

cdef extern from "string.h":
    cdef void *memcpy(void *, void *, int)

cdef class SoftDemux:
#    """\
#    SoftDemux([pidfilter]) -> new SoftDemux object
#    
#    Fast software demuxer for MPEG TS packets.
#
#    Keyword arguments:
#    - pidfilter  -- None (default) to not filter, or list of PIDs to accept (all others will be filtered out)
#    """

    cdef object         frag_buffer
    cdef unsigned char *cfrag

    cdef long int cfrag_remaining
    cdef long int length

    cdef char pidfilter[8192]
    
    def __new__(self, pidfilter=None):
        cdef int pid
        
        self.frag_buffer = []
        self.cfrag_remaining = 0
        self.length = 0
        
        if pidfilter == None:
            for pid from 0 <= pid < 8192:
                self.pidfilter[pid] = 1
        else:
            for pid from 0 <= pid < 8192:
                if pid in pidfilter:
                    self.pidfilter[pid] = 1
                else:
                    self.pidfilter[pid] = 0


    def insert(self, fragment):
#        """Insert a fragment of transport stream into the demuxer.
#           Call fetch() to fetch TS packets extracted.
#        """
        cdef long int fraglen
        
        fraglen = len(fragment)

        self.frag_buffer.append(fragment)

        if self.length == 0:
            self.cfrag = <unsigned char*>PyString_AsString(self.frag_buffer[0])
            self.cfrag_remaining = len(self.frag_buffer[0])

        self.length = self.length + fraglen


    def fetch(self):
#        """Returns list containing extracted TS packets in order, or empty list
#           if none found.
#           Each entry is a tuple: (pid, erroneous, scrambled, packet)
#        """
        cdef object extracted
        cdef int remaining
        cdef int amount
        cdef unsigned char *cpacket
        cdef object packet
        cdef int pid
        cdef int scrambled
        cdef int error
        cdef int accepting
        
        extracted = []

        # loop through the buffer until we've less than a TS packet (188 bytes) left in it
        while self.length >= 188:
            
            if self.cfrag[0] == 0x47:
                # we are at start of TS packet and have whole packet (length >= 188)
                
                # we'll *provisionally* accept the packet
                accepting = -1
                
                # see if we can easily detect the PID early
                if self.cfrag_remaining >= 3:
                    pid = ((self.cfrag[1] << 8) + self.cfrag[2]) & 0x1fff
                    accepting = self.pidfilter[pid]
                    
                if accepting:  # != 0
                    # allocate python string we're going to put the packet into
                    packet = PyString_FromStringAndSize(NULL, 188)
                    cpacket = <unsigned char*>PyString_AsString(packet)
        
                # copy the 188 bytes of packet out of the buffer and into the new string
                # or if filtering, just skip forwards through the buffer
                remaining = 188
                while remaining > 0:
                    amount = min(self.cfrag_remaining, remaining)
                    
                    if accepting:
                        memcpy(cpacket, self.cfrag, amount)
                        cpacket = cpacket + amount
                    
                    remaining = remaining - amount
                    self.cfrag = self.cfrag + amount
                    self.cfrag_remaining = self.cfrag_remaining - amount
                    self.length = self.length - amount
                    
                    # if reached end of fragment, get rid of it, then if one is buffered, move onto next
                    if self.cfrag_remaining == 0:
                        self.frag_buffer.pop(0)
                        if self.length > 0:
                            self.cfrag = <unsigned char*>PyString_AsString(self.frag_buffer[0])
                            self.cfrag_remaining = len(self.frag_buffer[0])
        
                # go back to beginning of packet and extract pid and flags
                
                # if we've not already worked out the PID, get it now and make the final decision on filtering / accepting this packet
                if accepting == -1:
                    pid       = ((cpacket[1-188] << 8) + cpacket[2-188]) & 0x1fff
                    accepting = self.pidfilter[pid]
                    
                if accepting:
                    error     = cpacket[1-188] & 0x80
                    scrambled = cpacket[3-188] & 0xc0
                
                    extracted.append( (pid,error,scrambled,packet) )
                
            else:
                # not yet found start of TS packet, move onto next byte in buffers
                self.cfrag = self.cfrag + 1
                self.cfrag_remaining = self.cfrag_remaining - 1
                self.length = self.length - 1
                
                # if reached end of fragment, get rid of it, then if one is buffered, move onto next
                if self.cfrag_remaining == 0:
                    self.frag_buffer.pop(0)
                    if self.length > 0:
                        self.cfrag = <unsigned char*>PyString_AsString(self.frag_buffer[0])
                        self.cfrag_remaining = len(self.frag_buffer[0])
        
        return extracted

