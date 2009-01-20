#!/usr/bin/python

import time
import Axon
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer

class Pinger(Axon.ThreadedComponent.threadedcomponent):
    tosend = [ ]
    box = "signal"
    delay = 0.3
    def main(self):
        i = 0
        for i in self.tosend:
            time.sleep(1.0)
            self.send(Axon.Ipc.producerFinished(), self.box)
            print "PINGER: sent", i
    
class Waiter(Axon.Component.component):
    def main(self):
        print "WAITER", self.id, "waiting"
        while not self.dataReady("control"):
            if not self.anyReady(): self.pause()
            yield 1
        msg = self.recv("control")
        print "WAITER", self.id, "shutting down having recieved:", msg
        self.send(msg, "signal")
        yield 1

class Whinger(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        while not self.dataReady("control"):
            print "WHINGER: waiting for shutdown"
            time.sleep(1)
        print "WHINGER: shutdown"


Pipeline(
    Pinger(tosend=[Axon.Ipc.producerFinished()],box="signal"),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        TO_SHUTDOWN3 = Waiter(),
        linkages = {
            ("TO_SHUTDOWN1","signal"):("TO_SHUTDOWN2","control"),
            ("TO_SHUTDOWN2","signal"):("TO_SHUTDOWN3","control"),
        }
    ),
    Whinger(),
).run()
