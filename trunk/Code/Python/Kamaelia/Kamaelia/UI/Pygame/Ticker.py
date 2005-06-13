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

class Ticker(Axon.Component.component):
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
      self.outline_colour = argd.get("outline_colour", (128,232,128))
      self.outline_width = argd.get("outline_width", 1)
      self.render_area = pygame.Rect((argd.get("render_left",1),
                                      argd.get("render_top",1),
                                      argd.get("render_right",399),
                                      argd.get("render_bottom",299)))

   def waitBox(self,boxname):
      waiting = True
      while waiting:
         if self.dataReady(boxname): return
         else: yield 1

   def main(self):
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"signal"), displayservice)
      self.send({ "callback" : (self,"control"), "size": (400,300)}, "signal")
      for _ in self.waitBox("control"): yield 1
      display = self.recv("control")

      my_font = pygame.font.Font(None, self.text_height)
      initial_postition = (self.render_area.left,self.render_area.top)
      position = [ self.render_area.left, self.render_area.top ]

      display.fill(self.background_colour)
      pygame.draw.rect(display,
                       self.outline_colour,
                       ( self.render_area.left-self.outline_width,
                         self.render_area.top-self.outline_width,
                         self.render_area.width+self.outline_width,
                         self.render_area.height+self.outline_width),
                       self.outline_width)

      maxheight = 0
      while 1:
         if self.dataReady("inbox"):
            word = self.recv("inbox")
            word = " " + word
            wordsize = my_font.size(word)
            word_render= my_font.render(word, 1, self.text_colour)

            if position[0]+wordsize[0] > self.render_area.right:
               position[0] = initial_postition[0]
               if position[1] + (maxheight + self.line_spacing)*2 > self.render_area.bottom:
                  display.blit(display,
                               (self.render_area.left, self.render_area.top),
                               (self.render_area.left, self.render_area.top+self.text_height+self.line_spacing,
                                  self.render_area.width-1, position[1]-self.render_area.top ))
                  pygame.draw.rect(display, 
                                  self.background_colour, 
                                  (self.render_area.left, position[1], 
                                   self.render_area.width-1,self.render_area.top+self.render_area.height-1-(position[1])),
                                  0)
                  pygame.display.update()
               else:
                  position[1] += maxheight + self.line_spacing

            display.blit(word_render, position)
            position[0] += wordsize[0]
            if wordsize[1] > maxheight:
               maxheight = wordsize[1]

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



