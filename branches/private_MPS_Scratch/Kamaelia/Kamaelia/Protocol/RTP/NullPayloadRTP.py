#!/usr/bin/env python2.3
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""
Null Payload RTP Classes.
Null Payload Pre-Framer.
Null Payload RTP Packet Stuffer - Same thing.

This Null payload also assumes constant bit rate load.

Subcomponents functionality:
    
* FileControl: - Only if RFA internal - isn't
    * FileReader - only if internal - isn't
    * FileSelector - only if internal - isn't
* Format Decoding
* DataFramaing
* Command Interpreter (Likely to be component core code)
"""

from Axon.Component import component, scheduler, newComponent
"""
Null Payload PreFramer

Inputs:

  * Recieves chunks of binary data
    * Each chunk has a potentially random length.
    * The "binary data" is in fact a python string
    * The length of the chunk is therefore len(chunk)
    - "recvsrc"
  * Recieves a "send your last chunk if necessary and
    shut down" message from outside.
    - "control"

Outputs:

  - "output"
  * Tuples of (Framed binary data chunk,timestamp)
     * The data chunk is passed on as a python string
     * Data chunk format:
         
        +-+-+-+4+5+-+-+-+9...
        |length | binary data
        +-+-+-+-+-+-+-+-+-...
        
     * The length part of the chunk is a long integer
       with the MSB in byte 1 and LSB in byte 4.
     * The length refers to the length of the binary data
       in the chunk, NOT the length of the chunk + the binary data.

Issues:
    
   * PreFramer should ensure where possible that it only sends
     whole chunks. That is equal sized, except for last chunk.
   * Binary chunks recieved from the file adapator may be
     of a different size from the data chunks passed onto the
     component's output.
   * The PreFramer will need to be "told" to send the last chunk.
     -- extra inbox
   * The PreFramer needs to include information on timestamp
     information - what time index does this chunk start at?
     As a result the chunker needs to understand what sort of data
     the information passed represents at creation time.
      * This pre-framer always assumes a constant bit rate, hence
        the timestamp is derived from the data rate * data size,
        rather than looking at timecoding data.
   * RFA is external to the Pre-Framer.

Requirements:
    
   * Accept a predefined chunk size
   * Accept chunks of data & frame the data to this size
   * Timestamp the data chunk
   * Create tuples with the following info:
      * Raw payload data - as a string ready for writing to a network socket
      * timestamp of the beginning of this chunk for playback
   * Sends these tuples out it's output

Environment:
    
   * Name of source - at __init__
   * Data Rate - at __init__
   * Chunksize - at __init__
   * inboxes: recvsrc, control
   * outboxes: output (probably feedback too)
   * Current Chunk, and size (implicit)
   * current timestamp (cumulative)

Algorithm:
    
   * Note source
   * Note timestamp
   * Zero/Empty current chunk
   * Loop:
     * If current chunk size >= chunk size:
        * grab first (current chunk size) bytes
        * frame chunk
        * send chunk
        * Go back to start of loop
        * This check happens before accepting chunks in
          the case that the data we recieve is larger
          than the data chunks we send.
     * Check inboxes:
        * If control:
          * handle control message
        * If recvsrc:
          * take data
          * Add to chunk

