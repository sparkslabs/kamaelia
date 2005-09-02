#!/usr/bin/python

from Kamaelia.Util.PipelineComponent import pipeline
from Axon.Component import component
from Axon.Ipc import WaitComplete, reactivate
from random import randint

class cat(component):
    def __init__(self, data):
        super(cat, self).__init__()
        self.data = data
    def main(self):
        for item in self.data:
            self.send(item, "outbox")
            yield 1

class printer(component):
   def tick(self,ID):
      for i in (1,2,3,4,5,6,7,8,9,10):
         print "TICK", ID, i
         yield i
      print "TICK DONE"
   def main(self):
      ID = randint(0,20000)
      print "PRE-WAIT"
      yield WaitComplete(self.tick(ID))
      print "POST-WAIT"
      while 1:
         yield 1
         try:
            data = self.recv("inbox")
            print data,
         except:
           print "NO DATA READY, LETS WAIT A BIT"
           ID = randint(0,20000)
           print "PRE-WAIT"
           yield WaitComplete(self.tick(ID))
           print "POST-WAIT"

pipeline(
         cat("""\
Information Center, n.: 
A room staffed by professional computer people whose job it is to tell you why you cannot have the information you require.
""".split(" ")),
         printer(),
).run()
