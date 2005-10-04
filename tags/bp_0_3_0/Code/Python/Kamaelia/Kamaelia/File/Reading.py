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
# Development history: 
#     ReadFileAdapter --> PromptedFileReader
#          /Sketches/filereading/ReadFileAdapter.py

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Util.RateFilter import ByteRate_RequestControl
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Util.Graphline import Graphline

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

def RateControlledFileReader(filename, readmode = "bytes", **rateargs):
    """ReadFileAdapter combined with a RateControl component
       Returns a component encapsulating a RateControl and ReadFileAdapter components.
            filename   = filename
            readmode   = "bytes" or "lines"
            **rateargs = named arguments to be passed to RateControl
        """
    return Graphline(RC  = ByteRate_RequestControl(**rateargs),
                     RFA = PromptedFileReader(filename, readmode),
                     linkages = { ("RC",  "outbox")  : ("RFA", "inbox"),
                                  ("RFA", "outbox")  : ("self", "outbox"),
                                  ("RFA", "signal")  : ("RC",  "control"),
                                  ("RC",  "signal")  : ("self", "signal"),
                                  ("self", "control") : ("RFA", "control")
                                }
    )


def ReusableFileReader(readmode):
    # File name here is passed to the this file reader factory every time
    # the file reader is started. The /reason/ for this is due to the carousel
    # can potentially pass different file names through each time. In essence,
    # this allows the readfile adaptor to be /reusable/

    def PromptedFileReaderFactory(filename):
        return PromptedFileReader(filename=filename, readmode=readmode)

    return Carousel(PromptedFileReaderFactory)

def RateControlledReusableFileReader(readmode):
    # The arguments passed over here are provided by the carousel each time an
    # instance is required.
    #
    # Specifically this means this creates a component that accepts on its
    # inbox filenames and arguments relating to the speed at which to read
    # that file. That file is then read in that manner and when it's done,
    # it waits to receive more commands regarding which files to read and
    # how.
    def RateControlledFileReaderFactory(args):
        filename, rateargs = args
        return RateControlledFileReader(filename, readmode, **rateargs)

    return Carousel( RateControlledFileReaderFactory )

def FixedRateControlledReusableFileReader(readmode = "bytes", **rateargs):
    """A file reading carousel, that reads at a fixed rate.
       Takes filenames on its inbox
    """
    return Graphline(RC       = ByteRate_RequestControl(**rateargs),
                     CAR      = ReusableFileReader(readmode),
                     linkages = {
                         ("self", "inbox")      : ("CAR", "next"),
                         ("self", "control")    : ("RC", "control"),
                         ("RC", "outbox")       : ("CAR", "inbox"),
                         ("RC", "signal")       : ("CAR", "control"),
                         ("CAR", "outbox")      : ("self", "outbox"),
                         ("CAR", "signal")      : ("self", "signal"),
                         ("CAR", "requestNext") : ("self", "requestNext"),
                         ("self", "next")       : ("CAR", "next")
                     }
           )







if __name__ == "__main__":
    pass
    
    





