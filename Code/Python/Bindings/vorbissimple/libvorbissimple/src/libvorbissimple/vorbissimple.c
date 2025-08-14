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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ogg/ogg.h>
#include <vorbis/codec.h>
#include <assert.h>

#include "vorbissimple.h"

/****************************************************************************
 * Code for handling ogg vorbis contexts
 */

ogg_vorbis_context * newOggVorbisContext(void) {
   ogg_vorbis_context * result;
   result = (ogg_vorbis_context *)malloc(sizeof(ogg_vorbis_context));
   if (!result) { return NULL; }

   memset(result, 0, sizeof *result);    // Zero the memory

   ogg_sync_init(&(result->oggSync)); /* Now we can read pages */
   result->decodeState = STARTSTATE;
   result->headerPacketsRead = 0;
   result->streamInitialised = 0;
   result->convsize = 0;
   result->buffer = NULL;
   result->bufferlen = 0;
   result->warnClipping = FALSE;
   /* result->oggBitstreamPage; */ /* No initialisation, but memset to zero above */
   return result;
}

/*************************************************************************
 * Code for dealing with source buffer data
 */

source_buffer * newSourceBuffer(FILE * fh, int buffersize) {
   source_buffer * result;
   result = (source_buffer *)malloc(sizeof(source_buffer));
   if (result) {
      result->fh = fh;
      result->_bytes = 0;
      if (buffersize) {
         result->buffer = (char *)malloc(sizeof(char)*buffersize);
      } else {
         result->buffer = NULL;
      }
      result->buffersize = buffersize;
      return result;
   }
   return NULL;
}

/****************************************************************************
 * Code for handling decode buffer results
 */

decode_buffer * newDecodeBuffer(int status) {
   /* Note, the decode buffer does not own any data of it's own, and hence
      does not allocate or free any data. This is a container to reference
      the library's buffer */
   decode_buffer * buffer;
   buffer = (decode_buffer *)malloc(sizeof(decode_buffer));
   if (!buffer) { return NULL; }

   buffer->buffer = NULL;
   buffer->len = 0;
   buffer->status = status;

   return buffer;

}

void sendBytesForDecode(ogg_vorbis_context * ovc, source_buffer *sourceBuffer){
   char * buffer;
   assert(sourceBuffer->_bytes >= 0 && sourceBuffer->_bytes <= sourceBuffer->buffersize);
   
   buffer = ogg_sync_buffer( &(ovc->oggSync), sourceBuffer->_bytes); // Get a buffer for the bytes we're sending

   memcpy(buffer,sourceBuffer->buffer, (size_t)sourceBuffer->_bytes);
   ogg_sync_wrote(&(ovc->oggSync),sourceBuffer->_bytes);
}

int checkStreamOggVorbis(ogg_vorbis_context * ovc) {
    int result;
    vorbis_info_init(&(ovc->vorbisInfo));
    vorbis_comment_init(&(ovc->vorbisComment));
    result = readPacket(ovc);
    if (result <1) return result;

    result=vorbis_synthesis_headerin(&(ovc->vorbisInfo),&(ovc->vorbisComment),&(ovc->oggPacket));

    if (result<0){
      return NOTOGGVORBIS;
    }
    return 1; /* SUCCESS */
}

int readPage(ogg_vorbis_context * oggVorbisContext){
   int result;
   result=ogg_sync_pageout(&(oggVorbisContext->oggSync),&(oggVorbisContext->oggBitstreamPage));
   if (result==0) {
      return NEEDDATA; }
   if (result <0) return CORRUPTPAGE;
   if (! oggVorbisContext->streamInitialised) {
      ogg_stream_init(&(oggVorbisContext->oggStream),ogg_page_serialno(&(oggVorbisContext->oggBitstreamPage)));
      oggVorbisContext->streamInitialised = TRUE;
   }
   return PAGEREAD;
}

/* Return values:
      PACKETREAD : Packet Read  (1)
      NEEDDATA Need Data (via readPage)  (-1)
      CORRUPTPAGE : Corrupt Page, need data  (-10)
      CORRUPTPACKET : Corrupt Packet, need data (-11)
*/
int readPacket(ogg_vorbis_context * ovc){
   int packetResult, pageResult;
   int packetRead = FALSE;

   assert(ovc != NULL);

   /* Ensure the logical stream is initialised at least once */
   if (!ovc->streamInitialised) {
       pageResult = readPage(ovc);
       if (pageResult <= 0)   /* NEEDDATA or error */
           return pageResult;
       /* readPage() initialises the stream when it sees the first page */
       ogg_stream_pagein(&ovc->oggStream, &ovc->oggBitstreamPage);
   }

   packetResult = ogg_stream_packetout(&ovc->oggStream, &ovc->oggPacket);
   if (packetResult < 0) return CORRUPTPACKET;
   if (packetResult > 0) return PACKETREAD;


   /* Keep pulling pages until we get a packet or need more data */
   for (;;) {
       pageResult = readPage(ovc);
       if (pageResult <= 0) {   /* NEEDDATA or error */
           return pageResult;
       }

      /* We don't check the result of stuffing things in the buffer - getting stuff out will fail if this fails */
       ogg_stream_pagein(&ovc->oggStream, &ovc->oggBitstreamPage);

       packetResult = ogg_stream_packetout(&ovc->oggStream, &ovc->oggPacket);
       if (packetResult < 0) return CORRUPTPACKET;
       if (packetResult > 0) return PACKETREAD;
   }
}

