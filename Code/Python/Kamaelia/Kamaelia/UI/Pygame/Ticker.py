#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#

import pygame
import Axon
from Kamaelia.UI.PygameDisplay import PygameDisplay
from Axon.Ipc import WaitComplete
import time

class Ticker(Axon.Component.component):
   Inboxes = { "inbox"    : "Specify (new) filename",
               "control"  : "",
               "alphacontrol" : "The alpha transparency of the image is controlled here. It expects  a value 0..255",
             }

   def __init__(self, **argd):
      super(Ticker,self).__init__()
      #
      # Bunch of initial configs.
      #
      self.text_height = argd.get("text_height",39)
      self.line_spacing = argd.get("line_spacing", self.text_height/7)
      self.background_colour = argd.get("background_colour", (48,48,128))
      self.background_colour = argd.get("background_colour", (128,48,128))
      self.text_colour = argd.get("text_colour", (232, 232, 48))
      self.outline_colour = argd.get("outline_colour", self.background_colour)
      self.outline_width = argd.get("outline_width", 1)
      self.position = argd.get("position",(1,1))
      self.left = argd.get("render_left",1)
      self.render_area = pygame.Rect((argd.get("render_left",1),
                                      argd.get("render_top",1),
                                      argd.get("render_right",399),
                                      argd.get("render_bottom",299)))
      self.words_per_second = 8
      self.delay = 1.0/self.words_per_second

   def waitBox(self,boxname):
      waiting = True
      while waiting:
         if self.dataReady(boxname): return
         else: yield 1

   def clearDisplay(self):
       self.display.fill(self.background_colour)
       self.renderBorder(self.display)
            
   def renderBorder(self, display):
      pygame.draw.rect(display,
                       self.outline_colour,
                       ( self.render_area.left-self.outline_width,
                         self.render_area.top-self.outline_width,
                         self.render_area.width+self.outline_width,
                         self.render_area.height+self.outline_width),
                       self.outline_width)
   

   def requestDisplay(self, **argd):
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"signal"), displayservice)
      self.send(argd, "signal")
      for _ in self.waitBox("control"): yield 1
      display = self.recv("control")
      self.display = display


   def handleAlpha(self):
       if self.dataReady("alphacontrol"):
            alpha = self.recv("alphacontrol")
            self.display.set_alpha(alpha)

   def main(self):
    yield WaitComplete(
          self.requestDisplay(DISPLAYREQUEST=True,
                              callback = (self,"control"),
# SMELL                              transparency = (128,48,128),
                            size = (self.render_area.width, self.render_area.height),
                            position = self.position
                            )
    ) 
    display = self.display

    my_font = pygame.font.Font(None, self.text_height)
    initial_postition = (self.render_area.left,self.render_area.top)
    position = [ self.render_area.left, self.render_area.top ]

    self.clearDisplay()

    maxheight = 0
    last=time.time()
    blankcount = 0
    alpha = -1
    while 1:
       self.handleAlpha()
#       if self.dataReady("alphacontrol"):
#            alpha = self.recv("alphacontrol")
#            print "BOING", alpha
#            self.display.set_alpha(alpha)
       if self.dataReady("control"):
          if self.dataReady("control"):
              data = self.recv("control")
              if isinstance(data, Axon.Ipc.producerFinished):
                  self.send(Axon.Ipc.producerFinished(message=display), "signal") # pass on the shutdown
                  return
       if self.dataReady("inbox"):
          word = self.recv("inbox")
          if word =="\n":
             word = ""
          if "\n" in word:
             lines = word.split("\n")[:-1]
             word = "BONG"
          else:
             lines = [word]
          c = len(lines)
          for line in lines:
              word = line
              words = line.split()
              if len(words) == 0:
                  if blankcount:
                      blankcount = 0
                      self.send( {"CHANGEDISPLAYGEO": True,
                                  "surface" : self.display,
                                  "position":(108,60)
                                 },
                                "signal")
                  else:
                      blankcount = 1
              for word in words:
                  while time.time() - last < self.delay:
                     self.handleAlpha()                     
                     yield 1
                  self.handleAlpha()
#                  if self.dataReady("alphacontrol"):
#                        alpha = self.recv("alphacontrol")
#                        print "BOING", alpha
#                        self.display.set_alpha(alpha)
                  if self.dataReady("control"): ### VOMIT : code duplication
                      if self.dataReady("control"):
                          data = self.recv("control")
                          if isinstance(data, Axon.Ipc.producerFinished):
                               self.send(Axon.Ipc.producerFinished(message=display), "signal") # pass on the shutdown
                               return
                  last = time.time()
                  word = " " + word
                  
                  alpha = self.display.get_alpha()
                  self.display.set_alpha(255)
                  wordsize = my_font.size(word)
                  word_render= my_font.render(word, 1, self.text_colour)

                  if position[0]+wordsize[0] > self.render_area.right or c > 1:
                     position[0] = initial_postition[0]
                     if position[1] + (maxheight + self.line_spacing)*2 > self.render_area.bottom:
                        display.set_colorkey(None)
                        display.blit(display,
                                     (self.render_area.left, self.render_area.top),
                                     (self.render_area.left, self.render_area.top+self.text_height+self.line_spacing,
                                      self.render_area.width-1, position[1]-self.render_area.top ))

                        pygame.draw.rect(display, 
                                        self.background_colour, 
                                        (self.render_area.left, position[1], 
                                         self.render_area.width-1,self.render_area.top+self.render_area.height-1-(position[1])),
                                        0)
                        # pygame.display.update()
                        if c>1:
                           c = c -1
                     else:
                        position[1] += maxheight + self.line_spacing

                  display.blit(word_render, position)
                  position[0] += wordsize[0]
                  if wordsize[1] > maxheight:
                     maxheight = wordsize[1]
                  self.display.set_alpha(alpha)
       yield 1


if __name__ == "__main__":
   from Kamaelia.Util.PipelineComponent import pipeline
   # Excerpt from Tennyson's Ulysses
   text = """\
The lights begin to twinkle from the rocks;
The long day wanes; the slow moon climbs; the deep
Moans round with many voices.  Come, my friends.
'T is not too late to seek a newer world.
Push off, and sitting well in order smite
The sounding furrows; for my purpose holds
To sail beyond the sunset, and the baths
Of all the western stars, until I die.
It may be that the gulfs will wash us down;
It may be we shall touch the Happy Isles,
And see the great Achilles, whom we knew.
Tho' much is taken, much abides; and tho'
We are not now that strength which in old days
Moved earth and heaven, that which we are, we are,--
One equal temper of heroic hearts,
Made weak by time and fate, but strong in will
To strive, to seek, to find, and not to yield.
"""
   class datasource(Axon.Component.component):
      def main(self):
         for x in text.split():
            self.send(x,"outbox")
            yield 1


   for _ in range(6):
      pipeline(datasource(),
                      Ticker()
              ).activate()

   Axon.Scheduler.scheduler.run.runThreads()



