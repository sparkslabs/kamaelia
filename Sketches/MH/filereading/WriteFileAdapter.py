#!/usr/bin/env python

import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class WriteFileAdapter(component):
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
       super(WriteFileAdapter, self).__init__()
       
       
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
#       print "WFA done"

               
   def shutdown(self):
      if self.dataReady("control"):
          msg = self.recv("control")
          if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
              self.send(msg, "signal")
              return True
      return False
      
               
   def closeDownComponent(self):
      self.file.close()

      
      
if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    from Axon.Scheduler import scheduler
    from ReadMultiFileAdapter import RateControlledReadFileAdapter

    pipeline( RateControlledReadFileAdapter("WriteFileAdapter.py"),
              WriteFileAdapter("/tmp/tmp_WriteFileAdapter.py")
            ).activate()
    
    scheduler.run.runThreads(slowmo=0)
