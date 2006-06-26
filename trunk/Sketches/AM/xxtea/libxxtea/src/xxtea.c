/* xxt encryptor by aliver               */
/* Version 2.0                           */
/*                                       */
/* An implementation of xxtea encryption */
/* A very small (code wise) secure block */
/* cipher. Supposedly faster than btea   */
/* and for files of any non-trival size  */
/* it's gonna be way faster than TEA or  */
/* IDEA. At worst it's something like 4x */
/* the speed of DES, and more secure by  */
/* a factor of 2^72 ~ 4.7 x 10^21        */
/* My tests seemed to indicate that xxt  */
/* is about 3x the speed of mcrypt with  */
/* the same options. Not that mcrypt is  */
/* not a great piece of work. It is.     */
/*                                       */
/* The xxtea algorithm was designed by:  */
/* David Wheeler and Roger Needham. Some */
/* code from their publications was used */
/* for some of the encryption portions.  */
/* However it was altered to be 64 bit   */
/* architecture friendly.                */
/*                                       */
/* Rain Forest Puppy, Zen Parse, Steven  */
/* M. Christey, Hank Leininger, Daniel   */
/* Hartmeier, and anyone I forgot who    */
/* provided me with feedback, bugfixes,  */
/* or pointed out errors in the original */
/* release of xxt                        */
/*****************************************/
/* CHANGE LOG - CHANGE LOG - CHANGE LOG  */
/* Version 2                             */
/* o Tried to mitigate race condition in */
/*   -g by wiping the environment var as */
/*   soon as it's copied.                */
/* o Checked for NULL pointer on -g      */
/* o Added use of O_EXCL for opening the */
/*   output file.                        */
/* o Fixed problem whereby the hash of   */
/*   the key was being reduced to 64bits */
/*   since I was using a char array that */
/*   was being populated with ascii hex  */
/*   values rather than just binary      */
/* o Moved the argv trashing loop up so  */
/*   that it happens before any file I/O */
/* o Fixed an issue whereby someone may  */
/*   create a malicious xxt crypted file */
/*   with a bad filesize header. Now I   */
/*   check for this.                     */
/* o Checked for access to read & write  */
/*   to file in case someone is dumb     */
/*   enough to make this setuid root     */
/* o Added the -f functionality to use a */
/*   whole file as the key. The file is  */
/*   hashed to a 128 bit key.            */
/*****************************************/
/* Compile with cc -O3 -o xxt xxt.c      */
/* "xxt -h" for help, after that         */
/* tested on IRIX, Solaris, Linux        */
/* NetBSD, and AIX                       */

/*****************************************/
/* CHANGE LOG - CHANGE LOG - CHANGE LOG  */
/* Anagha Mudigonda version 3*/
/* I used most alivers logic as is but I */
/* removed main and a lot of functions I */
/* do not need for kamaelia. Also I use  */
/* my own keygen function so I removed   */
/* the MD5 related code                  */
/*****************************************/
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
#include "xxtea.h"

static long btea( int32_t * v, int32_t n , int32_t * k );

