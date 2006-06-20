cdef extern from "aesint.h":
  int decrypt_aes(char* infile, char* outfile, char* deckey)
  int encrypt_aes(char* infile, char* outfile, char* enckey)
  int aes_dec( char *infile, char* outfile, char*deckey)
  int aes_enc(char* infile, char* outfile, char* enckey)

cdef extern from "keygen.h":
  void get_key(char* random_key, int keylen)

def enc_aes(Pinfile, Poutfile, Penckey):
  cdef char* infile
  cdef char* outfile
  cdef char* enckey
  infile = Pinfile
  outfile = Poutfile
  enckey = Penckey
  ret = encrypt_aes(infile, outfile, enckey)
  return ret
	
def dec_aes(Pinfile, Poutfile, Pdeckey):
  cdef char* infile
  cdef char* outfile
  cdef char* deckey
  infile = Pinfile
  outfile = Poutfile
  deckey = Pdeckey
  ret = decrypt_aes(infile, outfile, deckey)
  return ret

def generate_key(Prandom_key, int Pkeylen):
  cdef char*random_key
  cdef int keylen
  random_key = Prandom_key
  keylen = Pkeylen
  get_key(random_key, keylen)

