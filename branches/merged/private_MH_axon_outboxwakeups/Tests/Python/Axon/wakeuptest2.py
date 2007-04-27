#!/usr/bin/env python

# test for wakeups on message delivery
# this is a rough test only, and not really suitable (yet) to be part of the
# test suite

from Axon.ThreadedComponent import threadedcomponent
from Axon.AxonExceptions import noSpaceInBox

import time

class Producer(threadedcomponent):
    def __init__(self):
        super(Producer,self).__init__(queuelengths=1)
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
                    print repr(self),"unpaused"


class SlowConsumer(threadedcomponent):
    def __init__(self, numExpected):
        super(SlowConsumer,self).__init__(queuelengths=1)
        self.inboxes['inbox'].setSize(1)
        self.numExpected = numExpected
        
    def main(self):
        for _ in range(0,self.numExpected):
            time.sleep(0.5)
            while not self.anyReady():
                self.pause()
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
         
