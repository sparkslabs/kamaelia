#!/usr/bin/python

import time
import dvbpacket

DVB_RESYNC = "\x47"  
DVB_PACKET_SIZE = 188

def packetise(buffer):
    packets = []

    while len(buffer)>0:
        i = buffer.find(DVB_RESYNC)
        if i == -1: # if not found

            print "we have a dud"
            buffer = ""
            continue

        if i>0:
            buffer = buffer[i:]
            continue

        # packet is the first 188 bytes in the buffer now
        packet, buffer = buffer[:DVB_PACKET_SIZE], buffer[DVB_PACKET_SIZE:]
        packets.append( packet )

    return packets



def packetise2(buffer):
    packets = []
    i = 0
    while i < len(buffer):
        if buffer[i] != DVB_RESYNC:
            break

        packet = buffer[i:i+DVB_PACKET_SIZE]
        i += DVB_PACKET_SIZE
        packets.append( packet )

    return packets

packet = DVB_RESYNC + "."*187
for i in [10,100,1000,2000,3000,4000,5000,10000,100000]:
    print i, "packets"
    print
    packets_raw = i*packet

    A = time.time()
    for _ in xrange(1000):
        packets = dvbpacket.packetise(packets_raw)
    B = time.time()

    if len(packets) == i:
        print "    ","PACKETS VERIFIED"
    cython = B - A

    if 1:
        C = time.time()
        for _ in xrange(1000):
            packets = packetise(packets_raw)
        D = time.time()

        if len(packets) == i:
            print "    ","PACKETS VERIFIED"
        python = D - C

    if 0:
        E = time.time()
        for i in xrange(1000):
            packets = packetise2(packets_raw)
        F = time.time()

        python2 = F - E

    print "    ", cython
    print "    ", python
#    print "    ", python2
    print
    #print python - cython 
    #print python2 - cython 

    print "    ", "cython is", python / cython,  " times faster than python"
#    print "    ", "cython is", python2 / cython, " times faster than python2"
#    print "    ", "python2 is", python/python2, " times faster than python"
