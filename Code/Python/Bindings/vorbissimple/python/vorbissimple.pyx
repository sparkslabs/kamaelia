#
# Simple pyrex access wrapper for libvorbissimple
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from libc.string cimport memset, memcpy
from libcpp cimport bool
from libc.stdint cimport uintptr_t

cdef struct FILE
cdef extern from "Python.h":
   object PyBytes_FromStringAndSize(char *, int)
   #object PyUnicode_FromStringAndSize(char *, int)
   char * PyBytes_AsString(object)
   Py_ssize_t PyBytes_Size(object)

def printable(b):
   return chr(b) if 32 <= b <128 else "."

def printable_bytes(bs):
   return "".join([printable(b) for b in bs])


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
      unsigned char* buffer
      int _bytes
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

class VSSRetry(Exception):
   pass

class VSSNeedData(Exception):
   pass

bufsize = BUFSIZE

cdef class vorbissimple:
   cdef ogg_vorbis_context* oggVorbisContext
   cdef source_buffer* sourceBuffer
   cdef decode_buffer* decodeBuffer

   cdef object sourceQueue
   cdef long int sourceQueueLen

   def __cinit__(self):
      self.sourceBuffer = newSourceBuffer(NULL,BUFSIZE)
      self.oggVorbisContext = newOggVorbisContext()
      self.decodeBuffer = NULL
      self.sourceQueue = []  # We maintain a list of buffers to send
      self.sourceQueueLen = 0  # We maintain a total length to send

   def __dealloc__(self):
      if self.decodeBuffer:
         free(self.decodeBuffer)
         self.decodeBuffer = NULL

   def sendBytesForDecode(self, _bytes):
       self.sourceQueue.append(_bytes)  # We add the bytes end and append them to our send queue
       self.sourceQueueLen = self.sourceQueueLen + PyBytes_Size(_bytes) # We increase our total to send accordinging

   def __dequeueToDecoder(self):
      cdef int count
      cdef int i
      cdef Py_ssize_t j
      cdef object fragment
      # make sure we take at least 58 bytes (minimum accepted by libvorbis)
      if self.sourceQueueLen < 58:
          raise VSSNeedData()

      # don't take more than there is space in the buffer
      count = min(self.sourceQueueLen, BUFSIZE)

      # make sure we don't leave a straggling remains of <58 bytes
      if count < BUFSIZE and count > (BUFSIZE - 58):
          count = BUFSIZE - 58

      # copy from fragments into source buffer
      self.sourceBuffer._bytes = count
      self.sourceQueueLen = self.sourceQueueLen - count

      i=0
      while count > 0:
          fragment = self.sourceQueue[0]
          j = min(PyBytes_Size(fragment), count)
          assert i + j <= self.sourceBuffer.buffersize # guard

          memcpy(self.sourceBuffer.buffer +i ,  PyBytes_AsString(fragment), j)

          i += j
          count = count-j

          # if we've used the whole fragment, bin it; otherwise trim it to what's left
          if j == PyBytes_Size(fragment):
              del self.sourceQueue[0]
          else:
              self.sourceQueue[0] = self.sourceQueue[0][j:]

      assert i == self.sourceBuffer._bytes
      sendBytesForDecode(self.oggVorbisContext, self.sourceBuffer);

   def _getAudio(self): # FIXME: this is public API, not private
      # repeatedly try to get audio data, supplying data when requested if we
      # have some available...
      # ...until we don't have any, or the vorbis decoder says something else
      while 1:
         if self.decodeBuffer:
             free(self.decodeBuffer)
             self.decodeBuffer = NULL
         # else:
             # decodeBuffer is NULL")

         self.decodeBuffer = getAudio(self.oggVorbisContext)

         if self.decodeBuffer.status == NEEDDATA: # Decoder needs data... 
             self.__dequeueToDecoder()            # So we pass some in
         else:
             break

      if self.decodeBuffer.status == HAVEDATA:

         if self.decodeBuffer.len >0:
            return PyBytes_FromStringAndSize(self.decodeBuffer.buffer,self.decodeBuffer.len)
         else:
            return b""

      if self.decodeBuffer.status == NORMAL:
         raise VSSRetry()

      raise Exception("ERROR")
   
   def fails(self):
      raise Exception("Failed! :-)")  # FIXME: Should not be a string exception
