#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#
# Development history: /Sketches/filereading/ReadFileAdapter.py
#          ReadFileAdapter --> PromptedFileReader
#

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class PromptedFileReader(component):
   """Provides read access to a file.
      You request numbers of bytes/lines of data.
      Data is returned in response.
      
      Bytes returned as a single string
      Line(s) returned as a single string
      
      Shuts down in response to a shutdownMicroprocess message
   """
   Inboxes = { "inbox" : "requests to 'n' read bytes/lines",
               "control" : ""
             }
   Outboxes = { "outbox" : "data output",
                "signal" : "outputs 'producerFinished' after all data has been read"
              }

   def __init__(self, filename, readmode="bytes"):
       """Initialisation
       
          filename = name of file to read data from
          readmode = "bytes" to read in 'n' byte chunks
                   = "lines" to read 'n' line chunks
                      ('n' sent to inbox to request the data)
       """
       super(PromptedFileReader, self).__init__()
       
       if readmode == "bytes":
          self.read = self.readNBytes
       elif readmode == "lines":
          self.read = self.readNLines
       else:
           raise ValueError("readmode must be 'bytes' or 'lines'")
       
       self.file = open(filename, "rb",0)
       
       
   def readNBytes(self, n):
       data = self.file.read(n)
       if not data:
           raise "EOF"
       return data
   
   
   def readNLines(self, n):
       data = ""
       for i in xrange(0,n):
           data += self.file.readline()
       if not data:
           raise "EOF"
       return data
   
          
   def main(self):
       done = False
       while not done:
           yield 1
           
           if self.dataReady("inbox"):
               n = int(self.recv("inbox"))
               try:
                   data = self.read(n)
                   self.send(data,"outbox")
               except:
                   self.send(producerFinished(self), "signal")
                   done = True
           
           if self.shutdown():
               done = True
           else:
               self.pause()
               
   def shutdown(self):
      if self.dataReady("control"):
          msg = self.recv("control")
          if isinstance(msg, shutdownMicroprocess):
              self.send(msg, "signal")
              return True
      return False
      
               
   def closeDownComponent(self):
      self.file.close()

if __name__ == "__main__":
    pass