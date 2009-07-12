#!/usr/bin/python
""" 

This appears to be a minimal repeatable test case of a problem in
Axon.background.

Specifically on some runs, Axon.background will *not* wait for any
components to start before exitting. This means that anything that uses
Axon.background - including Axon.Handle can appear to not work.

Output in the case where Axon.background fails to start properly:
    <class 'Axon.background.background'>
    <background(Thread-1, initial daemon)>
    hello
    mainloop
    mainloop
    mainloop
    mainloop
    mainloop
    mainloop
    mainloop

Output in the case where Axon.background succeeds starting:

    <class 'Axon.background.background'>
    <background(Thread-1, initial daemon)>
    hello
    mainloop
    ping
    [<__main__.Pinger object at 0xb7c28d0c>]
    ping
    [<__main__.Pinger object at 0xb7c28d0c>]
    ping
    [<__main__.Pinger object at 0xb7c28d0c>]
    ping
    [<__main__.Pinger object at 0xb7c28d0c>]

This appears to be due to a race hazard, and so 1/2 the time it will
succeed, and half the time it fails. This is clearly resolvable.

"""
import time

import Axon
from Axon.background import background

print background
Y = background()
print Y
Y.start()

print "hello"

class Pinger(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        while 1:
            time.sleep(0.1)
            print "ping"
            print self.scheduler.listAllThreads()

c = 0
while 1:
    c +=1
    time.sleep(1)
    print "mainloop"
    if c == 1:
        Pinger().activate()
