#include <sys/time.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "keygen.h"

/*
random key where the key will be stored.
key_len : length of the key
*/
void get_key(char *random_key, unsigned key_len) {
    char tmp[11]; // max of 10 digits ( i am assuming rand returns a 32 bit number)
    unsigned key_cnt = 0;
    int i = 0;
	int tmp_len = 0;
    struct timeval tp;

    gettimeofday(&tp, NULL);
	srand((unsigned int)tp.tv_usec);

	while(key_cnt < key_len) {
        memset(tmp, 0, sizeof(tmp));
        sprintf(tmp, "%x", rand());
        tmp_len = strlen(tmp);
        for(i=0; ((i < tmp_len) && (key_cnt < key_len)); i++, key_cnt++) {
            random_key[key_cnt] = tmp[i];
         }
       }
       random_key[key_cnt] = 0;
}

/*int main() {
	char random_key[10];
	get_key(random_key,9);
	printf("%s",random_key);
}*/
//Usage: 
//initialize of random function with seed
//char random_key[33]; 
//get_key(random_key);
//
//
//
//
