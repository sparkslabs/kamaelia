#!/usr/bin/env python

from Axon.Component import component
from Kamaelia.Chassis.Pipeline import Pipeline

import sys

class MyComponent(component):
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
 
class MC2(component):
   def main(self):
      try:
        while 1:
           while self.dataReady("inbox"):
               print "Received: ", self.recv("inbox")
           while self.dataReady("control"):
               msg = self.recv("control")
               # do something with it here in normal circumstances
           yield 1
      except:
           print "MC2 Caught exception..."
           print sys.exc_info()

Pipeline(MyComponent(), MC2()).run()
