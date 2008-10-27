#!/usr/bin/python

import time
import Axon
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline

class Pinger(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        time.sleep(1.0)
        self.send(Axon.Ipc.producerFinished(), "signal")
        print "sent 1!"
        time.sleep(0.5)
        self.send(Axon.Ipc.shutdownMicroprocess(), "signal")
        print "sent 2!"
        time.sleep(0.5)
    
class Waiter(Axon.Component.component):
    def main(self):
        while not self.dataReady("control"):
            print self.name, "waiting"
            if not self.anyReady():
                 self.pause()
            yield 1
        msg = self.recv("control")
        print self.name, "shutting down having recieved:", msg
        self.send("passedon", "signal")
        yield 1

Pipeline(
    Pinger(),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        TO_SHUTDOWN3 = Waiter(),
        linkages = {
            ("TO_SHUTDOWN1", "signal") : ("TO_SHUTDOWN2", "control"),
        }
    )
).run()
