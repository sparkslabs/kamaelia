#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import time
import os
import Axon
import math
from ps_gfxcursor import GfxCursor
from Axon.Ipc import producerFinished, WaitComplete
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.UI.Pygame.Text import TextDisplayer
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.Util.Clock import CheapAndCheerfulClock as Clock
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
               "drawn"    : "Information on what was drawn on other Paint canvas",
               "newframe" : "Input pulses from the clock, to mark new frames in animations"
             }
   Outboxes = { "outbox" : "Used to talk to other Paint canvas",
                "laynum" : "Used to show the Active Layer number on the text displayer",
                "clock"  : "Used to stop the clock",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface" }

   def __init__(self, caption=None, position=None, margin=8, bgcolour = (124,124,124), fgcolour = (0,0,0), msg=None,
                transparent = False, size=(500,500), selectedColour=(0,0,0), activeLayer = None, animator = False):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Paint,self).__init__()

      self.backgroundColour = bgcolour
      self.foregroundColour = fgcolour
      self.activeLayer = activeLayer
      self.activeLayIn = 0
      self.margin = margin
      self.oldpos = None
      self.animator = animator
      self.drawing = False
      self.currentFrame = None
      self.tool = "Line"
      self.toolSize = 3
      self.layers = []
      self.brushes = [] # TEST PURPOSES
      self.activeBrush = None # TEST PURPOSES
      self.size = size
      self.selectedColour = selectedColour
      self.innerRect = pygame.Rect(10, 10, self.size[0]-20, self.size[1]-20)
      self.playing = False
      
      self.testingBrush = False
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
      self.layer = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "events" : (self, "inbox"),
                           "size": self.size,
                           "transparency" : self.backgroundColour }
      self.brush = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "events" : (self, "inbox"),
                           "size": (self.toolSize,self.toolSize),
                           "transparency" : self.backgroundColour }


      if not position is None:
        self.disprequest["position"] = position
        self.layer["position"] = position

   def waitBox(self,boxname):
      """Generator. yields 1 until data ready on the named inbox."""
      waiting = True
      while waiting:
        if self.dataReady(boxname): return
        else: yield 1


   def animate(self):
       FPS = 2
       clock = Clock(float(1)/FPS).activate()
       clock.link((clock, "outbox"), (self, "newframe"))
       for x in self.layers:
           if not self.dataReady("newframe"):
               self.pause()
           self.recv("newframe")
           print "now"

   def drawBG(self, bg = False):
      """Fills the currentlayer with a background, if it's the bg layer it also gives a border."""
      if bg == True:
         self.activeLayer.fill( (255,0,0) )
         self.activeLayer.fill( self.backgroundColour, self.innerRect )
      else: self.activeLayer.fill( self.backgroundColour )

   def floodFill(self, x, y, newColour, oldColour):
       """Flood fill on a region of non-BORDER_COLOR pixels."""
       #print "colour here = ",self.activeLayer.get_at((x,y))[0]
       #print "newColour = ",newColour[0]
       if (self.activeLayer.get_at((x,y))[0] == newColour[0] and self.activeLayer.get_at((x,y))[1] == newColour[1] and self.activeLayer.get_at((x,y))[2] == newColour[2]):
           return
       edge = [(x, y)]
       self.activeLayer.set_at((x, y), newColour)
       while edge:
           newedge = []
           for (x, y) in edge:
               for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                   if (self.activeLayer.get_at((s,t)) == oldColour):
                       self.activeLayer.set_at((s, t), newColour)
                       newedge.append((s, t))
           edge = newedge
       self.blitToSurface()

   def addLayer(self):
       """Sends a request for a new surface, using the layer details. ie. returns transparent surface of the bg size"""
       self.send( self.layer, "display_signal")
       if not self.dataReady('callback'):
           self.pause()
           yield 1
       x = self.recv("callback")
       self.layers.append(x)
       
   def addBrush(self):
       """Sends a request for a new surface, using the brush details. ie. returns transparent surface, of the toolSize"""
       self.send( self.brush, "display_signal")
       if not self.dataReady('callback'):
           self.pause()
           yield 1
       x = self.recv("callback")
       self.brushes.append(x)
       
   def save(self, filename):
       """Merges all the layers (by bliting them all to the background) and
        saves as a jpg, note this requires pygame 1.8 otherwise will save a bmp."""
       print "here"
       self.activeLayIn = 0
       self.activeLayer = self.layers[self.activeLayIn]
       self.send( self.activeLayIn, "laynum" )
       for x in self.layers:
           self.activeLayer.blit( x, (0,0) )
       if float(pygame.version.ver[0:3])>=1.8: #checking pygame version number
           filename = filename+'.JPG'
       else: filename = filename+'.BMP'
       pygame.image.save(self.activeLayer, filename)


   def main(self):
      """Main event loop, also handles input from other components"""
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"display_signal"), displayservice)

      self.send( self.disprequest,"display_signal")

      for _ in self.waitBox("callback"): yield 1
      self.display = self.recv("callback")
      self.layers.append(self.display)

  #    f = os.path.join('', "pennyarcade.gif")
  #    x = pygame.image.load(f)
  #    colorkey = x.get_at((0, 0))
  #    if colorkey is True:
  #        x.set_colorkey(colorkey, pygame.RLEACCEL)
  #    self.layers.append(x)
  #    self.display = x
  #    self.activeLayIn = len(self.layers)-1
  #    self.activeLayer = self.layers[self.activeLayIn]
  #    self.display.blit( x, (0,0) )
      

      layerDisp = TextDisplayer(size = (20, 20),position = (520,10)).activate()
      self.link( (self,"laynum"), (layerDisp,"inbox") )
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
      self.activeLayer = self.layers[self.activeLayIn]
      self.send( self.activeLayIn, "laynum" )
      image = pygame.Surface((20, 20))
      pygame.draw.circle(image, (1, 1, 1), (10, 10), self.toolSize, 0)
     # pygame.draw.circle(image, self.selectedColour, (10, 10), 8, 2)
      image.set_at((9, 9), (255,255,255))
      image.set_colorkey(0, pygame.RLEACCEL)
      cursor = GfxCursor(self.display, image, (10, 10))

      self.drawBG(True)
      self.blitToSurface()
      FPS = 1
      clock = Clock(float(1)/FPS).activate()
      clock.link((clock, "outbox"), (self, "newframe"))


      done = False
      while not done:
         dirtyrects = []
         dirtyrects.extend([cursor.hide()])
         if not self.anyReady():
             self.pause()
         yield 1
         while self.dataReady("control"):
            cmsg = self.recv("control")
            if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
               self.send(cmsg, "signal")
               done = True
         while self.dataReady("newframe") and self.playing:
             self.recv("newframe")
             if self.currentFrame != 0:
                self.layers[self.currentFrame].set_alpha(0)
             self.currentFrame = self.currentFrame + 1
             if self.currentFrame == len(self.layers)-1:
                 self.playing = False
             self.layers[self.currentFrame].set_alpha(255)
             self.blitToSurface()

         while self.dataReady("inbox"):
            for event in self.recv("inbox"):
                if isinstance(event, tuple):
                    self.send((event,),"outbox")
                    if event[0] == "Layer":
                        if event[1] == "Add":
                            yield WaitComplete( self.addLayer() )
                            self.activeLayIn = len(self.layers)-1
                            self.activeLayer = self.layers[self.activeLayIn]
                            self.drawBG()
                            if self.animator and len(self.layers)-2 >= 1:
                                for x in self.layers:
                                    s.set_alpha = 0
                                self.activeLayer.blit(self.layers[len(self.layers)-2],(0,0))
                            self.blitToSurface()
                        elif event[1] == "Delete":
                            self.send( producerFinished(message=self.activeLayer),"display_signal")
                            self.layers.remove(self.activeLayer)
                            self.activeLayIn = 0
                            self.activeLayer = self.layers[self.activeLayIn]
                          #  print self.layers
                        if event[1] == "Next":
                            if self.animator and self.activeLayIn != 0:
                            	self.activeLayer.set_alpha(0)
                            if self.activeLayIn == len(self.layers)-1:
                                self.activeLayIn = 0
                                self.activeLayer = self.layers[self.activeLayIn]
                            else:
                                self.activeLayIn += 1
                                self.activeLayer = self.layers[self.activeLayIn]
                            if self.animator:
                            	self.activeLayer.set_alpha(255)
                        elif event[1] == "Prev":
                            if self.animator and self.activeLayIn != 0:
                            	self.activeLayer.set_alpha(0)
                            if self.activeLayIn == 0:
                                self.activeLayIn = len(self.layers)-1
                                self.activeLayer = self.layers[self.activeLayIn]
                            else:
                                self.activeLayIn -= 1
                                self.activeLayer = self.layers[self.activeLayIn]
                            if self.animator:
                            	self.activeLayer.set_alpha(255)
                        self.send( self.activeLayIn, "laynum" )
                    elif event[0] == "Tool":
                        self.tool = event[1]
                    elif event[0] == "Size":
                        self.toolSize = event[1]/3
                        pygame.draw.circle(image, self.selectedColour, (10, 10), self.toolSize/3, 0)
                        image.set_at((9, 9), (255,255,255))
                        image.set_colorkey(0, pygame.RLEACCEL)
                        cursor = GfxCursor(self.display, image, (10, 10))
                    elif event[0] == "Alpha":
                        self.layers[self.activeLayIn].set_alpha(event[1])
                        self.blitToSurface()
                      #  print self.activeLayer.get_alpha()
                    elif event[0] == 'Colour':
                        self.selectedColour = event[1]
                        pygame.draw.circle(image, self.selectedColour, (10, 10), self.toolSize/3, 0)
                        image.set_at((9, 9), (255,255,255))
                        image.set_colorkey(0, pygame.RLEACCEL)
                        cursor = GfxCursor(self.display, image, (10, 10))
                    elif event[0] == 'Save':
                        self.save(event[1])
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cursor.disable()
                    if self.tool == "Circle":
                        if event.button == 1:
                            self.oldpos = event.pos
                            self.drawing = True
                    if self.tool == "Eraser":
                        self.selectedColour = self.backgroundColour
                        self.tool = "Line"
                    if self.tool == "Line":
                        if event.button == 1:
                            self.drawing = True
                    if self.tool == "Bucket":
                        self.floodFill(event.pos[0],event.pos[1],self.selectedColour,self.activeLayer.get_at(event.pos))
                    if self.tool == "Eyedropper":
                        self.selectedColour = self.activeLayer.get_at(event.pos)
                    if event.button == 3:
                        self.addLayer()
                        #self.oldpos = None
                        #self.drawBG()
                        #self.blitToSurface()
                        #self.send(("clear",), "outbox")
                elif event.type == (pygame.KEYDOWN):
                    if event.key == pygame.K_c:
                        image = pygame.image.load(os.path.join('', 'pennyarcade.gif'))
                        yield WaitComplete( self.addLayer() )
                        self.activeLayIn = len(self.layers)-1
                        self.activeLayer = self.layers[self.activeLayIn]
                        self.drawBG()
                        self.activeLayer.blit( image, (10,10) )
                        self.blitToSurface()
                        self.send( self.activeLayIn, "laynum" )
                    elif event.key == pygame.K_s:
                        """Testing a different brushing technique, bliting a brush"""
                        print self.size, self.toolSize
                        yield WaitComplete( self.addBrush() )
                        self.activeBrush = self.brushes[len(self.brushes)-1]
                        self.activeBrush.fill( self.backgroundColour )
                        pygame.draw.circle(self.activeBrush, self.selectedColour, (self.toolSize/2,self.toolSize/2), self.toolSize, 0)
                    elif event.key == pygame.K_a:
                        self.animator = True
                    elif event.key == pygame.K_l:
                        self.layers[1].blit( self.layers[1], (100,100) )
               #         temp = self.layers[1]
               #         self.layers[1].fill(self.backgroundColour)
               #         self.layers[1].blit( temp, (100,100) )
                    elif event.key == pygame.K_o:
                        for x in self.layers:
                            x.set_alpha(0)
                        self.layers[0].set_alpha(255)
                        self.currentFrame = 0
                        while self.dataReady("newframe"): # empty if there's anything there
                            self.recv("newframe")
                        self.playing = True
                        self.blitToSurface()



                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    cursor.enable()
                    if self.tool == "Circle":
                        rad = int(math.sqrt(((event.pos[0]-self.oldpos[0])**2)+((event.pos[1]-self.oldpos[1])**2)))
                        pygame.draw.circle(self.activeLayer, self.selectedColour, self.oldpos, rad, 0)
                        circle = ("circle", self.oldpos, rad)
                     #   self.send((circle,), "outbox")
                        self.blitToSurface()
                    self.drawing = False
                    self.oldpos = None
                elif event.type == pygame.MOUSEMOTION:
                    cursor.update(event)
                    if self.tool == "Line":
                        if self.drawing and self.innerRect.collidepoint(*event.pos):
                              if self.oldpos == None:
                                 self.oldpos = event.pos
                              else:
                                # pygame.draw.circle(self.activeLayer, self.selectedColour, self.oldpos, self.toolSize, 0)
                                 r = pygame.draw.line(self.activeLayer, self.selectedColour, self.oldpos, event.pos, self.toolSize)
                                 dirtyrects.append(r)
                               #  self.activeLayer.blit(self.activeBrush, event.pos) FAILED TECHNIQUE
                                 line = ("line", self.oldpos, event.pos)
                                 self.send((line,), "outbox")
                                 self.oldpos = event.pos
                    self.blitToSurface()
         self.pause()
         pygame.time.delay(5)
         dirtyrects.extend([cursor.show()])
         pygame.display.update(dirtyrects)
         yield 1

   def blitToSurface(self):
       """Refreshes the activelayer"""
       self.send({"REDRAW":True, "surface":self.activeLayer}, "display_signal")

