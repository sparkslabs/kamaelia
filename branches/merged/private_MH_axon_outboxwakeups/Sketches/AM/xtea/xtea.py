""" 
XTEA Block Encryption Algorithm

Author: Paul Chakravarti (paul_dot_chakravarti_at_mac_dot_com)
License: Public Domain

This module provides a Python implementation of the XTEA block encryption
algorithm (http://www.cix.co.uk/~klockstone/xtea.pdf). 

The module implements the basic XTEA block encryption algortithm
(`xtea_encrypt`/`xtea_decrypt`) and also provides a higher level `crypt`
function which symmetrically encrypts/decrypts a variable length string using
XTEA in OFB mode as a key generator. The `crypt` function does not use
`xtea_decrypt` which is provided for completeness only (but can be used
to support other stream modes - eg CBC/CFB).

This module is intended to provide a simple 'privacy-grade' Python encryption
algorithm with no external dependencies. The implementation is relatively slow
and is best suited to small volumes of data. Note that the XTEA algorithm has
not been subjected to extensive analysis (though is believed to be relatively
secure - see http://en.wikipedia.org/wiki/XTEA). For applications requiring
'real' security please use a known and well tested algorithm/implementation.

The security of the algorithm is entirely based on quality (entropy) and
secrecy of the key. You should generate the key from a known random source and
exchange using a trusted mechanism. In addition, you should always use a random
IV to seed the key generator (the IV is not sensitive and does not need to be
exchanged securely)


"""

import struct


def xtea_encrypt(key,block,n=32):
    """
        Encrypt 64 bit data block using XTEA block cypher
        * key = 128 bit (16 char) / block = 64 bit (8 char)

        >>> xtea_encrypt('0123456789012345','ABCDEFGH').encode('hex')
        'b67c01662ff6964a'
    """
    v0,v1 = struct.unpack("!2L",block)
    k = struct.unpack("!4L",key)
    sum,delta,mask = 0L,0x9e3779b9L,0xffffffffL
    for round in range(n):
        v0 = (v0 + (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
        sum = (sum + delta) & mask
        v1 = (v1 + (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
    return struct.pack("!2L",v0,v1)

def xtea_decrypt(key,block,n=32):
    """
        Decrypt 64 bit data block using XTEA block cypher
        * key = 128 bit (16 char) / block = 64 bit (8 char)

        >>> xtea_decrypt('0123456789012345','b67c01662ff6964a'.decode('hex'))
        'ABCDEFGH'
    """
    v0,v1 = struct.unpack("!2L",block)
    k = struct.unpack("!4L",key)
    delta,mask = 0x9e3779b9L,0xffffffffL
    sum = (delta * n) & mask
    for round in range(n):
        v1 = (v1 - (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
        sum = (sum - delta) & mask
        v0 = (v0 - (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
    return struct.pack("!2L",v0,v1)

def xtea_encrypt_arbit(key,block):
   #breakup the block into 8 byte
   times = len(block)/8
   index = 0
   start = 0
   enc_list = []
   
   while times != 0:
      slice = block[index:index+8]
      #print "slice is",slice
      index = index+8
      times = times - 1
      enc_list.append(xtea_encrypt(key,slice))

   return ''.join(enc_list)

def xtea_decrypt_arbit(key,block):
   #breakup the block into 8 byte
   times = len(block)/8
   index = 0
   start = 0
   enc_list = []
   
   while times != 0:
      slice = block[index:index+8]
      #print "slice is",slice
      index = index+8
      times = times - 1
      enc_list.append(xtea_decrypt(key,slice))

   return ''.join(enc_list)
"""
cipher = xtea_encrypt_arbit('1234567890123456','12345678ABCDEFGH')
print cipher
plain = xtea_decrypt_arbit('1234567890123456',cipher)
print plain

"""
