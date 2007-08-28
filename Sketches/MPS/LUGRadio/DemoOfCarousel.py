#!/usr/bin/python
#
#

import Axon

from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Chassis.Graphline import Graphline

class Source(Axon.Component.component):
    def main(self):
        print "XXX"
        self.send(("hello","world"), "outbox")
        yield 1
        self.send(("hello1","world1"), "outbox")
        yield 1
        self.send(("hello2","world2"), "outbox")
        yield 1
        self.send(("hello3","world3"), "outbox")
        yield 1
        self.send(("hello4","world4"), "outbox")
        yield 1
        print "XXX"

def mkMyComponent(args): return MyComponent(*args)

class MyComponent(Axon.Component.component):
    Outboxes = ["outbox", "signal", "requestNext"]
    def __init__(self, *args):
        print "XXX"
        super(MyComponent, self).__init__()
        print "ARGS", args

    def main(self):
        self.send(Axon.Ipc.producerFinished, "requestNext")
        yield 1

Graphline(SOURCE= Source(),
          SPECIALISE = Carousel(mkMyComponent),
          linkages = {
              ("SOURCE","outbox"):("SPECIALISE", "next"),
          }
         ).run()