int xxtea_encrypt(char* in_file, char* out_file, char* key) {
    extern int errno;
    int c;
    int i;
    int j;
    int sl;
    int first_block = 1;
    int fd_in;
    int fd_out;
    int bl = 0;
    int bytes_read;
    int pad = 0;
    int trnd = 0;
    int uid;
    int use_file = 0;
    uint32_t randpad[16];
    uint32_t filesize = 0;
    uint32_t filesize_msb = 0;
    uint32_t read_filesize_msb = 0;
    uint32_t read_filesize = 0;
    uint32_t bsf = 0;
    char fb_buffer[64];
    /* u_char *plaintext = NULL; */
    u_char plaintext[64];
    struct stat statbuf;

    /* They must give us an input file, and it must */
    /* be statable and readable by us or we fail    */
    if(in_file != NULL) {
        if(-1 == (stat(in_file,&statbuf))) {
            return IN_FILE_ERROR;
        }
        else {
            (off_t) filesize = statbuf.st_size;
            filesize_msb = htonl(filesize);
        }
        if(-1 == access(in_file,R_OK)) {
           /* fprintf(stderr,"FATAL: access denied while trying to read %s: %s\n"
                    ,in_file
                    ,strerror(errno));
            */
	    return NO_READ_PERMS;
        }
        if(-1 == (fd_in = open(in_file,O_RDONLY))) {
            //fprintf(stderr,"FATAL: Cannot open() the file.\n\t%s\n",strerror(errno));
            return IN_FILE_ERROR;
        }
    } else {
        //fprintf(stderr,"FATAL: no input file!\n");
        return IN_FILE_ERROR;
    }

        if(-1 == (fd_out = open(out_file,O_WRONLY|O_CREAT|O_EXCL,00600))) {
           /* fprintf(stderr,"FATAL: cannot open the output file %s for writing.\n\t%s\n"
                    ,out_file
                    ,strerror(errno));*/
         return OUT_FILE_ERROR;
        }
   

    /* create some random bytes that we may want to */
    /* use later on for padding, depending on the   */
    /* length of the input it may or may not get    */
    /* used. The maximum we may need for padding is */
    /* going to be 64 bytes. (the block size)       */
    for(i = 0; i < 16; i++) {
        srand(i);
        trnd = rand();
        srand((int)time(0) + getpid() + i + trnd);
        randpad[i] = rand();
    }

        while(first_block) {
            bytes_read = read(fd_in,plaintext,60);
            if(bytes_read == -1) {
                //printf("FATAL:  Problem reading input file.\n\t%s\n",strerror(errno));
                return READ_ERROR;
            }
            /* if the initial input isn't at least 60 bytes */
            /* we are going to have to pad it. */
            if(bytes_read != 60) {
                pad = 60 - bytes_read ;
                memcpy(plaintext+bytes_read,randpad,pad);
            }
            memcpy(fb_buffer, &filesize_msb, 4);
            memcpy(fb_buffer+4, plaintext, 60);
            btea((int32_t *) fb_buffer, 16, (int32_t *) key);
            write(fd_out,(char *) fb_buffer,64);
            first_block = 0;
        }
        while( (bytes_read = read(fd_in,plaintext,64)) ) {
            if(bytes_read == 64) {
                btea((int32_t *) plaintext, 16, (int32_t *) key);
                write(fd_out,(char *) plaintext,64);
            } else {
                pad = 64 - bytes_read;
                memcpy(plaintext+bytes_read,randpad,pad);
                btea((int32_t *) plaintext, 16, (int32_t *) key);
                write(fd_out,(char *) plaintext,64);
            }
        }
      

    /*  delete the infile */
    //unlink(in_file);

    close(fd_out);
    close(fd_in);
    return(XXTEA_SUCCESS);
}

