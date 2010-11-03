
cdef char DVB_RESYNC = "\x47"
cdef int DVB_PACKET_SIZE = 188

def packetise(buffer):
    packets = []
    cdef char first
    cdef char * buff
    cdef int i = 0
    while i < len(buffer):
        buff = <char*>buffer      # Access the buffer as a char * type
        first = buff[0]           # Pick out the first character
        if first != DVB_RESYNC:   # Compare with DVB_RESYNC packet
            break                 # If it isn't, it's duff, so throw it away

        packet = buffer[i:i+DVB_PACKET_SIZE]   # Otherwise, grab the first DVB_PACKET_SIZE bytes into a packet
        i += DVB_PACKET_SIZE                   # Increment our index beyond the packet
        packets.append( packet )               # Append the packet to the packets

    return packets                             # Return packets
