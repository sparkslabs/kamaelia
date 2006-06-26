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

#endif
