#!/usr/bin/python
#
# USAGE OF THIS IS DEPRECATED SINCE THIS CAN NOW BE USED IN THE MAIN CODE
# TREE
#
#
import pygame
import pygame.font
import time
from pygame.locals import *

from Axon.Scheduler import scheduler
from Axon.Component import component 
from Kamaelia.Util.PipelineComponent import pipeline
from SubtitleColourDecoderComponent import Colour


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
      self.screen_width = argd.get("screen_width",1024)
      self.screen_height = argd.get("screen_height",768)
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

      display = pygame.display.set_mode((self.screen_width, self.screen_height), FULLSCREEN )

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

      overlay = pygame.Surface((500,300))
#      overlay.set_colorkey((255,255,255))
      word_render= my_font.render("Testing, testing", 1, (0,0,0))
      overlay.fill((255,255,255))
      overlay.blit(word_render, (10,10))
      overlay.set_alpha(10)
      overlay = overlay.convert_alpha()
      C = 0
      while 1:
         C = C+1
         if C == 21: C=20
         display.blit(overlay, (50+C,50+C))
         for event in pygame.event.get():
            if event.type == KEYDOWN:
               if event.key == 113:
                  raise "Quitting Program"
         pygame.display.update()
         yield 1


if __name__ == "__main__":
   Ticker().run()
