#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
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
    def main(self):
        self.start = time.time()
        tosend = self.ToSend[:]
        while len(tosend) > 0:
            print "Source:- sending"
            self.send( tosend.pop(0), "outbox")
            yield 1
        self.send(producerFinished(), "signal")
        print "Source:- sent"
        time.sleep(1)
        yield 1

class Expecter(Axon.Component.component):
    Expect = ["hello\n","hello\n","hello\n","hello\n"]
    delay = 2
    def main(self):
        self.start = time.time()
        got = []
        print "Expecter:- recieving"
        self.shuttingdown = False
        self.count = 0
        while not self.shutdown():
#        while 1:
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
        testdata = ["hello","hello","hello","hello"]
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
