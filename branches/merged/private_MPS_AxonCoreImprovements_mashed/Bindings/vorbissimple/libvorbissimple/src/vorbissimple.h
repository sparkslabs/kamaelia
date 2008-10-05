#ifndef GUARD_LIBVORBISSIMPLE_H
#define GUARD_LIBVORBISSIMPLE_H
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
// FIXME: Currently the minimum buffer size is 58. (needs work!)
#define BUFSIZE 4096
#define FALSE 0
#define TRUE 1

#define PACKETREAD 1
#define PAGEREAD 1
#define COMMENTANDCODEBOOKHEADERSREAD 1
#define HAVEDATA 2

#define NEEDDATA -1
#define NORMAL -2
#define STARTSTATE -3
#define READFIRSTOGGPAGE -4
#define NOFIRSTPAGE -5
#define CHECKSTREAMOGGVORBIS -6
#define FAILSTATE -7
#define READCOMMENTANDCODEBOOKHEADERS -8
#define CORRUPTPAGE -10
#define CORRUPTPACKET -11
#define NOTOGGVORBIS -12
#define MAINDATADECODELOOP -14
/*
 * Types used by this example
 */
typedef int bool;

typedef struct {
   int decodeState;
   ogg_sync_state   oggSync;            /* sync and verify incoming physical bitstream */
   ogg_page         oggBitstreamPage;   /* one Ogg bitstream page.  Vorbis packets are inside */
   ogg_stream_state oggStream;          /* take physical pages, weld into a logical stream of packets */
   ogg_packet       oggPacket;          /* one raw packet of data for decode */
   vorbis_info      vorbisInfo;         /* struct that stores all the static vorbis bitstream settings */
   vorbis_comment   vorbisComment;      /* struct that stores all the bitstream user comments */
   vorbis_dsp_state vorbisDSP;          /* central working state for the packet->PCM decoder */
   vorbis_block     vorbisWorkingBlock; /* local working space for packet->PCM decode */
   ogg_int16_t convbuffer[BUFSIZE];     /* take 8k out of the data segment, not the stack */
   bool streamInitialised;
   bool warnClipping;
   int headerPacketsRead;
   int convsize;
   char * buffer; // Intermediate decode buffer (for passback to client)
   int    bufferlen;
} ogg_vorbis_context;

typedef struct {
   FILE * fh;
   char * buffer;
   int bytes;
   int buffersize;
} source_buffer;

typedef struct {
   char * buffer; // The actual storage space
   int len;
   int status;
} decode_buffer;

/* Prototypes */
extern ogg_vorbis_context * newOggVorbisContext(void);
extern source_buffer * newSourceBuffer(FILE * fh, int buffersize);
extern decode_buffer * newDecodeBuffer(int status) ;
extern int checkStreamOggVorbis(ogg_vorbis_context * oggVorbisContext);
extern int readPage(ogg_vorbis_context * oggVorbisContext);
extern int readPacket(ogg_vorbis_context * oggVorbisContext);
extern int readCommentAndCodebookHeaders(ogg_vorbis_context * oggVorbisContext);
extern int decodeDataStream(ogg_vorbis_context * oggVorbisContext);
extern int PCMfloatsToIntPCM(int samples, float **pcm, int bout, ogg_vorbis_context * oggVorbisContext);
extern void readData(source_buffer * sourceBuffer);
extern void sendBytesForDecode(ogg_vorbis_context * ovc, source_buffer *sourceBuffer);
extern void clearBuffer(ogg_vorbis_context *  oggVorbisContext);
extern void bufferResults(ogg_vorbis_context *  oggVorbisContext, int bout);
extern decode_buffer * getAudio(ogg_vorbis_context * oggVorbisContext);

#endif
