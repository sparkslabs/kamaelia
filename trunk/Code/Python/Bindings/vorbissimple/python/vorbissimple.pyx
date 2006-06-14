#
# Simple pyrex access wrapper for libvorbissimple
#

cdef struct FILE
cdef extern from "Python.h":
   object PyString_FromStringAndSize(char*, int)

cdef extern from "stdlib.h":
   void free(void *ptr)
   
cdef extern from "vorbissimple.h":

   # This is an opaque type as far as we're concerned
   ctypedef struct ogg_vorbis_context
   cdef int BUFSIZE

   cdef int NEEDDATA
   cdef int HAVEDATA
   cdef int NORMAL

   ctypedef struct source_buffer:
      FILE* fh
      char* buffer
      int bytes
      int buffersize

   ctypedef struct decode_buffer:
      char * buffer
      int len
      int status

   ogg_vorbis_context* newOggVorbisContext()
   source_buffer* newSourceBuffer(FILE* fh, int buffersize)

   decode_buffer* getAudio(ogg_vorbis_context* oggVorbisContext)
   void readData(source_buffer* sourceBuffer)
   void sendBytesForDecode(ogg_vorbis_context* ovc, source_buffer* sourceBuffer)

cdef class vorbissimple:
   cdef ogg_vorbis_context* oggVorbisContext
   cdef source_buffer* sourceBuffer
   cdef decode_buffer* decodeBuffer

   def __new__(self):
      self.sourceBuffer = newSourceBuffer(NULL,BUFSIZE)
      self.oggVorbisContext = newOggVorbisContext()
      self.decodeBuffer = NULL
      
   def __dealloc__(self):
      if self.decodeBuffer:
         free(self.decodeBuffer)
         self.decodeBuffer = NULL

   def sendBytesForDecode(self, bytes):
      cdef int i 
      i = 0
      while i < len(bytes):
         self.sourceBuffer.buffer[i]= ord(bytes[i])
         i = i + 1

      self.sourceBuffer.bytes = len(bytes)
      sendBytesForDecode(self.oggVorbisContext, self.sourceBuffer);

   def _getAudio(self):
      if self.decodeBuffer:
         free(self.decodeBuffer)
         self.decodeBuffer = NULL
      self.decodeBuffer = getAudio(self.oggVorbisContext)
      if self.decodeBuffer.status == NEEDDATA:
         raise "NEEDDATA"

      if self.decodeBuffer.status == HAVEDATA:

         if self.decodeBuffer.len >0:
            return PyString_FromStringAndSize(self.decodeBuffer.buffer,self.decodeBuffer.len)
         else:
            return ""

      if self.decodeBuffer.status == NORMAL:
         raise "RETRY"

      raise "ERROR"

   
   def fails(self):
      raise "Failed! :-)"


#print "test"
