#!/usr/bin/python

import sys
import time
import re
import Axon
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Util.Console import ConsoleEchoer


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

if 0:
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

if 0:
    def grep(lines, pattern):
        regex = re.compile(pattern)
        while 1:
            for l in lines():
                if regex.search(l):
                    yield l
            yield

    def source():
        lines = [
           "hello",
           "world",
           "game",
           "over",
        ]
        for line in lines:
            yield line

    for line in grep( source, "l"):
        if line:
            print line
        else:
            break

class SourceIt(Axon.Component.component):
    def main(self):
        def grep(lines, pattern):
            regex = re.compile(pattern)
            while 1:
                for l in lines():
                    if regex.search(l):
                        yield l
                yield

        while not self.dataReady("control"):
            for line in grep( self.Inbox, "l"):
                if line:
                    print line
                else:
                    break
            yield

        if self.dataReady("control"):
            self.send(self.recv("control"), "signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

if 0:
    Pipeline(
        DataSource([ "hello", "world", "game", "over"] ),
        SourceIt(),
    ).run()

def source():
    for data in ["a","b","c"]:
        print data

def source2():
    for data in ["a","b","c"]:
        print data

def myWrapper(F):
    def myFunc(*argv, **argd):
        print "myFunc", F, argv, argd
        argv = (source,) + argv
        F(*argv, **argd)
    return myFunc

def myWrapper2(F):
    def myFunc(*argv, **argd):
        print "myFunc", F, argv, argd
        argv = (source,) + argv[1:]
        F(*argv, **argd)
    return myFunc

def myWrapper3(F):
    def myFunc(*argv, **argd):
        print "myFunc", F, argv, argd
        if argv[0] == None:
            argv = (source,) + argv[1:]
        F(*argv, **argd)
    return myFunc

def mockGrep(lines, pattern):
    print "mockGrep", lines, pattern

# myWrapper(mockGrep)("l")
# myWrapper2(mockGrep)(None, "l")
myWrapper3(mockGrep)(None, "l")
myWrapper3(mockGrep)(source2, "l")
