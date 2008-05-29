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
from Axon.Ipc import producerFinished, shutdownMicroprocess
   
class Source(Axon.Component.component):
    ToSend = ["hello"]
    def main(self):
        tosend = self.ToSend[:]
        while len(tosend) > 0:
            print "sending"
            self.send( tosend.pop(0), "outbox")
            yield 1
        self.send(producerFinished(), "signal")
        print "sent"
        yield 1

class Expecter(Axon.Component.component):
    Expect = ["hello"]
    def main(self):
        got = []
        print "recieving"
#        self.shuttingdown = False
#        while not self.shutdown():
        while 1:
            while self.dataReady("inbox"):
                D = self.recv("inbox")
                print ".", D
                got.append(D)
            yield 1

        if self.Expect == got: # Only works for basic types (lists, tuples, strings, etc)
            print "DATA RECIEVED INTACT", got
        else:
            print "DATA MANGLED", got
        self.send( self.control_message, "signal") # Pass on

    def shutdown(self):
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

    if 1:
        testdata = [ 1,2,3]
        ProcessPipeline( # Interestingly, fails, BUT the IPC message gets through!
            Source(ToSend=testdata),
            Expecter(Expect=testdata),
        )
