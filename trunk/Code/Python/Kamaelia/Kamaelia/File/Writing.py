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
# Development history: /Sketches/filereading/WriteFileAdapter.py
#          WriteFileAdapter --> FileWriter
#

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class SimpleFileWriter(component):
   """Provides write access to a file.
      Shuts down in response to a shutdownMicroprocess message or producerFinished message
   """
   Inboxes = { "inbox" : "data to write to file",
               "control" : ""
             }
   Outboxes = { "outbox" : "",
                "signal" : "outputs 'producerFinished' after all data has been read"
              }

   def __init__(self, filename, readmode="bytes"):
       """Initialisation
       
          filename = name of file to write to
       """
       super(SimpleFileWriter, self).__init__()
       self.file = open(filename, "wb",0)
       
   def writeData(self, data):
       data = self.file.write(data)
          
   def main(self):
       done = False
       while not done:
           yield 1
           
           if self.dataReady("inbox"):
               data = self.recv("inbox")
               self.writeData(data)
           
           if self.shutdown():
               done = True
           else:
               self.pause()
               
   def shutdown(self):
      if self.dataReady("control"):
          msg = self.recv("control")
          if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
              self.send(msg, "signal")
              return True
      return False
      
               
   def closeDownComponent(self):
      self.file.close()

      
if 0:
    print "Temporarily disabled tests since they rely on code in /Sketches"
    if __name__ == "__main__":
        from Kamaelia.Util.PipelineComponent import pipeline
        from ReadMultiFileAdapter import RateControlledReadFileAdapter

        pipeline( RateControlledReadFileAdapter("WriteFileAdapter.py"),
                  SimpleWriter("/tmp/tmp_WriteFileAdapter.py")
                ).run()
