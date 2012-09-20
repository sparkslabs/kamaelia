#!/usr/bin/python
# -*- coding: utf-8 -*-

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


import Axon
import os
import shutil
from Axon.Ipc import producerFinished, shutdownMicroprocess

class CheckpointSequencer(Axon.Component.component):
    Inboxes = {
        "inbox" : "Receives slide navigation instructions",
        "control" : "",
    }
    Outboxes = {
        "outbox" : "Sends canvas slide loading instructions",
        "signal" : "",
        "toDecks" : "Sends messages relating to slide deletions", # Can't be moved to decks component as it needs to know the current slide number
    }
    
    def __init__(self, rev_init_callback = None,
		       rev_access_callback = None,
                       rev_checkpoint_callback = None,
                       blank_slate_callback = None,
                       initial = 1,
                       last = 1):
        super(CheckpointSequencer, self).__init__()
        if rev_init_callback: self.initMessage = rev_init_callback
        if rev_access_callback: self.loadMessage = rev_access_callback
        if rev_checkpoint_callback: self.saveMessage = rev_checkpoint_callback
        if blank_slate_callback: self.newMessage = blank_slate_callback
        self.initial = initial
        self.last = last

    def initMessage(self, current): return current
    def loadMessage(self, current): return current
    def saveMessage(self, current): return current
    def newMessage(self, current): return current

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def main(self):
        current = self.initial
        last = self.last
        self.send( self.initMessage(current), "outbox")
        dirty = False
        loadsafe = False
        while self.shutdown():
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                if isinstance(command,list):
                    if command[0] == "first":
                        last = command[1]
                    command = command[0]
                if command == "first":
                    current = 1
                    self.send( self.loadMessage(current), "outbox")
                if command == "delete":
                    if (current == last and last > 1) or (current < last and current != 1):
                        # go to previous slide
                        dirty = False
                        command = "prev"
                        last -= 1
                        self.send(["delete",current],"toDecks")
                    elif current == 1 and current < last:
                        # fix numbering then reload current slide
                        last -= 1
                        #command = "next"
                        loadsafe = True
                        self.send(["delete",current],"toDecks")
                    elif current == 1:
                        self.send("clearscribbles", "toDecks")
                # The below command is ONLY used when slide 1 has been deleted and the 'new' slide 1 replacing is has to be loaded
                # Whilst not ideal, this avoids a possible race condition following the sending to two messages to two different components
                if command == "loadsafe":
                   if loadsafe == True:
                        self.send( self.loadMessage(current), "outbox")
                        loadsafe = False
                if command == "prev":
                    if current >1:
                        if dirty:
                            self.send( self.saveMessage(current), "outbox")
                            dirty = False
                        current -= 1
                        self.send( self.loadMessage(current), "outbox")
                if command == "next":
                    if current <last:
                        if dirty:
                            self.send( self.saveMessage(current), "outbox")
                            dirty = False
                        current += 1
                        self.send( self.loadMessage(current), "outbox")
                if command == "reset":
                    # Used when a deck has been closed to reset counters
                    if dirty:
                        dirty = False
                    current = 1
                    self.send( self.loadMessage(current), "outbox")        
                    last = 1
                if command == "checkpoint":
                    if current == last:
                        self.send( self.saveMessage(current), "outbox")
                        last += 1
                        current = last
                    else:
                        last += 1
                        current = last
                        self.send( self.saveMessage(current), "outbox")
                        last += 1
                        current = last
                if command == "new":
                    self.send( self.saveMessage(current), "outbox")
                    last += 1
                    current = last
                    self.send( self.newMessage(current), "outbox")
                    self.send( self.saveMessage(current), "outbox")
                if command == "undo":
                    self.send( self.loadMessage(current), "outbox")
                if command == "dirty":
#                    print "OK, got dirty message"
                    dirty = True
#                    self.send( self.loadMessage(current), "outbox")

                if command == ("prev", "local"):
                    if current >1:
                        if dirty:
                            self.send( self.saveMessage(current), "outbox")
                            dirty = False
                        current -= 1
                        mess = self.loadMessage(current)
                        mess[0].append("nopropogate")
                        self.send( mess, "outbox")

                if command == ("next", "local"):
                    if current <last:
                        if dirty:
                            self.send( self.saveMessage(current), "outbox")
                            dirty = False
                        current += 1
                        mess = self.loadMessage(current)
                        mess[0].append("nopropogate")
                        self.send( mess, "outbox")
#                        self.send( self.loadMessage(current), "outbox")

            if not self.anyReady():
                self.pause()
                yield 1

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    def loadMessage(current): return [["LOAD", "slide.%d.png" % (current,)]]
    def saveMessage(current): return [["SAVE", "slide.%d.png" % (current,)]]

    Pipeline(
        ConsoleReader(">>>", ""),
        CheckpointSequencer(lambda X: [["LOAD", "slide.%d.png" % (X,)]],
                            lambda X: [["SAVE", "slide.%d.png" % (X,)]],
                            initial=0,
                            last=0,
                           ),
        ConsoleEchoer(),
    ).run()



if __name__ == "__OLDmain__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    def loadMessage(current): return [["LOAD", "slide.%d.png" % (current,)]]
    def saveMessage(current): return [["SAVE", "slide.%d.png" % (current,)]]

    Pipeline(
        ConsoleReader(">>>", ""),
        CheckpointSequencer(lambda X: [["LOAD", "slide.%d.png" % (X,)]],
                            lambda X: [["SAVE", "slide.%d.png" % (X,)]],
                            initial=0,
                            last=0,
                           ),
        ConsoleEchoer(),
    ).run()





































