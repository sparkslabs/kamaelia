#!/usr/bin/env python

from Axon.Component import component
from Kamaelia.Chassis.Pipeline import Pipeline
from Axon.Ipc import *

import sys, traceback

class Producer(component):
   def main(self):
      self.send("a")
      yield 1
      self.send("b")
      yield 2
      self.send("c")
      yield 3
      self.send("d")
      yield 4
      self.send("e")
 
class ProducerMakesException(component):
   def main(self):
      self.send("a")
      yield 1
      self.send("b")
      yield 2
      self.send("c")
      yield 3
      raise Exception("spam","eggs")
      yield 4
      self.send("d")
 
class Consumer(component):
   def main(self):
      try:
        while 1:
           while self.dataReady("inbox"):
               print "Received: ", self.recv("inbox")
           yield 1
      except producerFinished:
           print "It finished"
      except:
           print "MC2 Caught exception..."
           info = sys.exc_info()
           print info[1]
           print "".join(traceback.format_exception(*info))

print "==========================================="
print "Running first system ... normal termination"
print "==========================================="
Pipeline(Producer(), Consumer()).run()

print "===================================================================="
print "Running second system ... first node in pipeline throws an exception"
print "===================================================================="
Pipeline(ProducerMakesException(), Consumer()).run()

