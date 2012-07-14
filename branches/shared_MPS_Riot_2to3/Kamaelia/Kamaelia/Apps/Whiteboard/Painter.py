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
#

import Axon
import pygame
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Painter(Axon.Component.component):
    """\
    Painter() -> new Painter component.
    """

    Inboxes =  { "inbox"   : "For receiving PygameDisplay events",
                 "control" : "",
                 "colour"  : "select drawing, using colour",
                 "erase"   : "select eraser",
                 "load"    : "image to load",
                 "save"    : "filename to save image to",
               }
    Outboxes = { "outbox" : "outputs drawing instructions",
                 "signal" : "",
               }

    def __init__(self):
        super(Painter,self).__init__()
        self.sendbuffer = []


    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1


    def main(self):
        """Main loop"""

        yield 1
        r,g,b = 0,0,0
        dragging = False
        mode="LINE"

        while self.shutdown():

            while self.dataReady("colour"):
                r,g,b = self.recv("colour")
                mode = "LINE"

            while self.dataReady("erase"):
                self.recv("erase")
                mode = "ERASE"

            while self.dataReady("load"):
                command = self.recv("load")
                self.sendbuffer.append(command)

            while self.dataReady("save"):
                command = self.recv("save")
                self.sendbuffer.append(command)

            while self.dataReady("inbox"):
                message = self.recv("inbox")
                for data in message:
                    if data.type == pygame.MOUSEBUTTONDOWN:
                        if data.button==1:
                            oldpos = data.pos
                            dragging = True
                        elif data.button==3:
                            pygame.display.toggle_fullscreen() ### XXX WART
                    elif data.type == pygame.MOUSEMOTION and dragging:
                        self.cmd(mode, oldpos, data.pos, r, g, b)
                        oldpos = data.pos
                    elif data.type == pygame.MOUSEBUTTONUP and dragging:
                        self.cmd(mode, oldpos, data.pos, r, g, b)
                        oldpos = data.pos
                        dragging = False
            self.flushbuffer()
            self.pause()
            yield 1

    def cmd(self, mode, oldpos, newpos, r, g, b):
        if mode=="LINE":
            self.sendbuffer.append( ["LINE", str(r),str(g),str(b), str(oldpos[0]), str(oldpos[1]), str(newpos[0]), str(newpos[1])] )

        elif mode=="ERASE":
            self.sendbuffer.append( ["CIRCLE", "255","255","255", str(newpos[0]), str(newpos[1]), "8"])

    def flushbuffer(self):
        if len(self.sendbuffer):
            self.send(self.sendbuffer[:], "outbox")
            self.sendbuffer = []
