#!/usr/bin/python

import time
import sys

def follow(fname):
    f = file(fname)
    f.seek(0,2) # go to the end
    while True:
        l = f.readline()
        if not l: # no data
            time.sleep(.1)
        else:
            yield l

def printer(lines):
    for line in lines():
        sys.stdout.write(line)
        sys.stdout.flush()

if 0:
    g = lambda : follow("somefile.txt")
    printer(g)

if 1:
    import Axon
    class BlockingProducer(Axon.ThreadedComponent.threadedcomponent):
        g = None
        def main(self):
            def source():
                for i in range(10):
                    yield str(i)+"\n"
                yield
                print "Source done"
            if self.g:
                source = self.g

            while not self.dataReady("control"):
                for data in source():
                    self.send(data, "outbox")
                break

            if self.dataReady("control"):
                self.send(self.recv("control"), "signal")
            else:
                self.send(Axon.Ipc.producerFinished(), "signal")

if 0:
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer

    Pipeline(
        BlockingProducer(g = lambda : follow("somefile.txt")),
        ConsoleEchoer(),
    ).run()

if 0:
    def mydecorator(F):
        print "Decorating"
        def replacement(*args, **argv):
            F()
            print "Game Over", args, argv
        print "Decorated"
        return replacement

    @mydecorator
    def greeting():
        print "Hello World"

    greeting("testing", "testing", g="123")

def blockingProducer(GF):
    def replacement(*argv, **argd):
        return BlockingProducer(g= lambda : GF(*argv,**argd))
    return replacement

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer

@blockingProducer
def follow(fname):
    f = file(fname)
    f.seek(0,2) # go to the end
    while True:
        l = f.readline()
        if not l: # no data
            time.sleep(.1)
        else:
            yield l

Pipeline(
    follow("somefile.txt"),
    ConsoleEchoer(),
).run()