/* This function forms a state machine who's purpose in life is very simple:
   Read 2 vorbis packets, and pass them onto the vorbis subsystem.

   In can be put on pause due to a need for more data/etc. Let's write it
   that way then, and store the state in the ov context.
   Our success case is >0
 */
int readCommentAndCodebookHeaders(ogg_vorbis_context * ovc) {
   int result;
   if (ovc->headerPacketsRead >= 2) return FAILSTATE;
   // FIXME: This means we need to reset this on each new bitstream
   while (ovc->headerPacketsRead<2) {
      result = readPacket(ovc);
      if (result <0) return result; // Pass back errors
      // Otherwise we have a packet usable in oggVorbisContext->oggPacket
      vorbis_synthesis_headerin(&(ovc->vorbisInfo),&(ovc->vorbisComment),&(ovc->oggPacket));
      ovc->headerPacketsRead += 1;
   }

   ovc->convsize=BUFSIZE / ( ovc->vorbisInfo.channels ? ovc->vorbisInfo.channels : 1 );

    /* OK, got and parsed all three headers. Initialize the Vorbis packet->PCM decoder. */
    /* First, central decode state */
   vorbis_synthesis_init(&(ovc->vorbisDSP),&(ovc->vorbisInfo));

   /* Second, local state for most of the decode so multiple block
     decodes can proceed in parallel. We could init multiple
     vorbis_block structures for vd here */
   vorbis_block_init(&(ovc->vorbisDSP),&(ovc->vorbisWorkingBlock));

   return 1;
}

/* Convert the float values (-1.<=range<=1.) to whatever PCM format and write it out
    o **pcm is a multichannel float vector. In stereo, for example,
            pcm[0] is left, and pcm[1] is right.
    o samples is the size of each channel. */
int PCMfloatsToIntPCM(int samples, float **pcm, int bout, ogg_vorbis_context * oggVorbisContext) {
    /* convert floats to 16 bit signed ints (host order) and interleave */
    int j;
    int i;
    int clipflag=0;
    int channels = oggVorbisContext->vorbisInfo.channels;
    for(i=0;i<channels;i++){
        ogg_int16_t *ptr=(oggVorbisContext->convbuffer)+i;
        float  *mono=pcm[i];
        for(j=0;j<bout;j++){
            int val=mono[j]*32767.f;
            /* might as well guard against clipping */
            if(val>32767){
                val=32767;
                clipflag=1;
            }
            if(val<-32768){
                val=-32768;
                clipflag=1;
            }
            *ptr=val;
            ptr+=channels;
        }
    }
    return clipflag;
}

int decodeDataStream(ogg_vorbis_context * oggVorbisContext) {
   int vs_result;
   int result;
   int convsize = oggVorbisContext->convsize;
   float **pcm;
   int samples;
   bool havedata=FALSE;

   clearBuffer(oggVorbisContext);
   while (TRUE) { // Our exit condition is either packet read failure (start of loop) or having data (end of loop)
      result = readPacket(oggVorbisContext);
      if (result <0) return result; // Pass back errors

      // Otherwise we have a packet usable in oggVorbisContext->oggPacket
      // We can now decode it! Yay!
      vs_result=vorbis_synthesis(&(oggVorbisContext->vorbisWorkingBlock),
                                 &(oggVorbisContext->oggPacket));
      if(vs_result==0) { /* test for success! */
         vorbis_synthesis_blockin(&(oggVorbisContext->vorbisDSP),&(oggVorbisContext->vorbisWorkingBlock));
      }
      
      havedata=FALSE; // This variable act as a marker to say if we entered the loop

      samples=vorbis_synthesis_pcmout(&(oggVorbisContext->vorbisDSP),&pcm);
      while(samples>0) {
         int clipflag=0;
         int bout=(samples<convsize?samples:convsize);
         havedata=TRUE; // Marker to not we entered this loop
         clipflag = PCMfloatsToIntPCM(samples, pcm, bout, oggVorbisContext);
         if(oggVorbisContext->warnClipping && clipflag)
            fprintf(stderr,"Clipping in frame %ld\n",(long)(oggVorbisContext->vorbisDSP.sequence));

         bufferResults(oggVorbisContext,bout);
         /* tell libvorbis how many samples we actually consumed */
         vorbis_synthesis_read(&(oggVorbisContext->vorbisDSP),bout);
         samples=vorbis_synthesis_pcmout(&(oggVorbisContext->vorbisDSP),&pcm);
      }
      if (havedata) // If we entered the loop it means we have data
         return HAVEDATA;
   }
}

