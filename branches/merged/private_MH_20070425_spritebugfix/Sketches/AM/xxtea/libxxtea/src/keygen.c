/* 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
     All Rights Reserved.

 You may only modify and redistribute this under the terms of any of the
 following licenses(2): Mozilla Public License, V1.1, GNU General
 Public License, V2.0, GNU Lesser General Public License, V2.1

 (1) Kamaelia Contributors are listed in the AUTHORS file and at
     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
     not this notice.
 (2) Reproduced in the COPYING file, and at:
     http://kamaelia.sourceforge.net/COPYING
 Under section 3.5 of the MPL, we are using this text since we deem the MPL
 notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
 notice is prohibited.
#
 Please contact us via: kamaelia-list-owner@lists.sourceforge.net
 to discuss alternative licensing.
 -------------------------------------------------------------------------
*/
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
/*
int main() {
	char random_key[10];
	get_key(random_key,9);
	printf("%s",random_key);
}*/
