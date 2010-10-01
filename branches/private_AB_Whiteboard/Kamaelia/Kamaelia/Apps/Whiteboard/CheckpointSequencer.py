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
    def __init__(self, rev_access_callback = None,
                       rev_checkpoint_callback = None,
                       blank_slate_callback = None,
                       initial = 1,
                       highest = 1,
                       notepad = "Scribbles"):
        super(CheckpointSequencer, self).__init__()
        if rev_access_callback: self.loadMessage = rev_access_callback
        if rev_checkpoint_callback: self.saveMessage = rev_checkpoint_callback
        if blank_slate_callback: self.newMessage = blank_slate_callback
        self.initial = initial
        self.highest = highest
        self.notepad = notepad


    def loadMessage(self, current): return current
    def saveMessage(self, current): return current
    def newMessage(self, current): return current
    
    def fixNumbering(self):
        exists = 1
        slides = os.listdir(self.notepad)
        slides.sort()
        for x in slides:
            if x == "slide." + str(exists) + ".png":
                # This slide exists, skip to next one
                pass
            else:
                # This slide doesn't exist, find the next one up and copy it down
                try:
                    shutil.move(self.notepad + "/" + x,self.notepad + "/slide." + str(exists) + ".png")
                except Exception, e:
                    print("Failed to renumber slides. There may be an error in the sequence")
            exists += 1

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False

    def main(self):
        current = self.initial
        highest = self.highest
        self.send( self.loadMessage(current), "outbox")
        dirty = False
        while not self.finished():
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                if command == "delete":
                    try:
                        os.remove(self.notepad + "/slide." + str(current) + ".png")
                    except Exception, e:
                        pass
                    
                    if current == highest and highest > 1:
                        # go to previous slide
                        dirty = False
                        command = "prev"
                        highest -= 1
                        self.fixNumbering()
                    elif current < highest and current != 1:
                        # go to previous slide and fix numbering
                        dirty = False
                        command = "prev"
                        highest -= 1
                        self.fixNumbering()
                    elif current == 1 and current < highest:
                        # fix numbering then reload current slide
                        highest -= 1
                        self.fixNumbering()
                        self.send( self.loadMessage(current), "outbox")
                    else:
                        # Do nothing
                        pass
                if command == "save":
                    self.send( self.saveMessage(current), "outbox")
                if command == "prev":
                    if current >1:
                        if dirty:
                            self.send( self.saveMessage(current), "outbox")
                            dirty = False
                        current -= 1
                        self.send( self.loadMessage(current), "outbox")
                if command == "next":
                    if current <highest:
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
                    highest = 0
                    for x in os.listdir(self.notepad):
                        if os.path.splitext(x)[1] == ".png":
                            highest += 1
                    if highest < 1:
                        highest = 1
                if command == "checkpoint":
                    if current == highest:
                        self.send( self.saveMessage(current), "outbox")
                        highest += 1
                        current = highest
                    else:
                        highest += 1
                        current = highest
                        self.send( self.saveMessage(current), "outbox")
                        highest += 1
                        current = highest
                if command == "new":
                    self.send( self.saveMessage(current), "outbox")
                    highest += 1
                    current = highest
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
                    if current <highest:
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
                            highest=0,
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
                            highest=0,
                           ),
        ConsoleEchoer(),
    ).run()





































