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

