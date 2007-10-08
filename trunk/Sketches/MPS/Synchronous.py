#!/usr/bin/python

import Axon
import time
from Kamaelia.Chassis.Pipeline import Pipeline

class MySender(Axon.Component.component):
    def main(self):
        while 1:
            yield 1
            sent = False
            print "-----------------------------------------------------------------------"
            while not sent:
                try:
                    self.send(time.time(), "outbox")
                    sent = True
                except Axon.AxonExceptions.noSpaceInBox:
                    print "         Gah1"
#                    self.pause()
                    yield 1
                else:
                    print "NO Gah1"
            sent = False
            while not sent:
                try:
                    self.send(time.time(), "outbox")
                    sent = True
                except Axon.AxonExceptions.noSpaceInBox:
                    print "         Gah2"
#                    self.pause()
                    yield 1
                else:
                    print "NO Gah2"
            sent = False
            while not sent:
                try:
                    self.send(time.time(), "outbox")
                    sent = True
                except Axon.AxonExceptions.noSpaceInBox:
                    print "         Gah3"
#                    self.pause()
                    yield 1
                else:
                    print "NO Gah3"

class MyReceiver(Axon.Component.component):
    def main(self):
        self.setInboxSize("inbox", 1)
        t = time.time()
        while 1:
            while time.time()-t <0.1:
                yield 1
            t = time.time()
            if self.dataReady("inbox"):
                print "        ",self.recv()
            yield 1

Pipeline(
    MySender(),
    MyReceiver(),
).run()