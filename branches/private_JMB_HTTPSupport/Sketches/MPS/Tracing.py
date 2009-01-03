#!/usr/bin/python

import Axon
from Kamaelia.Chassis.Pipeline import Pipeline

class Tracer(Axon.Component.component):
    tag = "default"
    def main(self):
        print self.tag, "running"
        while 1:
            while not self.anyReady():
                self.pause
                yield 1

            while self.dataReady("inbox"):
                d = self.recv("inbox")
                print self.tag, "data", repr(d)
                self.send(d,"outbox")

            while self.dataReady("control"):
                d = self.recv("control")
                print self.tag, "control", repr(d)
                self.send(d,"signal")

def Trace(someComponent,tracetag=":"):
    return Pipeline(
        Tracer(tag="in"+tracetag),
        someComponent,
        Tracer(tag="out"+tracetag),
    )
