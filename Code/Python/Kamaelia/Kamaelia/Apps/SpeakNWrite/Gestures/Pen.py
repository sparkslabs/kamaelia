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

# Pygame based pen, drives a Sketcher canvas

import pygame
from Axon.Component import component


class Pen(component):
    
    Inboxes =  { "inbox"   : "For receiving PygameDisplay events",
                 "control" : "",
               }
    Outboxes = { "outbox" : "outputs drawing instructions",
                 "signal" : "",
                 "points" : "(x,y) pairs"
               }
    
    def __init__(self, bgcolour=(255,255,255)):
        super(Pen,self).__init__()
        self.sendbuffer = []
        self.bgcolour = bgcolour     
    
    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
    
    
    def main(self):
        """Main loop"""
        
        yield 1
        r,g,b = 128,128,128
        dragging = False
        mode="LINE"        
        
        while not self.finished():
        
            while self.dataReady("inbox"):
                message = self.recv("inbox")
                for data in message:
                    if data.type == pygame.MOUSEBUTTONDOWN:
                        if data.button==1:
                            self.sendbuffer.append( ["CLEAR"]+[str(x) for x in self.bgcolour] )
                            oldpos = data.pos
                            dragging = True
                    elif data.type == pygame.MOUSEMOTION and dragging:
                        self.sendbuffer.append( ["CIRCLE", "224","224","224",str(data.pos[0]),str(data.pos[1]),"1"] )
                        self.send( (data.pos[0], data.pos[1]), "points")
                        oldpos = data.pos
                    elif data.type == pygame.MOUSEBUTTONUP and dragging:
                        self.sendbuffer.append( ["CIRCLE", "224","224","224",str(data.pos[0]),str(data.pos[1]),"1"] )
                        self.send( (data.pos[0], data.pos[1]), "points")
                        self.send( "ENDSTROKE", "points")
                        oldpos = data.pos
                        dragging = False
            self.flushbuffer()
            self.pause()
            yield 1


    def flushbuffer(self):
        if len(self.sendbuffer):
            self.send(self.sendbuffer[:], "outbox")
            self.sendbuffer = []

