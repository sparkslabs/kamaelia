# http://yeoldeclue.com/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1200236224
# 
import time
import Axon
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer

class PeriodicWakeup(Axon.ThreadedComponent.threadedcomponent):
    interval = 1
    def main(self):
        while 1:
            time.sleep(self.interval)
            self.send("tick", "outbox")

class WakeableIntrospector(Axon.Component.component):
    def main(self):
        while 1:
            Q = [ q.name for q in self.scheduler.listAllThreads() ]
            Q.sort()
            self.send("*debug* THREADS"+ str(Q), "outbox")
            self.scheduler.debuggingon = False
            yield 1
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            while self.dataReady("inbox"):
                self.recv("inbox")

def activate():
    Pipeline(
        PeriodicWakeup(),
        WakeableIntrospector(),
        ConsoleEchoer(),
    ).activate()
