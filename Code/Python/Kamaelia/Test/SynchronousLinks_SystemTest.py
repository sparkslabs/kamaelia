#!/usr/bin/env python2.3
#
import time
import sys ; sys.path.append("..")
from Axon.Component import component, scheduler, linkage, noSpaceInBox

class testProducer(component):
   """This producer tries to produce data and pass it on as fast as it can. The remote
   user might be able to accept data at this speed, it might not"""
   def main(self):
      print "Producer init",time.time()
      while 1:
         t = time.time()
         thingsToSend=[t]
         for i in self.synchronisedSend(thingsToSend):
            yield 1
         yield 1

class testConsumer(component):
   """This consumer consumes slowly - once per threshhold seconds."""
   threshhold =0.5
   def main(self):
      print "Consumer init"
      t = time.time()
      while 1:
         if time.time()-t > testConsumer.threshhold:
            t = time.time()
            if self.dataReady("inbox"):
               print "Collecting from these",self.inboxes
               data = self.recv("inbox")
               print "Consumer Recv", data
         yield 1

class adHocPostman(component):
   def __init__(self,producer,consumer):
      self.__super.__init__()
      self.producer = producer
      self.consumer = consumer
      self.link = linkage(self.producer,self.consumer,synchronous=True) # Link outbox to inbox
   def main(self):
      while 1:
         self.link.moveDataWithCheck() # Perform delivery
         yield 1

if __name__ =="__main__":
   producer = testProducer()
   consumer = testConsumer()
   postman  = adHocPostman(producer,consumer)
   producer.activate()
   consumer.activate()
   postman.activate()
   scheduler.run.runThreads()

