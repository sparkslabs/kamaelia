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
   
   cdef object sourceQueue
   cdef long int sourceQueueLen

   def __new__(self):
      self.sourceBuffer = newSourceBuffer(NULL,BUFSIZE)
      self.oggVorbisContext = newOggVorbisContext()
      self.decodeBuffer = NULL
      self.sourceQueue = []
      self.sourceQueueLen = 0
      
   def __dealloc__(self):
      if self.decodeBuffer:
         free(self.decodeBuffer)
         self.decodeBuffer = NULL

   def sendBytesForDecode(self, bytes):
       self.sourceQueue.append(bytes)
       self.sourceQueueLen = self.sourceQueueLen + len(bytes)
       
   def __dequeueToDecoder(self):
      cdef int count
      cdef int i
      cdef int j
      cdef object fragment
      
      # make sure we take at least 58 bytes (minimum accepted by libvorbis)
      
      if self.sourceQueueLen < 58:
          raise "NEEDDATA"
      
      # don't take more than there is space in the buffer
      count = min(self.sourceQueueLen, BUFSIZE)
      
      # make sure we don't leave a straggling remains of <58 bytes
      if count < BUFSIZE and count > (BUFSIZE - 58):
          count = BUFSIZE - 58
          
      # copy from fragments into source buffer
      self.sourceBuffer.bytes = count
      self.sourceQueueLen = self.sourceQueueLen - count
      i=0
      while count > 0:
          fragment = self.sourceQueue[0]
          
          # copy from fragment
          for j from 0 <= j < min(len(fragment), count):
              self.sourceBuffer.buffer[i] = ord(fragment[j])
              i=i+1
          
          count=count-j
          
          # if we've used the whole fragment, bin it; otherwise trim it to what's left
          if j == len(fragment):
              del self.sourceQueue[0]
          else:
              self.sourceQueue[0] = self.sourceQueue[0][j:]

      sendBytesForDecode(self.oggVorbisContext, self.sourceBuffer);
      
   def _getAudio(self):
      # repeatedly try to get audio data, supplying data when requested if we
      # have some available...
      # ...until we don't have any, or the vorbis decoder says something else
      while 1:
         if self.decodeBuffer:
             free(self.decodeBuffer)
             self.decodeBuffer = NULL
             
         self.decodeBuffer = getAudio(self.oggVorbisContext)
        
         if self.decodeBuffer.status == NEEDDATA:
             self.__dequeueToDecoder()
         else:
             break


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
