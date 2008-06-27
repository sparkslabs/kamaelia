#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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

"""\
===========================
Simple Pygame drawing board
===========================

A simple drawing board for the pygame display service.

Use your left mouse button to draw to the board and the
right to erase your artwork.

"""


import pprocess
import pygame
import Axon
import math
from Axon.Ipc import producerFinished
from Kamaelia.UI.PygameDisplay import PygameDisplay
class Paint(Axon.Component.component):
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
               "drawn"    : "Information on what was drawn on other Paint canvas"
             }
   Outboxes = { "outbox" : "Used to talk to other Paint canvas",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }
   
   def __init__(self, caption=None, position=None, margin=8, bgcolour = (124,124,124), fgcolour = (0,0,0), msg=None,
                transparent = False, size=(500,500), selectedColour=(0,0,0)):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Paint,self).__init__()

      self.backgroundColour = bgcolour
      self.foregroundColour = fgcolour
      self.margin = margin
      self.oldpos = None
      self.drawing = False
      self.tool = "Line"
      self.toolSize = 3
      self.size = size
      self.selectedColour = selectedColour
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
      
   def floodFill(self, x, y, newColour, oldColour):
       """Flood fill on a region of non-BORDER_COLOR pixels."""
       if (self.display.get_at((x,y)) == newColour):
           print "hergfhe"
           return
       edge = [(x, y)]
       self.display.set_at((x, y), newColour)
       while edge:
           newedge = []
           for (x, y) in edge:
               for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                   if (self.display.get_at((s,t)) == oldColour):
                       self.display.set_at((s, t), newColour)
                       newedge.append((s, t))
           edge = newedge
       self.blitToSurface()
   def addLayer(self):
      displayservice = PygameDisplay.getDisplayService()
    #  self.link((self,"display_signal"), displayservice)

      self.send( self.disprequest,
                  "display_signal")
      for _ in self.waitBox("callback"): yield 1
      self.display = self.recv("callback")
      self.drawBG()
      self.blitToSurface()
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
         if not self.anyReady():
             print "in this box"
             self.pause()
         yield 1
         while self.dataReady("control"):
            cmsg = self.recv("control")
            if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
               self.send(cmsg, "signal")
               done = True

         while self.dataReady("inbox"):
            for event in self.recv("inbox"):
                if isinstance(event, tuple):
                    if event[0] == "Tool":
                        self.tool = event[1]
                    if event[0] == "Size":
                        self.toolSize = event[1]
                    elif event[0] == 'circle':
                        pygame.draw.circle(self.display, (255,0,0), event[1], event[2], 0)
                        self.blitToSurface()
                    elif event[0] == 'line':
                        pygame.draw.line(self.display, (0,0,0), event[1], event[2], 3)
                        self.blitToSurface()
                    elif event[0] == 'colour':
                        self.selectedColour = event[1]
                    break
                if event == "clear":
                    print "YAY!"
                    self.oldpos = None
                    self.drawBG()
                    self.blitToSurface()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.tool == "Circle":
                        if event.button == 1:
                            self.oldpos = event.pos
                            self.drawing = True
                    if self.tool == "Line":
                        if event.button == 1:
                            self.drawing = True
                    if self.tool == "Bucket":
                        self.floodFill(event.pos[0],event.pos[1],self.selectedColour,self.display.get_at(event.pos))
                    if self.tool == "Eyedropper":
                        self.selectedColour = self.display.get_at(event.pos)
                    if event.button == 3:
                        self.addLayer()
                        #self.oldpos = None
                        #self.drawBG()
                        #self.blitToSurface()
                        #self.send(("clear",), "outbox")
                elif event.type == (pygame.KEYDOWN):
                    if event.key == pygame.K_c:
                       self.display.set_alpha = 0
                       self.tool = "Circle"
                    elif event.key == pygame.K_l:
                       self.tool = "Line"


                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.tool == "Circle":
                        rad = math.sqrt(((event.pos[0]-self.oldpos[0])**2)+((event.pos[1]-self.oldpos[1])**2))
                        pygame.draw.circle(self.display, self.selectedColour, self.oldpos, rad, 0)
                        circle = ("circle", self.oldpos, rad)
                        self.send((circle,), "outbox")
                        self.blitToSurface()
                    self.drawing = False
                    self.oldpos = None
                elif event.type == pygame.MOUSEMOTION:
                    if self.tool == "Line":
                        if self.drawing and self.innerRect.collidepoint(*event.pos):
                              if self.oldpos == None:
                                 self.oldpos = event.pos
                              else:
                                 pygame.draw.circle(self.display, self.selectedColour, self.oldpos, self.toolSize, 0)
                                # pygame.draw.line(self.display, self.selectedColour, self.oldpos, event.pos, self.toolSize)
                                 line = ("line", self.oldpos, event.pos)
                                 self.send((line,), "outbox")
                                 self.oldpos = event.pos
                              self.blitToSurface()
         self.pause()
         yield 1

   def blitToSurface(self):
       self.send({"REDRAW":True, "surface":self.display}, "display_signal")

__kamaelia_components__  = ( Paint, )


class DisplayConfig(Axon.Component.component):
    width = 800
    height = 480
    def main(self):
        pgd = PygameDisplay( width=self.width, height=self.height ).activate()
        PygameDisplay.setDisplayService(pgd)
        yield 1
    

                  
if __name__ == "__main__":
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   from pygame.locals import *
   from XYPad import XYPad
   from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
   from Kamaelia.UI.Pygame.Button import Button
   import sys; sys.path.append("../../../MPS/pprocess/");
   from Axon.experimental.Process import ProcessGraphline
   from Kamaelia.Chassis.Graphline import Graphline
   from Kamaelia.Chassis.Pipeline import Pipeline


   ProcessGraphline(
        COLOURS = Pipeline(
                      DisplayConfig(width=270),
                      XYPad(size=(255, 255), bouncingPuck = False, position = (10, 200),
                           bgcolour=(0, 0, 0), fgcolour=(255, 255, 255), colourSelector = True),
                  ),
        WINDOW1 = Pipeline(
                      DisplayConfig(width=520, height=520),
                      Paint(bgcolour=(100,100,172),position=(10,10), size = (500,500), transparent = True),
                  ),
        linkages = {
            ("COLOURS", "outbox") : ("WINDOW1", "inbox"),
        }
   ).run()
# Licensed to the BBC under a Contributor Agreement: THF/DK
