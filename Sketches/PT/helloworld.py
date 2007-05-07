#!/usr/bin/env python
import time
from Axon.Component import component
from Axon.Scheduler import scheduler

class HelloPusher(component):
    def main(self):
        while True:
            time.sleep(0.5) # normally this would be a bad idea, since the entire scheduler will halt inside this component. 
            self.send("\n!ednom ,tulas", 'outbox')
            yield 1

class Reverser(component):
    def main(self):
        while True:
            if self.dataReady('inbox'):
                item = self.recv('inbox')
                self.send(item[::-1], 'outbox')
            else: self.pause()
            yield 1

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer

thepipe = Pipeline(HelloPusher(), Reverser(), ConsoleEchoer()).activate()

# thepipe = Pipeline(HelloPusher(), Reverser(), ConsoleEchoer()).run()

scheduler.run.runThreads()