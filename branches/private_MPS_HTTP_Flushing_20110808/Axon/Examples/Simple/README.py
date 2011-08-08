#!/usr/bin/python

from Axon.Component import *

class Producer(component):
   Inboxes=[]
   Outboxes=["result"]
   def __init__(self):
      super(Producer, self).__init__()
   def main(self):
      i = 100
      while(i):
         i = i -1
         self.send("hello", "result")
         yield  1

class Consumer(component):
   Inboxes=["source"]
   Outboxes=["result"]
   def __init__(self):
      super(Consumer, self).__init__()
      self.count = 0
      self.i = 30
   def doSomething(self):
      print (self.name, "Woo",self.i)
      if self.dataReady("source"):
         self.recv("source")
         self.count = self.count +1
         self.send(self.count, "result")

   def main(self):
      yield 1
      while(self.i):
         self.i = self.i -1
         self.doSomething()
         yield 1

class testComponent(component):
   Inboxes=["_input"]
   Outboxes=[]
   def __init__(self):
      super(testComponent, self).__init__()
      self.producer = Producer()
      self.consumer = Consumer()
      self.addChildren(self.producer, self.consumer)
      self.link((self.producer, "result"), (self.consumer, "source"))
      self.link((self.consumer, "result"), (self, "_input"))
      self.addChildren(self.producer, self.consumer)

   def main(self):
      yield newComponent(*self.childComponents())
      while not self.dataReady("_input"):
         yield 1
      result = self.recv("_input")
      print ("Consumer finished with result:", result, "!")

p = testComponent()
p.activate()
scheduler.run.runThreads(slowmo=0)# context = r.runThreads()

