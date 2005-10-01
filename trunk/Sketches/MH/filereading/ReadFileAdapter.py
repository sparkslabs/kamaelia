#!/usr/bin/env python
# RETIRED
print """
/Sketches/filereading/ReadFileAdapter.py:

 This file has been retired.
 It is retired because it is now part of the main code base.
 If you want to use this, you should be using Kamaelia.File.Reading
    ReadFileAdapter here is named PromptedFileReader there

 This file now deliberately exits to encourage you to fix your code :-)
 (Hopefully contains enough info to help you fix it)
"""

import sys
sys.exit(0)
#

import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class ReadFileAdapter(component):
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
       super(ReadFileAdapter, self).__init__()
       
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
#       print "RFA done"

               
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