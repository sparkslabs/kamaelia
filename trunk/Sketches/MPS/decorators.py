#!/usr/bin/python

import sys
import time
import re
import Axon
from Kamaelia.Chassis.Pipeline import Pipeline

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

def blockingProducer(GF):
    def replacement(*argv, **argd):
        return BlockingProducer(g= lambda : GF(*argv,**argd))
    return replacement

def TransformerGenComponent(GF):
    class SourceIt(Axon.Component.component):
        def __init__(self, *argv, **argd):
            self.argv = argv
            self.argd = argd
            self.F = GF
            super(SourceIt, self).__init__()
        def main(self):
            F = self.F
            argv = self.argv
            if argv[0] == None:
                argv = (self.Inbox,) + argv[1:]

            argd = self.argd

            gen = F( *argv, **argd )
            while not self.dataReady("control"):
                for line in gen:
                    if line:
                        self.send(line, "outbox")
                    else:
                        break
                yield

            if self.dataReady("control"):
                self.send(self.recv("control"), "signal")
            else:
                self.send(Axon.Ipc.producerFinished(), "signal")
    return SourceIt

@blockingProducer
def follow(fname):
    "To stop this generator, you need to call it's .stop() method. The wrapper could do this"
    f = file(fname)
    f.seek(0,2) # go to the end
    while True:
        l = f.readline()
        if not l: # no data
            time.sleep(.1)
        else:
            yield l

@TransformerGenComponent
def grep(lines, pattern):
    "To stop this generator, you need to call it's .stop() method. The wrapper could do this"
    regex = re.compile(pattern)
    while 1:
        for l in lines():
            if regex.search(l):
                yield l
        yield

@TransformerGenComponent
def printer(lines):
    "To stop this generator, you need to call it's .stop() method. The wrapper could do this"
    while 1:
        for line in lines():
            sys.stdout.write(line)
            sys.stdout.flush()
        yield

Pipeline(
    follow("somefile.txt"),
    grep(None, "o"),
    printer(None)
).run()
