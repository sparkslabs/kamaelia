#
# Simple pyrex access wrapper for libxxtea
#
cdef extern from "xxtea.h":
  int xxtea_decrypt(char* in_file, char* out_file, char* key)
  int xxtea_encrypt(char* in_file, char* out_file, char* key)
  long btea_8bytes( unsigned char* v, int n , unsigned char* k )
  
  cdef enum defines:
     XXTEA_SUCCESS = 0
     IN_FILE_ERROR = 1
     NO_READ_PERMS = 2
     NO_WRITE_PERMS = 3
     OUT_FILE_ERROR = 4
     READ_ERROR = 5
     FILE_SIZE_ERROR = 6
cdef extern from "Python.h":
   object PyString_FromStringAndSize(char*,int)
   
cdef extern from "keygen.h":
  void get_key(char* random_key, unsigned key_len)

def generate_key(char* random_key, int key_len):
   get_key(random_key, key_len)

def enc_xxtea(char* infile, char* outfile, char* key):
   ret = xxtea_encrypt(infile, outfile, key)
   return ret

def dec_xxtea(char* infile, char* outfile, char* key):
   ret = xxtea_decrypt(infile, outfile, key)
   return ret
# This might be the only function useful to kamaelia.
# 8 bytes of a passed parameter are processed. The rest are just ignored.

def xxbtea(data, int no , key):
    cdef  char* Cdata
    cdef char* Ckey
    Cdata = data
    Ckey = key
    btea_8bytes(Cdata, no,Ckey)
    return PyString_FromStringAndSize(Cdata,8)
