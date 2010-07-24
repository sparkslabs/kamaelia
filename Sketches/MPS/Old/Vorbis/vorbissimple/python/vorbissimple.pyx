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

   def __init__(self):
      self.sourceBuffer = newSourceBuffer(NULL,BUFSIZE)
      self.oggVorbisContext = newOggVorbisContext()
      self.decodeBuffer = NULL

   def sendBytesForDecode(self, bytes):
      cdef int i 
      i = 0
#      print "VS:SB HERE 1"
      while i < len(bytes):
         self.sourceBuffer.buffer[i]= ord(bytes[i])
         i = i + 1

#      print "VS:SB HERE 2"
      self.sourceBuffer.bytes = len(bytes)
      sendBytesForDecode(self.oggVorbisContext, self.sourceBuffer);
#      print "VS:SB HERE 3", len(bytes), bytes

   def _getAudio(self):
#      print "VS:GA Here 1"
      if self.decodeBuffer:
         free(self.decodeBuffer)
#      print "VS:GA Here 2"
      self.decodeBuffer = getAudio(self.oggVorbisContext)
#      print "VS:GAHere 3"
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
