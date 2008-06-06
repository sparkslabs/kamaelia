#!/usr/bin/env python


import sys; sys.path.append("../pprocess/");
from ProcessPipelineNotComponent import ProcessPipeline
from Kamaelia.Chassis.Graphline import Graphline

import pprocess
import pygame
import Axon
import math
import time
from Axon.Ipc import producerFinished
from Axon.Ipc import producerFinished

default_test_data = ["there","once","was","a"]
class Source(Axon.Component.component):
    ToSend = default_test_data
    AllowRace = True
    def main(self):
        self.start = time.time()
        tosend = self.ToSend[:]
        while len(tosend) > 0:
            print "Source:- sending"
            self.send( tosend.pop(0), "outbox")
            yield 1
        yield 1
        self.send(producerFinished(), "signal")
        print "Source:- sent"
        if not self.AllowRace:
            time.sleep(1)
        yield 1

class Expecter(Axon.Component.component):
    Expect = default_test_data
    delay = 2
    tick = time.time()
    def ticking(self, got):
        if time.time()-self.tick > 1:
            print self.name, "tick", got
            self.tick = time.time()
    def main(self):
        self.start = time.time()
        got = []
        print "Expecter:- recieving"
        self.shuttingdown = False
        self.count = 0
        while not self.shutdown():
            self.ticking(got)
            while self.dataReady("inbox"):
                D = self.recv("inbox")
                print "Expecter:- RECIEVED", repr(D), self.count, len(self.Expect)
                got.append(D)
                self.count += 1
            yield 1

        if self.Expect == got: # Only works for basic types (lists, tuples, strings, etc)
            print "Expecter:- DATA RECIEVED INTACT", got
        else:
            print "Expecter:- DATA MANGLED", got
        self.send( self.control_message, "signal") # Pass on

    def shutdown(self):
        if time.time() - self.start < self.delay:
            return False
        if self.count != len(self.Expect):
            return False
        if not self.dataReady("control"):
            return False
        
        self.control_message = self.recv("control")
        
        msg = self.control_message # alias to make next line clearer
        if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
            print "GOT SHUTDOWN"
            return True

        return False

   
if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline

    if 1: # Basic test of Source/Expecter
        ProcessPipeline( # Interestingly, fails, BUT the IPC message gets through!
            Source(),
            Expecter(),
        ).run()

    if 0: # Basic test of Source/Expecter
        testdata = ["there","once","was","a"]
        ProcessPipeline( # Interestingly, fails, BUT the IPC message gets through!
            Source(ToSend=testdata),
            Expecter(Expect=testdata),
        ).run()

