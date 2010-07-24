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
#ifndef XXTEA_H
#define XXTEA_H

#define XXTEA_SUCCESS 0
#define IN_FILE_ERROR 1
#define NO_READ_PERMS 2
#define NO_WRITE_PERMS 3
#define OUT_FILE_ERROR 4
#define READ_ERROR 5
#define FILE_SIZE_ERROR 6
#define MX (z>>5^y<<2)+(y>>3^z<<4)^(sum^y)+(k[p&3^e]^z);

extern int xxtea_decrypt(char* in_file, char* out_file, char* key);
extern int xxtea_encrypt(char* in_file, char* out_file, char* key);
//long btea_8bytes(unsigned char* data, int rounds, unsigned char* key);
long btea_8bytes(char* data, int rounds, char* key);
#endif
