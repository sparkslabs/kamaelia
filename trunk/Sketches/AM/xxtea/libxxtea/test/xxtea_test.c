/*
 Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)

 (1) Kamaelia Contributors are listed in the AUTHORS file and at
     http://www.kamaelia.org/AUTHORS - please extend this file,
     not this notice.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
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
#include <pthread.h>

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
void enc_entire_file_thr(void* arg) {
    int ret;
    // note that the caller is responsible for allocating memory for the key
    char key[32];
    char dest_file[32];
    char dec_file[32];

    get_key(key,32);
    // now you have the key. use it to encrypt the file.
    // in this example i'll encrypt this source file.
     strcpy(dest_file,"xxtea_test.enc");
     strcat(dest_file,(char*)arg);
     ret = xxtea_encrypt("xxtea_test.c",dest_file,key);
    if(ret == 0)
    	printf("Encrypted to %s \n",dest_file);
    else
       printf("Encryption failed. Status %d \n", ret);
    printf("Decrypting file %s \n",dest_file);

    strcpy(dec_file,"xxtea_testdec");
    strcat(dec_file,(char*)arg);
    printf("dec file name %s",dec_file);

    ret = xxtea_decrypt(dest_file,dec_file,key);
    if(ret == 0) {
    } else
       printf("Decryption failed. Status %d \n", ret);
}
void enc_char_string(void* args) {
       char txt[6];
       char *key = "12345678901234567890123456789012";
       for(;;) {
       strcpy(txt,"hello");
       btea_8bytes(txt, 2, key);
       //printf("cipher text : [%s] \n",txt);
       btea_8bytes(txt, -2, key);
       printf("thread id %s",(char*) args);
       printf("decipher text : [%s] \n",txt);
  }
}

int main() {
   pthread_t t1;
   pthread_t t2;
    if ( pthread_create(&t1, NULL, enc_entire_file_thr, (void *)"1") != 0 ) {
    printf("pthread_create() error \n");
    abort();
   }
 
    if ( pthread_create(&t2, NULL, enc_entire_file_thr, (void *)"2") != 0 ) {
    printf("pthread_create() error \n");
    abort();
   } 
   
   while (1)
      sleep(100);

   
   //enc_entire_file();
   //printf("**************************************ECNRYPTED ENTIRE FILE \n");
   //enc_char_string();
   //printf("**************************************ECNRYPTED STRING \n");
}  
