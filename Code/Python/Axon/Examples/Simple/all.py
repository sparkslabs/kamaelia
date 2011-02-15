#!/usr/bin/python

from Axon.Component import *

class Consumer(component):
    Inboxes = ["source"]
    Outboxes = ["result"]

    def __init__(self):
        super(Consumer, self).__init__()
        #this variable is not used for anything important
        self.i = 30
    
    def dosomething(self):
        if self.dataReady("source"):
            op = self.recv("source")
            print(self.name,"received --> ",op)
            return op

    def main(self):
        yield 1
        R = None
        while(self.i):
            self.i = self.i - 1
            R = self.dosomething()
            yield 1
        print ("Consumer has finished consumption !!!")
        self.send(R,"result")

class Producer(component):
   Inboxes=[]
   Outboxes=["result"]
   def __init__(self):
      super(Producer, self).__init__()
   def main(self):
      i = 30
      while(i):
         i = i - 1
         self.send("hello"+str(i), "result")
         print(self.name," sent --> hello"+str(i))
         yield 1
      print("Producer has finished production !!!")

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
        self.link((self.producer,"result"),(self.consumer,"source"))
        #source_component     --> self.consumer
        #sink_component       --> self
        #sourcebox            --> result
        #sinkbox              --> _input

        self.link((self.consumer,"result"), (self,"_input"))

    def childComponents(self):
        return [self.producer,self.consumer]
    
    def main(self):
        yield newComponent(*self.childComponents())
        while not self.dataReady("_input"):
            yield 1
        result = self.recv("_input")
        print("consumer finished with result: ", result , "!")

p = testComponent()
p.activate()
scheduler.run.runThreads(slowmo=0) 

