# include "aesint.h"

int encrypt_aes(char* infile, char* outfile, char* enckey) {
	return aes_enc(infile, outfile, enckey);
}
int decrypt_aes(char* infile, char* outfile, char* deckey) {
	return aes_dec(infile, outfile, deckey);
}
