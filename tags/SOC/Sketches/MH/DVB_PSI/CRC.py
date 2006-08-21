#!/usr/bin/env python

# old slow CRC algorithm. 
# must reconstruct my new fast algorithm sometime soon


def crc32(data):
    poly = 0x4c11db7
    crc = 0xffffffff
    for byte in data:
        byte = ord(byte)
        for bit in range(7,-1,-1):  # MSB to LSB
            z32 = crc>>31    # top bit
            crc = crc << 1
            if ((byte>>bit)&1) ^ z32:
                crc = crc ^ poly
            crc = crc & 0xffffffff
    return crc

def dvbcrc(data):
    return not crc32(data)

