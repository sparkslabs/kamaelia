#!/usr/bin/python

import time
import Axon
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Console import *
from Kamaelia.Chassis.Pipeline import Pipeline

class Source(Axon.ThreadedComponent.threadedcomponent):
    value = 1
    sleep = 1
    def main(self):
        while 1:
            self.send(str(self.value), "outbox")
            time.sleep(self.sleep)

Backplane("broadcast").activate()

Pipeline(
    Source(),
    SubscribeTo("broadcast"),
    ConsoleEchoer(),
).activate()

Pipeline(
    ConsoleReader(),
    PublishTo("broadcast", forwarder=True),
    ConsoleEchoer(),
).run()

