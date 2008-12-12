#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
      super(adHocPostman, self).__init__()
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

