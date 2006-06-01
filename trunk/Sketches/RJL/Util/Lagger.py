from Axon.Component import component
from time import sleep

class Lagger(component):
   def __init__(self, sleeptime = 0.01):
      super(Lagger, self).__init__()
      self.sleeptime = sleeptime
   
   def main(self):
      while 1:
         yield 1
         sleep(self.sleeptime)