void clearBuffer(ogg_vorbis_context *  oggVorbisContext){
   /* The approach we take is to always reallocate a new buffer at this point */
   /* This is mainly for simplicity, and simplifies memory management */
   if (oggVorbisContext->buffer)
      free(oggVorbisContext->buffer);
   oggVorbisContext->buffer = NULL;
   oggVorbisContext->bufferlen = 0;
}

void bufferResults(ogg_vorbis_context *  oggVorbisContext, int bout){
   char * buffer;
   int len = 2*(oggVorbisContext->vorbisInfo.channels)*bout;
   if (! oggVorbisContext->buffer) {
      /* If no data from this packet has been buffered, grab a buffer, and copy
         in the data from the conversion buffer */
      buffer = (char *) malloc(len);
      memcpy((void *) buffer, (void *) oggVorbisContext->convbuffer, len);
      oggVorbisContext->buffer = buffer;
      oggVorbisContext->bufferlen = len;
   }
    else {
      /* Otherwise we need to create a larger buffer, copy in the already buffered
         data, free up the old buffer's memory, then add the new data onto the end.
         This might seem overly simple - why not allocate something bigger initially?
         Again simplicity.
         */
      buffer = (char *) malloc(oggVorbisContext->bufferlen + len);
      memcpy((void *) buffer, (void *) oggVorbisContext->buffer, oggVorbisContext->bufferlen);

      free(oggVorbisContext->buffer);        /* Discard old buffer, */
      oggVorbisContext->buffer = buffer ;    /* And use the enlarged one that contains the old data */
      buffer += oggVorbisContext->bufferlen; /* Shift temporary pointer to just end of existing data */
      oggVorbisContext->bufferlen += len;    /*Copy new data in at that point, and update buffer length */
      memcpy((void *) buffer, (void *) oggVorbisContext->convbuffer, len);
   }
}

decode_buffer * getAudio(ogg_vorbis_context * oggVorbisContext){
   int _result;
   decode_buffer * result; /* Beginning to think this might be part of context */
   result = newDecodeBuffer(NORMAL); // FIXME: Memory leak
   switch (oggVorbisContext->decodeState) {
      case STARTSTATE:
         result->status = NEEDDATA;
         oggVorbisContext->decodeState = CHECKSTREAMOGGVORBIS;
         break;
      case CHECKSTREAMOGGVORBIS:
         oggVorbisContext->decodeState = FAILSTATE;
         if ( ( (_result= checkStreamOggVorbis(oggVorbisContext))>0 ) ) {
            oggVorbisContext->decodeState = READCOMMENTANDCODEBOOKHEADERS;
         }
         if (_result == NEEDDATA) {
            oggVorbisContext->decodeState = CHECKSTREAMOGGVORBIS;
            result->status = NEEDDATA;
         }
         break;
      case READCOMMENTANDCODEBOOKHEADERS:
         _result = readCommentAndCodebookHeaders(oggVorbisContext);
         switch (_result) {
            case COMMENTANDCODEBOOKHEADERSREAD:
               oggVorbisContext->decodeState = MAINDATADECODELOOP;
               break;
            case NEEDDATA:
               result->status = NEEDDATA;
               break;
            default:
               oggVorbisContext->decodeState = FAILSTATE;
               break;
         }
         break;
      case MAINDATADECODELOOP:
         _result = decodeDataStream(oggVorbisContext);
         // FIXME: Needs to handle end of stream correctly
         //        currently looks at EOF
         if (_result==NEEDDATA)
            result->status = NEEDDATA;
         if (_result == HAVEDATA) {
            if (oggVorbisContext->bufferlen>0) {
               /* We pass back aliases to the internal passback buffers */
               result->buffer = oggVorbisContext->buffer;
               result->len = oggVorbisContext->bufferlen;
               result->status = HAVEDATA;
            }
         }
         break;
      default:
         result->status = NEEDDATA; /* NO! it should die! */
         break;
   }
   return result;
}

void readData(source_buffer * sourceBuffer){
   sourceBuffer->_bytes = -1;
   if (!sourceBuffer->buffer) {
      fprintf(stderr, "No buffer to read data into\n");
      return;
   }
   sourceBuffer->_bytes = fread(sourceBuffer->buffer,1,sourceBuffer->buffersize, sourceBuffer->fh);
}
