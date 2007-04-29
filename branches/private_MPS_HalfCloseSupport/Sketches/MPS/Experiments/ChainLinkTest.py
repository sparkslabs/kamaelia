#!/usr/bin/python


import Axon
import time

class Link(Axon.Component.component):
   def __init__(self, Next=None, source=False, echoer=False):
       super(Link, self).__init__()
       self.source = source
       self.echoer = echoer
       self.Next = Next
   def main(self):
       global N
       t = time.time()
#       print "running"
       if self.Next:
           self.link((self, "outbox"), (self.Next,"inbox"))
#           print "linking to", self.Next
           self.Next = None # release the reference
       if self.source:
           self.send("ping", "outbox")
#           print len(self.outboxes["outbox"])
       while 1:
            if not self.anyReady():
                self.pause()
                print "paused"
                yield 1
            while self.dataReady("inbox"):
               data = self.recv("inbox")
               self.send(data, "outbox")
               if self.echoer:
                   print "ping", time.time(), t-time.time(), (time.time()-t)/N*1000000
                   t = time.time()
            yield 1
                
   def addNext(self, Next):
       self.Next = Next

N = 2000

L=range(N)
L[0]  = Link(source=True)
for i in xrange(1,N-1):
    L[i]  = Link()

L[-1] = Link(echoer=True)
L[-1].addNext(L[0])
for i in xrange(N-1):
    L[i].addNext(L[i+1])

for i in xrange(N-1):
    L[i].activate()

L[-1].run()
