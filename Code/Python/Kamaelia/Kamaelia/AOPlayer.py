"""
"""
from Axon.Component import component
import ao
import sys

class AOPlayerComponent(component):
   def __init__(self, id=None):
      self.__super.__init__()
      #if id is None:
      #   id = 'oss'
      #print "FOO1"
      #self.dev = ao.AudioDevice("oss")

   def main(self):
      print "FOO"
      while 1:
         print "BAR"
         #if self.dataReady("inbox"):
         #   buff = self.recv("inbox")
         #   bytes = len(buff)
         #   sys.stdout.write("\nARRGH\n")
         #   sys.stdout.flush()
         #   #self.dev.play(buff)
         yield 1

