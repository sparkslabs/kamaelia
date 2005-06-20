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
from Kamaelia.Physics.Simple.SpatialIndexer import SpatialIndexer

import random
import time

count = 0
class myRectangle(object):
   def __init__(self, **argd):
      global count
      self.rect = argd["rect"]
      self.centre = argd["centre"]
      self.scale = argd["scale"]
      self.collided = False
      self.id = count
      count = count + 1


class Ticker(Axon.Component.component):
   def __init__(self, **argd):
      super(Ticker,self).__init__()
      #
      # Bunch of initial configs.
      #
      self.display = None

   def waitBox(self,boxname):
      waiting = True
      while waiting:
         if self.dataReady(boxname): return
         else: yield 1

   def requestDisplay(self, size=(400,300)):
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"signal"), displayservice)
      self.send({ "DISPLAYREQUEST" : True,
                  "callback" : (self,"control"),
                  "size": size,
                  "scaling" : 1.0},
                  "signal")

   def randomRectangle(self, mwidth, mheight,minx,miny,maxwidth, maxheight):
      
      if mwidth - minx < maxwidth: maxwdith = mwidth - minx
      if mheight - miny < maxheight: maxheight = mheight - miny
      
      left = random.randint(minx, mwidth-minx)
      top = random.randint(miny, mheight-miny)
      width = random.randint(int(maxwidth*0.75), maxwidth)
      height = random.randint(int(maxheight*0.25), maxheight)

      print "WIDTH, HEIGHT", width,height
      centre = left+width/2, top+height/2
      scale = 1.0

      return myRectangle(**{ "rect" : pygame.Rect(left, top, width, height), 
               "centre" : centre, 
               "scale" : scale })

   def renderRectangle(self, rectangle, offset, scale):
       left, top, width, height = rectangle.rect
       left = left - offset[0]
       top = top - offset[1]
       left, top, width, height = [ X*scale for X in (left, top, width, height) ]

       pygame.draw.rect(self.display,
                    (64,64,64),
                    (left, top, width, height),
                    2)
       pygame.draw.line(self.display, 
                    (64,64,64), 
                    (left, top), 
                    (left+width, top+height), 
                    2)
       pygame.draw.line(self.display, 
                    (64,64,64), 
                    (left, top+height),
                    (left+width, top),
                    2)

   def renderRectangles(self, rectangles,rescale = False):
       self.display.fill((255,255,255))
       minleft = 0
       maxright = 0
       mintop = 0
       maxbottom = 0
       for rectangle in rectangles:
          if minleft > rectangle.rect.left: minleft = rectangle.rect.left
          if maxright < rectangle.rect.right: maxright = rectangle.rect.right
          if mintop > rectangle.rect.top: mintop = rectangle.rect.top
          if maxbottom < rectangle.rect.bottom: maxbottom = rectangle.rect.bottom
          
#       print "MAX BORDER", minleft, mintop, maxright, maxbottom
       width = maxright-minleft
       height = maxbottom-mintop
#       print "WIDTH, HEIGHT", width, height
       scale = 1
       try:
          horiz_scale = 950/float(width)
          vert_scale = 700/float(height)
#          print "SCALE HORIZ", horiz_scale
#          print "SCALE VERT", vert_scale
          scale = horiz_scale
          if scale > vert_scale: scale = vert_scale
          if scale > 1: scale = 1
#          print "SCALE", scale
       except ZeroDivisionError:
          scale = 1.0
       if not rescale:
          scale = 1.0
          
       for rectangle in rectangles:
           self.renderRectangle(rectangle,(minleft,mintop),scale)

   def overlappingRectangles(self,rects):
      result = False
      for rect in rects :
         rect.collided = (rect.rect.collidelist([ x.rect for x in rects if x is not rect ]) != -1)
         if rect.collided:
            result = True
      return result


   def dx(self, x, y): return x[0]-y[0]
   def dy(self, x, y): return x[1]-y[1]
   def ds(self, x,y):  return self.dx(x, y)**2 + self.dy(x, y)**2

   def spreadRectangles(self,rectangles):
      result = []
      for r in rectangles:
         if r.collided:
               P = []
               for s in rectangles:
                  if s is r: continue
                  sum_square_of_distances = self.ds(r.centre, s.centre)
                  distance_X = self.dx(r.centre,s.centre)
                  distance_Y = self.dy(r.centre,s.centre)
                  
                  stepX = distance_X * 0.05
                  stepY = distance_Y * 0.05
                  P.append( (sum_square_of_distances, s.id, stepX, stepY) )

               P.sort()
               dx,dy = 0,0
               for x_,y_ in [(float(P[0][0])/X[0]*X[2],float(P[0][0])/X[0]*X[3]) for X in P ]:
                  dx,dy = dx+x_ , dy+y_
               r.centre = r.centre[0] + dx, r.centre[1] + dy
               r.rect.left = r.rect.left + dx
               r.rect.top = r.rect.top + dy
         result.append(r)
      return result

   def main(self):
      self.requestDisplay(size=(950,700))
      for _ in self.waitBox("control"): yield 1
      self.display = self.recv("control")
      rectangles = []

      while len(rectangles)<20:
         add = self.randomRectangle(700,500,20,20,300,300)
         rectangles.append(add)
         self.renderRectangles(rectangles)
         yield 1

      time.sleep(3)

      while self.overlappingRectangles(rectangles):
         time.sleep(0.01)
         rectangles = self.spreadRectangles(rectangles)
         self.renderRectangles(rectangles,rescale=True)
         yield 1

      my_font = pygame.font.Font(None, 48)
      word_render= my_font.render("ALL DONE", 1, (48,48,224))
                  
      self.display.blit(word_render, (200,200))
            

if __name__ == "__main__":

   Ticker().run()

