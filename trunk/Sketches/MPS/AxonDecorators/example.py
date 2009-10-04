#!/usr/bin/python

import sys
import time
import re
import Axon
from Kamaelia.Chassis.Pipeline import Pipeline
from decorators import blockingProducer, TransformerGenComponent

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
