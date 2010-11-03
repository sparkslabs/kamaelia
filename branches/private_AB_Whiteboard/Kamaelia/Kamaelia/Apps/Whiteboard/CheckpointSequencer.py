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
    
    def __init__(self, rev_access_callback = None,
                       rev_checkpoint_callback = None,
                       blank_slate_callback = None,
                       initial = 1,
                       last = 1):
        super(CheckpointSequencer, self).__init__()
        if rev_access_callback: self.loadMessage = rev_access_callback
        if rev_checkpoint_callback: self.saveMessage = rev_checkpoint_callback
        if blank_slate_callback: self.newMessage = blank_slate_callback
        self.initial = initial
        self.last = last


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
        self.send( self.loadMessage(current), "outbox")
        dirty = False
        while self.shutdown():
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                if command == "delete":
                    if current == last and last > 1:
                        # go to previous slide
                        dirty = False
                        command = "prev"
                        last -= 1
                    elif current < last and current != 1:
                        # go to previous slide and fix numbering
                        dirty = False
                        command = "prev"
                        last -= 1
                    
                #if command == "save": # MOVEME!!!!! - What does this even do? Commented out, appears pointless given that current remains unchanged
                    #self.send( self.saveMessage(current), "outbox")
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
                if command == "first":
                    if dirty:
                        dirty = False
                    current = 1
                    self.send( self.loadMessage(current), "outbox")        
                    last = 0
                    for x in os.listdir(self.notepad):
                        if os.path.splitext(x)[1] == ".png":
                            last += 1
                    if last < 1:
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
                if command == "delete":
                    if current == 1 and current < last:
                        # fix numbering then reload current slide
                        last -= 1
                        #command = "next"
                        self.send( self.loadMessage(current+1), "outbox")
                    self.send(["delete",current],"toDecks")

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





































