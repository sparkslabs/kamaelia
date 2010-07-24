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

"""\
===========================
Simple Pygame drawing board
===========================

A simple drawing board for the pygame display service.

Use your left mouse button to draw to the board and the
right to erase your artwork.

"""
import sys; sys.path.append("../MPS/pprocess/");
from Axon.experimental.Process import ProcessPipeline
from Axon.experimental.Process import ProcessGraphline
from Kamaelia.Chassis.Graphline import Graphline

import pprocess
import pygame
import Axon
import math
from Axon.Ipc import producerFinished
from Kamaelia.UI.PygameDisplay import PygameDisplay

class MagnaDoodle(Axon.Component.component):
   """\
   MagnaDoodle(...) -> A new MagnaDoodle component.

   A simple drawing board for the pygame display service.

   (this component and its documentation is heaviliy based on Kamaelia.UI.Pygame.Button)

   Keyword arguments:
   
   - position     -- (x,y) position of top left corner in pixels
   - margin       -- pixels margin between caption and button edge (default=8)
   - bgcolour     -- (r,g,b) fill colour (default=(224,224,224))
   - fgcolour     -- (r,g,b) text colour (default=(0,0,0))
   - transparent  -- draw background transparent if True (default=False)
   - size         -- None or (w,h) in pixels (default=None)
   
   """
   
   Inboxes = { "inbox"    : "Receive events from PygameDisplay",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from PygameDisplay",
               "drawn"    : "Information on what was drawn on other MagnaDoodles"
             }
   Outboxes = { "outbox" : "Used to talk to other MagnaDoodles",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }
   
   def __init__(self, caption=None, position=None, margin=8, bgcolour = (124,124,124), fgcolour = (0,0,0), msg=None,
                transparent = False, size=(200,200)):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(MagnaDoodle,self).__init__()
      
      self.backgroundColour = bgcolour
      self.foregroundColour = fgcolour
      self.margin = margin
      self.oldpos = None
      self.drawing = False
      self.shape = "line"
###      print "KEY",key
      
      self.size = size
      self.innerRect = pygame.Rect(10, 10, self.size[0]-20, self.size[1]-20)

      if msg is None:
         msg = ("CLICK", self.id)
      self.eventMsg = msg
      if transparent:
         transparency = bgcolour
      else:
         transparency = None
      self.disprequest = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "events" : (self, "inbox"),
                           "size": self.size,
                           "transparency" : transparency }
      
      if not position is None:
        self.disprequest["position"] = position

       
   def waitBox(self,boxname):
      """Generator. yields 1 until data ready on the named inbox."""
      waiting = True
      while waiting:
        if self.dataReady(boxname): return
        else: yield 1
   
   def drawBG(self):
      self.display.fill( (255,0,0) )
      self.display.fill( self.backgroundColour, self.innerRect )
     
   
   def main(self):
      """Main loop."""
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"display_signal"), displayservice)

      self.send( self.disprequest,
                  "display_signal")
             
      for _ in self.waitBox("callback"): yield 1
      self.display = self.recv("callback")
      self.drawBG()
      self.blitToSurface()
      
      self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                  "surface" : self.display},
                  "display_signal")

      self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONUP,
                  "surface" : self.display},
                  "display_signal")

      self.send({ "ADDLISTENEVENT" : pygame.MOUSEMOTION,
                  "surface" : self.display},
                  "display_signal")
		  
      self.send({ "ADDLISTENEVENT" : pygame.KEYDOWN,
		  "surface" : self.display},
		  "display_signal")


      done = False
      while not done:
         while self.dataReady("control"):
            cmsg = self.recv("control")
            if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
               self.send(cmsg, "signal")
               done = True
         while self.dataReady("drawn"):
                print "drawn"
                for x in self.recv("drawn"):
                    if x == "c":
                        self.oldpos = None
                        self.drawBG()
                        self.blitToSurface()
         while self.dataReady("inbox"):
            for event in self.recv("inbox"):
  #              print event
                if isinstance(event, tuple):
#                    print "here"
                    if event[0] == 'circle':
                        pygame.draw.circle(self.display, (255,0,0), event[1], event[2], 0)
                        self.blitToSurface()
                    if event[0] == 'line':
                        pygame.draw.line(self.display, (0,0,0), event[1], event[2], 3)
                        self.blitToSurface()
                    break
                if event == "clear":
                    print "YAY!"
                    self.oldpos = None
                    self.drawBG()
                    self.blitToSurface()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
     #               self.send(event, "outbox")
                    if self.shape == "circle":
                        if event.button == 1:
                            self.oldpos = event.pos
                #            print event.pos
                            self.drawing = True
                     #       self.send(event, "outbox")
                    if self.shape == "line":
                        if event.button == 1:
                            self.drawing = True
                    if event.button == 3:
                        self.oldpos = None
                        self.drawBG()
                        self.blitToSurface()
                        self.send(("clear",), "outbox")
                        print "I'm here!"
                elif event.type == (pygame.KEYDOWN):
                    if event.key == pygame.K_c:
                       self.shape = "circle"
                    elif event.key == pygame.K_l:
                       self.shape = "line"


                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.shape == "circle":
                        rad = math.sqrt(((event.pos[0]-self.oldpos[0])**2)+((event.pos[1]-self.oldpos[1])**2))
          #              print event.pos
          #              print rad
                        pygame.draw.circle(self.display, (0,0,0), self.oldpos, rad, 0)
                        circle = ("circle", self.oldpos, rad)
                        self.send((circle,), "outbox")
                        self.blitToSurface()
                    self.drawing = False
                    self.oldpos = None
                elif event.type == pygame.MOUSEMOTION:
#                   print "BUTTON", event.button
                    if self.shape == "line":
                        if self.drawing and self.innerRect.collidepoint(*event.pos):
                              if self.oldpos == None:
                                 self.oldpos = event.pos
                              else:
                                 pygame.draw.line(self.display, (0,0,0), self.oldpos, event.pos, 3)
                                 line = ("line", self.oldpos, event.pos)
                                 self.send((line,), "outbox")
                                 self.oldpos = event.pos
                              self.blitToSurface()
         self.pause()
         yield 1
            
      
   def blitToSurface(self):
       self.send({"REDRAW":True, "surface":self.display}, "display_signal")

__kamaelia_components__  = ( MagnaDoodle, )

                  
if __name__ == "__main__":
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   from pygame.locals import *
   
  # Magna = MagnaDoodle().activate()
   ProcessGraphline(
        WINDOW1 = MagnaDoodle(bgcolour=(100,100,172),position=(0,0) ),
        WINDOW2 = MagnaDoodle(bgcolour=(172,100,100),position=(0,0) ),
        linkages = {
            ("WINDOW1", "outbox") : ("WINDOW2", "inbox")
         #   ("WINDOW1", "outbox") : ("WINDOW2", "drawn")
        },
        __debug = True,
   ).run()
   
  # Axon.Scheduler.scheduler.run.runThreads()  
# Licensed to the BBC under a Contributor Agreement: THF/DK
