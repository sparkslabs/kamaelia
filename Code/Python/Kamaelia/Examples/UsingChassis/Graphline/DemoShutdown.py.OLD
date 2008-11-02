#!/usr/bin/python

import time
import Axon
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer

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
        self.send(msg, "signal")
        yield 1

print "If the graphline's 'control' and 'signal' boxes aren't wired to anything"
print "Graphline will make sure all child components shutdown and will pass it on"

Pipeline(
    Pinger(),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        TO_SHUTDOWN3 = Waiter(),
        linkages = {
            ("TO_SHUTDOWN1", "signal") : ("TO_SHUTDOWN2", "control"),
        }
    ),
    ConsoleEchoer(),
).run()

print "Success!"
print 
print "Now a 2nd test (slightly different)..."

Pipeline(
    Pinger(),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        linkages = {
            ("self", "control") : ("TO_SHUTDOWN1", "control"),
            ("TO_SHUTDOWN1", "signal") : ("TO_SHUTDOWN2", "control"),
            ("TO_SHUTDOWN2", "signal") : ("self", "signal"),
        }
    ),
    ConsoleEchoer(),
).run()

print 
print "Now a 3rd test (slightly different)..."

Pipeline(
    Pinger(),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        linkages = {
#            ("self", "control") : ("TO_SHUTDOWN1", "control"),
            ("TO_SHUTDOWN1", "signal") : ("TO_SHUTDOWN2", "control"),
            ("TO_SHUTDOWN2", "signal") : ("self", "signal"),
        }
    ),
    ConsoleEchoer(),
).run()


print 
print "Now a 4th test (slightly different)..."

Pipeline(
    Pinger(),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        linkages = {
            ("self", "control") : ("TO_SHUTDOWN1", "control"),
            ("TO_SHUTDOWN1", "signal") : ("TO_SHUTDOWN2", "control"),
#            ("TO_SHUTDOWN2", "signal") : ("self", "signal"),
        }
    ),
    ConsoleEchoer(),
).run()

print
print "Now this one will fail to terminate ..."

Pipeline(
    Pinger(),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        linkages = {
            ("self", "control") : ("TO_SHUTDOWN1", "control"),
#            ("TO_SHUTDOWN1", "signal") : ("TO_SHUTDOWN2", "control"),
            ("TO_SHUTDOWN2", "signal") : ("self", "signal"),
        }
    ),
    ConsoleEchoer(),
).run()
