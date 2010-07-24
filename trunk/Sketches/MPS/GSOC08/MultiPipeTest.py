#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------

import sys; sys.path.append("../pprocess/");
from MultiPipeline import ProcessPipeline
from MultiPipeline import ProcessGraphline
from Kamaelia.Chassis.Graphline import Graphline

import pprocess
import pygame
import Axon
import math
import time
from Axon.Ipc import producerFinished, shutdownMicroprocess
   
class Source(Axon.Component.component):
    ToSend = ["hello\n","hello\n","hello\n","hello\n"]
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
    Expect = ["hello\n","hello\n","hello\n","hello\n"]
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
#        while 1:
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
    
    if 0: # This stuff works
        Pipeline(
            Source(),
            Expecter(),
        ).run()

        testdata = [1,2,3,4,5]
        Pipeline(
            Source(ToSend=testdata),
            Expecter(Expect=testdata),
        ).run()

        testdata = [[1,2],[3,4],[5,6]]
        Pipeline(
            Source(ToSend=testdata),
            Expecter(Expect=testdata),
        ).run()

        testdata = [(1,2),(3,4), (5,6), (7,8)]
        Pipeline(
            Source(ToSend=testdata),
            Expecter(Expect=testdata),
        ).run()

        testdata = [{ (1,2):(3,4)} , {(5,6):(7,8)}]
        Pipeline(
            Source(ToSend=testdata),
            Expecter(Expect=testdata),
        ).run()

        testdata = [{ (1,2):(3,4)} , {(5,6):(7,8)}]
        Pipeline(
            Source(ToSend=testdata),
            Expecter(Expect=testdata),
        ).run()

    if 0: # Basic test of Source/Expecter
        ProcessPipeline( # Interestingly, fails, BUT the IPC message gets through!
            Source(),
            Expecter(),
        ).run()

    if 1: # Basic test of Source/Expecter
        testdata = ["there","once","was","a"]
        ProcessPipeline( # Interestingly, fails, BUT the IPC message gets through!
            Source(ToSend=testdata),
            Expecter(Expect=testdata),
        ).run()

    if 0:
        testdata = [ 1,2,3]
        ProcessPipeline( # Interestingly, fails, BUT the IPC message gets through!
            Source(ToSend=testdata),
            Expecter(Expect=testdata),
        )
