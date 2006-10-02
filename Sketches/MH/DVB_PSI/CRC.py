#!/usr/bin/env python

# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""\
CRC algorithm used to verify the integrity of data in DVB transport streams.
"""

# # old slow CRC algorithm. 
# # ought to recode a faster algorithm sometime soon
# 
# def crc32(data):
#     poly = 0x4c11db7
#     crc = 0xffffffff
#     for byte in data:
#         byte = ord(byte)
#         for bit in range(7,-1,-1):  # MSB to LSB
#             z32 = crc>>31    # top bit
#             crc = crc << 1
#             if ((byte>>bit)&1) ^ z32:
#                 crc = crc ^ poly
#             crc = crc & 0xffffffff
#     return crc
# 
# def dvbcrc(data):
#     return not crc32(data)

def __MakeCRC32(polynomial = 0x4c11db7,initial=0xffffffff):
    """\
    MakeCRC32([polynomial][,inital]) -> (string -> 32bit CRC of binary string data)
    
    Returns a function that calculatees the 32 bit CRC of binary data in a
    string, using the specified CRC polynomial and initial value.
    """
    
    # precalculate the effect on the CRC of processing a byte of data
    # create a table of values to xor by, indexed by
    # new_byte_of_data xor most-sig-byte of current CRC
    xorvals = []
    for x in range(0,256):   # x is the result of top byte of crc xored with new data byte
        crc = x<<24
        for bit in range(7,-1,-1):  # MSB to LSB
            z32 = crc>>31    # top bit
            crc = crc << 1
            if z32:
                crc = crc ^ polynomial
            crc = crc & 0xffffffff
        xorvals.append(crc & 0xffffffff)   # only interested in bottom 24 bits
    
    # define the function that will do the crc, using the table we've just
    # precalculated.
    def fastcrc32(data):
        crc = 0xffffffff
        for byte in data:
            byte = ord(byte)
            xv = xorvals[byte ^ (crc>>24)]
            crc = xv ^ ((crc & 0xffffff)<<8)
        return crc

    return fastcrc32

__dvbcrc = __MakeCRC32(polynomial = 0x04c11db7)

dvbcrc = lambda data : not __dvbcrc(data)


