#include "aesint.c"
void get_key(char *random_key);
int main() {
	  char random_key[33];
	   get_key(random_key);
	   encrypt_aes("testenc.orig","testenc.enc",random_key);
	   printf("ENNNNCCCCRYPTED \n");
	   decrypt_aes("testenc.enc","testenc.dec",random_key);
	   printf("DDDDDDEEEECCRPPPPPPTTTEED \n");
}
			