"""

def packLengthAsString(aNumber):
   #
   # Most significant byte is in byte 1
   #
   r1, r2, byte1 = aNumber>>8,aNumber>>16,aNumber>>24
   byte2 = r2 - (byte1<<8)
   byte3 = r1 - (r2   <<8)
   byte4 = aNumber -  (r1   <<8)
   return "".join([chr(x) for x in [byte1,byte2,byte3,byte4] ])

class NullPayloadPreFramer(component):
   """
   Inboxes:
       control -> File select, file read control, framing control
       recvsrc -> Block/Chunks of raw disk data
   Outboxes:
       activatesrc -> Control messages to the file reading subsystem
       output -> The framed data, payload ready
   """
   Inboxes=["control", "recvsrc"]
   Outboxes=["output"]
   Usescomponents=[] # List of classes used.
   def __init__(self, sourcename, sourcebitrate=65536,
                chunksize=1400):
      """* Name of source - at __init__
         * Data Rate - at __init__
         * Chunksize - at __init__
      """
      super(NullPayloadPreFramer,self).__init__()
      self.sourcename=sourcename           # Note source
      self.sourcebitrate=sourcebitrate     # Note source bit rate
      self.sourceoctetrate=sourcebitrate/8.0 # Cache source octet rate
      self.chunksize=chunksize             # Note required chunksize
      self.currentchunk=""                 # Zero/Empty current chunk
      self.timestamp=0                     # Note timestamp
      self._dataSent=0                     # For more accurate timestamps!
      self.quitFlag=False                  # We're not shutting down

   def initialiseComponent(self):
      "No initialisation"
      return 1

   def updateTimestamp(self,datatosend):
      """C.updateTimestamp(datatosend)

      self.timestamp stores the timestamp of the end of the most recently
      transmitted data, whenever we send some data this timestamp needs to
      be updated. This method represents the calculation involved. (calculate
      the time period the data covers, and increment the timestamp)
      """
      self._dataSent +=len(datatosend)
      self.timestamp=self._dataSent/self.sourceoctetrate

   def makeChunk(self, datatosend):
      """C.makeChunk(datatosend) -> chunk : network ready data
      """
      lengthToSend = packLengthAsString(len(datatosend))
      chunk = lengthToSend+datatosend
      return chunk

   def sendCurrentChunk(self,sendpartial=False):
      """ * grab first (current chunk size) bytes
          * frame chunk
          * send chunk
      """
      if len(self.currentchunk) <self.chunksize and not sendpartial:
         return 0
      datatosend, self.currentchunk = self.currentchunk[0:self.chunksize], self.currentchunk[self.chunksize:]
      timestamp = self.timestamp
      self.updateTimestamp(datatosend)
      chunk = self.makeChunk(datatosend)
      result = (timestamp, chunk)
      self.send(result ,"output")
      return 1

   def handleShutdown(self):
      if len(self.currentchunk)>0:
         # If we have no more data to send we simply
         # shutdown, otherwise we simply exit.
         self.sendCurrentChunk(sendpartial=True)
         return 2    # This is so that mainBody's results when read straight through are 1,2,3,4
      return 0

   def handleControl(self):
      """returns quit flag - True means quit"""
      if self.dataReady("control"):
         message = self.recv("control")
         if message == "shutdown":
            return True
      return False      # Don't quit

   def mainBody(self):
      """Loopbody:
      """
      # If we have enough data to send, send it and done for this loop
      if len(self.currentchunk) >= self.chunksize:
         self.sendCurrentChunk()
         return 1

      # If we're in shutdown mode, handle shutdown procedure.
      # NB, this can repeat - which is why we return the value we do
      if self.quitFlag:
         return self.handleShutdown()  # 2 or 0

      # Collect any data to send and add it onto the data to send queue
      if self.dataReady("recvsrc"):
         self.currentchunk += self.recv("recvsrc")
         return 3

      # Check for a control message - which could be a shutdown so we need
      # to catch the return value
      if self.dataReady("control"):
         self.quitFlag = self.handleControl()
         return 4
      return 5

   def closeDownComponent(self):
      "No closedown/shutdown code"
      pass

__kamaelia_components__  = ( NullPayloadPreFramer, )


if __name__ =="__main__":
   from Kamaelia.Util.Console import ConsoleEchoer
   from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor

   class NullPayloadPreFramer_testHarness(component):
      #Inboxes=["inbox"] List of inbox names if different
      #Outboxes=["outbox"] List of outbox names if different
      #Usescomponents=[] # List of classes used.

      def __init__(self):
         super(NullPayloadPreFramer_testHarness,self).__init__() # !!!! Must happen, if this method exists
         self.source = ReadFileAdaptor("Support/BlankFile.txt", readsize="1450", steptime=0)
         self.transform = NullPayloadPreFramer("TestSource", 65536, chunksize=257)
         self.sink = ConsoleEchoer()

      def initialiseComponent(self):
         self.link( (self.source, "outbox"), (self.transform, "recvsrc"))
         self.link( (self.transform, "output"), (self.sink, "inbox"))
         return newComponent(self.source, self.transform, self.sink)

      def mainBody(self):
         "The system will run until it hits a dead end, and then spin"
         return 1

   NullPayloadPreFramer_testHarness().activate()
   scheduler.run.runThreads()
