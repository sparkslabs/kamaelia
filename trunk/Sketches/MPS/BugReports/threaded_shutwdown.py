#!/usr/bin/env python

import random

import Axon
from Axon.Ipc import shutdownMicroprocess, producerFinished
from Kamaelia.Chassis.Pipeline import Pipeline

class Source(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        self.send(random.random(), 'outbox')
        self.send(producerFinished(), 'signal')
        print 'source done'



class Sink(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        while True:
            if self.dataReady('inbox'):
                msg = self.recv('inbox')
                print 'sink', msg
            elif self.dataReady('control'):
                msg = self.recv('control')
                self.send(msg, 'signal')
                if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                    break
            else:
                self.pause()
        print 'sink done'

for i in range(500):
    print i
    Pipeline(
        Source(),
        Sink(),
        ).run()
