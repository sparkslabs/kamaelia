#!/usr/bin/python

import pygame
import pygame.font
import time
from pygame.locals import *

from Axon.Scheduler import scheduler
from Axon.Component import component 
from Kamaelia.Util.PipelineComponent import pipeline
from SubtitleColourDecoderComponent import Colour

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


class datasource(component):
   def main(self):
      for x in text.split():
         self.send(x,"outbox")
         yield 1


class Ticker(component):

   def __init__(self, **argd):
      super(Ticker,self).__init__()
      #
      # Bunch of initial configs.
      #
      self.screen_width = argd.get("screen_width",800)
      self.screen_height = argd.get("screen_height",600)
      self.text_height = argd.get("text_height",39)
      self.line_spacing = argd.get("line_spacing", self.text_height/7)
      self.background_colour = argd.get("background_colour", (48,48,128))
      self.ticker_background_colour = argd.get("ticker_background_colour", (128,48,128))
      self.text_colour = argd.get("text_colour", (232, 232, 48))
      self.ticker_outline_colour = argd.get("ticker_outline_colour", (128,232,128))
      self.ticker_outline_width = argd.get("ticker_outline_width", 1)
      self.render_area = pygame.Rect((argd.get("render_left",50),
                                      argd.get("render_top",200),
                                      argd.get("render_right",700),
                                      argd.get("render_bottom",300)))
   def main(self):
      pygame.init()

      display = pygame.display.set_mode((self.screen_width, self.screen_height))#, FULLSCREEN )

      my_font = pygame.font.Font(None, self.text_height)

      initial_postition = (self.render_area.left,self.render_area.top)
      position = [ self.render_area.left, self.render_area.top ]

      display.fill(self.background_colour)
      pygame.draw.rect(display, 
                       self.ticker_outline_colour, 
                       ( self.render_area.left-self.ticker_outline_width,
                         self.render_area.top-self.ticker_outline_width,
                         self.render_area.width+self.ticker_outline_width,
                         self.render_area.height+self.ticker_outline_width),
                       self.ticker_outline_width)

      pygame.draw.rect(display, 
                      self.ticker_background_colour, 
                      (self.render_area.left, self.render_area.top, 
                          self.render_area.width-1,self.render_area.height-1),
                      0)

      pygame.display.update()
      maxheight = 0
      import sys
      while 1:
         for event in pygame.event.get():
            if event.type == KEYDOWN:
               if event.key == 113:
                  raise "Quitting Program"
         if self.dataReady("inbox"):
            word = self.recv("inbox")
            if isinstance(word, Colour):
               self.text_colour = word.getPygameColour()
            else:
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
                                     self.ticker_background_colour, 
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
         pygame.display.update()
         yield 1


if __name__ == "__main__":
   pipeline(datasource(),
                   Ticker()
           ).run()
