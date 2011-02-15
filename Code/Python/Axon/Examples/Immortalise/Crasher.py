#!/usr/bin/python

import Axon
import random

class myException(Exception):
    pass

print ("Please look at the source of this file to see what's going on")

#
# Doing the following will make the schedule call .stop() on any components
# that crash, but not cause the scheduler to crash.
#
if 1:
    Axon.Scheduler.scheduler.immortalise()

#
# Doing the following returns the scheduler to it's normal behaviour - ie
# only catching StopIteration and calling .stop() on components that do that
# (or on scheduler .stop())
#

if 0:
    Axon.Scheduler.scheduler.mortalise()

class Crasher(Axon.Component.component):
    def main(self):
        while 1:
            c = 0
            while 1:
                if random.randint(0,100) < 5:
                    print ("Returning Normally")
                    return
                elif random.randint(0,100) < 10:
                    print ("Raising Exception")
                    raise myException()
                else:
                    yield c
                c = c+1
    def stop(self):
        print (".stop() called in Crasher")
        super(Crasher, self).stop()

Crasher().run()

