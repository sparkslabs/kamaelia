#!/usr/bin/env python

# test for wakeups on message delivery
# this is a rough test only, and not really suitable (yet) to be part of the
# test suite

from Axon.Component import component
from Axon.AxonExceptions import noSpaceInBox

import time

class Producer(component):
    def main(self):
        
        for i in range(0,10):
            while 1:
                try:
                    self.send(repr(self)+" : "+repr(i),"outbox")
                    print repr(self),"sent",i
                    break
                except noSpaceInBox:
                    print repr(self),"blocked"
                    self.pause()
                    yield 1
                    print repr(self),"unpaused"


class SlowConsumer(component):
    def __init__(self, numExpected):
        super(SlowConsumer,self).__init__()
        self.inboxes['inbox'].setSize(1)
        self.numExpected = numExpected
        
    def main(self):
        for _ in range(0,self.numExpected):
            t=time.time() + 0.5
            while time.time() < t:
                yield 1
            while not self.anyReady():
                yield 1
            print "Received:",self.recv("inbox")


from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline

print
print "***ONE PRODUCER, ONE SLOW CONSUMER***"
Pipeline(Producer(), SlowConsumer(numExpected=10)).run()

print
print "***TWO PRODUCERS, ONE SLOW CONSUMER***"
Graphline( P1 = Producer(),
           P2 = Producer(),
           C = SlowConsumer(numExpected=20),
           linkages = {
               ("P1","outbox") : ("C","inbox"),
               ("P2","outbox") : ("C","inbox"),
           }
         ).run()
         
