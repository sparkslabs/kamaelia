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
# include "xxtea.h"
int main(int argc, char* argv) {
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
