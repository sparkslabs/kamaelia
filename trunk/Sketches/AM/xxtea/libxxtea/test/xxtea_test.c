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
// compile with gcc -c 
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <inttypes.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <netinet/in.h>
# include "xxtea.h"
void enc_entire_file() {
    int ret;
    // note that the caller is responsible for allocating memory for the key
    char key[32];

    get_key(key,32);
    // now you have the key. use it to encrypt the file.
    // in this example i'll encrypt this source file.
    printf("Encrypting file xxtea_test.c \n");
    ret = xxtea_encrypt("xxtea_test.c","xxtea_test.enc",key);
    if(ret == 0)
    	printf("Encrypted to xxtea_test.enc \n");
    else
       printf("Encryption failed. Status %d \n", ret);

    printf("Decrypting file xxtea_test.dec \n");
    ret = xxtea_decrypt("xxtea_test.enc","xxtea_test.dec",key);
    if(ret == 0) {
       printf("Decrypted to  xxtea_test.dec \n");
       printf("xxtea_test.c and xxtea_test.dec should be the same \n");
    } else
       printf("Decryption failed. Status %d \n", ret);
 }

void enc_char_string() {
       char txt[6];
       char *key = "12345678901234567890123456789012";
       strcpy(txt,"hello");
       btea_8bytes(txt, 2, key);
       printf("cipher text : [%s] \n",txt);
       btea_8bytes(txt, -2, key);
       printf("decipher text : [%s] \n",txt);
  
}

int main() {
   enc_entire_file();
   printf("**************************************ECNRYPTED ENTIRE FILE \n");
   enc_char_string();
   printf("**************************************ECNRYPTED STRING \n");
}  
