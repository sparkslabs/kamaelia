/*
 * Simple Ogg Vorbis decoder, (c) 2004 BBC Michael Sparks
 *
 * Based in part on the original sample ogg vorbis decoder - structure is
 * designed for reuse.
 *
 * Incorporates code (c) 1994-2004 XIPHOPHORUS Company http://www.xiph.org/
 *
 * Important limitations include:
 *   * Has a minimum buffer size of 58 bytes (important detail)
 *   * Does not handle chained bitstreams.
 *     (Multiple vorbis streams concatenated in a file)
 *   * Uses EOF to indicate end of stream
 *
 * Seems to decode most ogg vorbis file pretty well though
 *
 */

/* #include "libvorbissimple.c" */

#include "vorbissimple.h"

#include <stdio.h>

int main(int argc, char *argv[]) {
   bool decoding = TRUE;
   ogg_vorbis_context * oggVorbisContext;
   source_buffer * sourceBuffer;
   decode_buffer * decodeBuffer;

   oggVorbisContext = newOggVorbisContext();
   sourceBuffer = newSourceBuffer(stdin,BUFSIZE);
   while(decoding) {
      decodeBuffer = getAudio(oggVorbisContext);
      switch (decodeBuffer->status) {
         case NEEDDATA:
            readData(sourceBuffer);
            if (sourceBuffer->bytes > 0)
               sendBytesForDecode(oggVorbisContext, sourceBuffer);
            else
               decoding = FALSE;
            break;
         case HAVEDATA:
            /* We have to use the contents of the decodeBuffer befor asking
              for more bytes, or else we lose the contents, this could mean just
              buffering */
            fwrite(decodeBuffer->buffer,sizeof(char),decodeBuffer->len,stdout);
            break;
         case NORMAL:
            /* Just so that we can signify normal status */
            break;
         default: /* Unknown status, exit */
            decoding = FALSE;
            break;
      }
      free(decodeBuffer);
   }
   free(sourceBuffer);
   free(oggVorbisContext);
   return 0;
}
