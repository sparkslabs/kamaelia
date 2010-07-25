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
#
# Magna Doodle Application Logic - which is a bunch of IShards and Shards
# which are only really usable in this project
#

#
# This is where we will put shards that come from *inside* the main method
# and inside __init__
#

def __INIT__(self):
    self.backgroundColour = argd.get("bgcolour", (124,124,124))
    self.foregroundColour = argd.get("fgcolour", (0,0,0))
    self.margin = argd.get("margin", 8)
    self.oldpos = None
    self.drawing = False

    self.size = argd.get("size", (200,200))
    self.innerRect = pygame.Rect(10, 10, self.size[0]-20, self.size[1]-20)

    if argd.get("msg", None) is None:
        argd["msg"] = ("CLICK", self.id)
    self.eventMsg = argd.get("msg", None)
    if argd.get("transparent",False):
        transparency = argd.get("bgcolour", (124,124,124))
    else:
        transparency = None
    self.disprequest = { "DISPLAYREQUEST" : True,
                         "callback" : (self,"callback"),
                         "events" : (self, "inbox"),
                         "size": self.size,
                         "transparency" : transparency }

    if not argd.get("position", None) is None:
        self.disprequest["position"] = argd.get("position",None)

def SetEventOptions(self):
    self.addListenEvent("MOUSEBUTTONDOWN")
    self.addListenEvent("MOUSEBUTTONUP")
    self.addListenEvent("MOUSEMOTION")

def MOUSEBUTTONDOWN_handler(self):
    #print 'down'
    if  event.button == 1:
        self.drawing = True
    elif event.button == 3:
        self.oldpos = None
        self.drawBG()
        self.blitToSurface()

def MOUSEBUTTONUP_handler(self):
    #print 'up'
    if event.button == 1:
        self.drawing = False
        self.oldpos = None

def MOUSEMOTION_handler(self):
    #print 'move'
    if self.drawing and self.innerRect.collidepoint(*event.pos):
        if self.oldpos == None:
            self.oldpos = event.pos
        else:
            pygame.draw.line(self.display, (0,0,0), self.oldpos, event.pos, 3)
            self.oldpos = event.pos
        self.blitToSurface()

#
# Non-Reusable SHARD NOT ISHARD
#
def drawBG(self):
    self.display.fill( (255,0,0) )
    self.display.fill( self.backgroundColour, self.innerRect )

