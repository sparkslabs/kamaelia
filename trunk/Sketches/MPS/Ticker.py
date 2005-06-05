#!/usr/bin/python

import pygame
import pygame.font
import time
from pygame.locals import *


def waitkey(timeout=0.025):
   t = time.time()
   while 1:
       for event in pygame.event.get():
          if event.type in (QUIT, KEYDOWN):
             return 
       if timeout and time.time()-t>timeout:
          return

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

def word_source():
   for x in text.split():
      yield x

#
# Bunch of initial configs.
#
screen_width = 800
screen_height = 600
text_height = 39
line_spacing = text_height/7
background_colour = (48,48,128)
ticker_background_colour = (128,48,128)
text_colour = (232, 232, 48)
ticker_outline_colour = (128,232,128)
ticker_outline_width = 1
render_area = pygame.Rect((50,201,700,300))

pygame.init()

display = pygame.display.set_mode((screen_width, screen_height))
my_font = pygame.font.Font(None, text_height)

initial_postition = (render_area.left,render_area.top)
position = [ render_area.left, render_area.top ]

display.fill(background_colour)
pygame.draw.rect(display, 
                 ticker_outline_colour, 
                 ( render_area.left-ticker_outline_width,
                   render_area.top-ticker_outline_width,
                   render_area.width+ticker_outline_width,
                   render_area.height+ticker_outline_width),
                 ticker_outline_width)

pygame.draw.rect(display, 
                ticker_background_colour, 
                (render_area.left, render_area.top, 
                    render_area.width-1,render_area.height-1),
                0)

pygame.display.update()
maxheight = 0
import sys
for word in word_source():
   word = " " + word
   wordsize = my_font.size(word)
   word_render= my_font.render(word, 1, text_colour)

   if position[0]+wordsize[0] > render_area.right:
      position[0] = initial_postition[0]
      if position[1] + (maxheight + line_spacing)*2 > render_area.bottom:
         display.blit(display, 
                      (render_area.left, render_area.top),
                      (render_area.left, render_area.top+text_height+line_spacing,
                         render_area.width-1, position[1]-render_area.top ))
         pygame.draw.rect(display, 
                         ticker_background_colour, 
                         (render_area.left, position[1], 
                            render_area.width-1,render_area.top+render_area.height-1-(position[1])),
                         0)
         pygame.display.update()
      else:
         position[1] += maxheight + line_spacing

   display.blit(word_render, position)
   pygame.display.update()
   waitkey()
   position[0] += wordsize[0]
   if wordsize[1] > maxheight:
      maxheight = wordsize[1]

waitkey(0)