int xxtea_decrypt(char* in_file, char* out_file, char* key) {
    extern int errno;
    int c;
    int i;
    int j;
    int sl;
    int first_block = 1;
    int fd_in;
    int fd_out;
    int bl = 0;
    int bytes_read;
    int pad = 0;
    int trnd = 0;
    int uid;
    int use_file = 0;
    uint32_t randpad[16];
    uint32_t filesize = 0;
    uint32_t filesize_msb = 0;
    uint32_t read_filesize_msb = 0;
    uint32_t read_filesize = 0;
    uint32_t bsf = 0;
    char fb_buffer[64];
    /* u_char *plaintext = NULL; */
    u_char plaintext[64];
    struct stat statbuf;

    /* They must give us an input file, and it must */
    /* be statable and readable by us or we fail    */
    if(in_file != NULL) {
        if(-1 == (stat(in_file,&statbuf))) {
            //fprintf(stderr,"FATAL: cannot stat the input file!\n");
            return IN_FILE_ERROR;
        }
        else {
            (off_t) filesize = statbuf.st_size;
            filesize_msb = htonl(filesize);
        }
        if(-1 == access(in_file,R_OK)) {
            /*fprintf(stderr,"FATAL: access denied while trying to read %s: %s\n"
                    ,in_file
                    ,strerror(errno));
            */
           return READ_ERROR;
        }
        if(-1 == (fd_in = open(in_file,O_RDONLY))) {
            //fprintf(stderr,"FATAL: Cannot open() the file.\n\t%s\n",strerror(errno));
            return READ_ERROR;
        }
    } else {
        //fprintf(stderr,"FATAL: no input file!\n");
        return IN_FILE_ERROR;
    }

    
        if(-1 == (fd_out = open(out_file,O_WRONLY|O_CREAT|O_EXCL,00600))) {
            /*fprintf(stderr,"FATAL: cannot open the output file %s for writing.\n\t%s\n"
                    ,out_file
                    ,strerror(errno));
            */
	    return OUT_FILE_ERROR;
        }
   

    /* create some random bytes that we may want to */
    /* use later on for padding, depending on the   */
    /* length of the input it may or may not get    */
    /* used. The maximum we may need for padding is */
    /* going to be 64 bytes. (the block size)       */
    for(i = 0; i < 16; i++) {
        srand(i);
        trnd = rand();
        srand((int)time(0) + getpid() + i + trnd);
        randpad[i] = rand();
    }

    
        while(first_block) {
            read(fd_in,plaintext,64);
            btea((int32_t *) plaintext, -16, (int32_t *) key);
            memcpy(&read_filesize_msb,plaintext,4);
            read_filesize = ntohl(read_filesize_msb);
            /* now that we know the filesize. Let's calculate if the */
            /* in file actually matches it. This is an attempt to    */
            /* avoid someone making an "evil" xxt and creating files */
            /* to crash someone elses "good" version and/or create   */
            /* monster files.                                        */
            pad = (64 - (read_filesize) % 64);
            if(pad < 4) {
                pad += 64;
                i = read_filesize ;
            } else {
                i = read_filesize;
            }
            if(filesize != (i + pad)) {
                //fprintf(stderr,"FATAL: the file size in the header is mismatched with the actual size.\n");
                return FILE_SIZE_ERROR;
            }
            if(read_filesize >= 60) {
                write(fd_out,(char *) plaintext+4,60);
            } else {
                write(fd_out,(char *) plaintext+4,read_filesize);
            }
            bsf += 64;
            first_block = 0;
        }
        while(0 != (bytes_read = read(fd_in,plaintext,64)) ) {
            btea((int32_t *) plaintext, -16, (int32_t *) key);
            bsf += 64;
            if(bsf < (read_filesize + 4) && read_filesize > 64) {
                write(fd_out,(char *) plaintext,64);
            } else {
                bl = 64 - (bsf - (read_filesize + 4)); /* calc how much is really left */
                write(fd_out,(char *) plaintext,bl);
            }
        }
    

    /*  delete the infile */
    //unlink(in_file);

    close(fd_out);
    close(fd_in);
    return(XXTEA_SUCCESS);
}
/*
int main (int argc, char *argv[]) {
	printf("encrypting \n");
	encrypt("test","test.enc","12345678901234567890123456789012");
	printf("encrypted \n");
	printf("decrypting \n");
	decrypt("test.enc","test.dec","12345678901234567890123456789012");
	printf("decrypted \n");
}
*/
/* nearly all the following xxtea crypto */
/* code from the post script             */
/* by David Wheeler and Roger Needham    */
/* I've altered it to be more portable   */
/* on 64 bit platforms by making use of  */
/* definitions in stdint.h               */
static long btea( int32_t * v, int32_t n , int32_t * k ) {
    uint32_t z=v[n-1], y=v[0], sum=0,e,
                                   DELTA=0x9e3779b9 ;
    int32_t p, q ;
    if ( n>1) {
        /* Coding Part */
        q = 6+52/n ;
        while ( q-- > 0 ) {
            sum += DELTA ;
            e = sum >> 2&3 ;
            for ( p = 0 ; p < n-1 ; p++ )
                y = v[p+1],
                    z = v[p] += MX
                                y = v[0] ;
            z = v[n-1] += MX
                      }
                      return 0 ;
    }
    /* Decoding Part */
    else if ( n <-1 ) {
        n = -n ;
        q = 6+52/n ;
        sum = q*DELTA ;
        while (sum != 0) {
            e = sum>>2 & 3 ;
            for (p = n-1 ; p > 0 ; p-- )
                z = v[p-1],
                    y = v[p] -= MX
                                z = v[n-1] ;
            y = v[0] -= MX
                        sum -= DELTA ;
        }
        return 0 ;
    }
    return 1 ;
} /* Signal n=0,1,-1 */