__kamaelia_components__  = ( Paint, )


class DisplayConfig(Axon.Component.component):
    width = 800
    height = 480
    def main(self):
        pgd = PygameDisplay( width=self.width, height=self.height ).activate()
        PygameDisplay.setDisplayService(pgd)
        yield 1



if __name__ == "__main__":
   from pygame.locals import *
   from ToolBox import ToolBox
   from Axon.experimental.Process import ProcessGraphline
   from Kamaelia.Chassis.Graphline import Graphline
   from Kamaelia.Chassis.Pipeline import Pipeline
   from Kamaelia.Chassis.Seq import Seq

   ProcessGraphline(
       COLOURS = Seq(
            DisplayConfig(width=285, height=600),
            ToolBox(size=(270, 600)),
            ),

       WINDOW1 = Seq(
                 DisplayConfig(width=555, height=520),
                 Paint(bgcolour=(100,100,172),position=(10,10), size = (500,500), transparent = False),
                  ),
       WINDOW2 = Seq(
                 DisplayConfig(width=555, height=520),
                 Paint(bgcolour=(100,100,172),position=(10,10), size = (500,500), transparent = False),
                  ),
        linkages = {
            ("COLOURS", "outbox") : ("WINDOW1", "inbox"),
            ("WINDOW1", "outbox") : ("WINDOW2", "inbox"),
        }
   ).run()
# Licensed to the BBC under a Contributor Agreement: THF/DK
