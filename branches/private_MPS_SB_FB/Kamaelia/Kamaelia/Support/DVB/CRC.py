#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""\
CRC algorithm used to verify the integrity of data in DVB transport streams.
"""

# # old slow CRC algorithm. 
# # ought to recode a faster algorithm sometime soon
# 
# def crc32(data):
#     poly = 0x4c11db7
#     crc = 0xffffffffL
#     for byte in data:
#         byte = ord(byte)
#         for bit in range(7,-1,-1):  # MSB to LSB
#             z32 = crc>>31    # top bit
#             crc = crc << 1
#             if ((byte>>bit)&1) ^ z32:
#                 crc = crc ^ poly
#             crc = crc & 0xffffffffL
#     return crc
# 
# def dvbcrc(data):
#     return not crc32(data)

def __MakeCRC32(polynomial = 0x4c11db7L,initial=0xffffffffL):
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
        crc = long(x)<<24
        for bit in range(7,-1,-1):  # MSB to LSB
            z32 = crc>>31    # top bit
            crc = crc << 1
            if z32:
                crc = crc ^ polynomial
            crc = crc & 0xffffffffL
        xorvals.append(crc & 0xffffffffL)   # only interested in bottom 24 bits
    
    # define the function that will do the crc, using the table we've just
    # precalculated.
    def fastcrc32(data):
        crc = 0xffffffffL
        for byte in data:
            byte = ord(byte)
            xv = xorvals[byte ^ (crc>>24)]
            crc = xv ^ ((crc & 0xffffffL)<<8)
        return crc

    return fastcrc32

__dvbcrc = __MakeCRC32(polynomial = 0x04c11db7L)

dvbcrc = lambda data : not __dvbcrc(data)


