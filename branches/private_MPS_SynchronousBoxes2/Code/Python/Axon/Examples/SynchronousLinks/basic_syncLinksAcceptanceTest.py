#!/usr/bin/python

from Axon.Component import *
import Axon.Component
print component.__init__.__doc__
class Consumer(component):
    Inboxes = ["source"]
    Outboxes = ["result"]

    def __init__(self):
        super(Consumer, self).__init__()
        print "huh?"
        #this variable is not used for anything important
        self.i = 30
    
    def dosomething(self):
        if self.dataReady("source"):
            op = self.recv("source")
            print self.name,"received --> ",op
            self.send(op,"result")

    def main(self):
        yield 1
        while(self.i):
            self.i = self.i - 1
            self.dosomething()
            yield 1
        print "Consumer has finished consumption !!!"

class Producer(component):
   Inboxes=[]
   Outboxes=["result"]
   def __init__(self):
      super(Producer, self).__init__()
   def main(self):
      i = 30
      while(i):
         i = i - 1
         try:
            self.send("hello"+str(i), "result")
            self.send("hello"+str(i), "result")
            print self.name," sent --> hello"+str(i)
         except noSpaceInBox, e:
            print "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            print "Failed to deliver"
            size, capacity = e.args
            print "Box Capacity", capacity
            print "Current size", size
         yield 1
      print "Producer has finished production !!!"

class testComponent(component):
    Inboxes = ["_input"]
    Outboxes = []
    def __init__(self):
        super(testComponent, self).__init__()
        self.producer = Producer()
        self.consumer = Consumer()
        self.addChildren(self.producer,self.consumer)
        #link the source i.e. "result" to the sink i.e. "source"
        #this is the arrow no.1
        L = self.link((self.producer,"result"),(self.consumer,"source"), pipewidth=5)
        print "PIPEWIDTH", L.setSynchronous()
        print "PIPEWIDTH", L.setSynchronous(4)
        L.setShowTransit(True, "Producer, Consumer")
        #source_component     --> self.consumer
        #sink_component       --> self
        #sourcebox            --> result
        #sinkbox              --> _input
        #postoffice           --> self.postoffice
        #i.e. create a linkage between the consumer (in consumer.py) and 
        #ourselves. The output from the consumer will be used by us. The
        #sourcebox (outbox) would be "result" and the sinkbox (inbox) would
        #be our box "_input"
        #this is the arrow no. 2
        self.link((self.consumer,"result"),(self,"_input"))

    def childComponents(self):
        return [self.producer,self.consumer]
    
    def main(self):
        yield newComponent(*self.childComponents())
        while not self.dataReady("_input"):
            yield 1
        result = self.recv("_input")
        print "consumer finished with result: ", result , "!"

testComponent().run()

