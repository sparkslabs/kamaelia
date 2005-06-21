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
      self.orig = self.rect[:]
      self.centre = argd["centre"]
      self.scale = argd["scale"]
      self.collided = False
      self.id = count
      count = count + 1

def xfloat_range(min, max, steps):
    intermediate = steps -1
    for i in xrange(intermediate):
       yield min + i*((max-min)/float(intermediate))
    yield max

def x_range(min, max, steps):
    for x in xfloat_range(min, max, steps):
       yield int(x)


class Ticker(Axon.Component.component):
   def __init__(self, **argd):
      super(Ticker,self).__init__()
      #
      # Bunch of initial configs.
      #
      self.display = None
      self.display_height = 700
      self.display_width = 900

   def waitBox(self,boxname):
      waiting = True
      while waiting:
         if self.dataReady(boxname): return
         else: yield 1

   def requestDisplay(self, size=(400,300), fullscreen=0):
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"signal"), displayservice)
      self.send({ "DISPLAYREQUEST" : True,
                  "callback" : (self,"control"),
                  "size": size,
                  "fullscreen" : fullscreen,
                  "scaling" : 1.0},
                  "signal")

   def randomRectangle(self, mwidth, mheight,minx,miny,maxwidth, maxheight):
      
      if mwidth - minx < maxwidth: maxwdith = mwidth - minx
      if mheight - miny < maxheight: maxheight = mheight - miny
      
      left = random.randint(minx, mwidth-minx)
      top = random.randint(miny, mheight-miny)
      width = random.randint(int(maxwidth*0.75), maxwidth)
      height = random.randint(int(maxheight*0.25), maxheight)

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

   def getOffsetRescale(self, rectangles):
       minleft = 0
       maxright = 0
       mintop = 0
       maxbottom = 0
       for rectangle in rectangles:
          if minleft > rectangle.rect.left: minleft = rectangle.rect.left
          if maxright < rectangle.rect.right: maxright = rectangle.rect.right
          if mintop > rectangle.rect.top: mintop = rectangle.rect.top
          if maxbottom < rectangle.rect.bottom: maxbottom = rectangle.rect.bottom
          
       width = maxright-minleft
       height = maxbottom-mintop
       scale = 1
       try:
          horiz_scale = self.display_width/float(width)
          vert_scale = self.display_height/float(height)
          scale = horiz_scale
          if scale > vert_scale: scale = vert_scale
          if scale > 1: scale = 1
       except ZeroDivisionError:
          scale = 1.0

       return (minleft, mintop), scale

   def renderRectangles(self, rectangles,rescale = False):
       self.display.fill((255,255,255))
       if rescale:   
          offset, scale = self.getOffsetRescale(rectangles)
       else:
          offset, scale = (0,0), 1.0
       
       for rectangle in rectangles:
           self.renderRectangle(rectangle,offset,scale)

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
      self.requestDisplay(size=(self.display_width, self.display_height),
                          fullscreen=1)
      for _ in self.waitBox("control"): yield 1
      self.display = self.recv("control")

      while True:
         rectangles = []

         while len(rectangles)<20:
            add = self.randomRectangle(700,500,20,20,300,300)
            rectangles.append(add)
            self.renderRectangles(rectangles)
            yield 1

         yield 1
         while self.overlappingRectangles(rectangles):
            rectangles = self.spreadRectangles(rectangles)

         offset, scale = self.getOffsetRescale(rectangles)
         for frame in self.renderAnimatedRectangles(rectangles, offset, scale):
            time.sleep(0.01)
            yield 1

         self.renderRectangles(rectangles,rescale=True)
         my_font = pygame.font.Font(None, 48)
         word_render= my_font.render("ALL DONE", 1, (48,48,224))
                     
         self.display.blit(word_render, (200,200))
         yield 1
         yield 1
         time.sleep(3)
 

   def renderAnimatedRectangles(self, rectangles, offset, scale, steps = 25):
      animators = []
      for i in xrange(len(rectangles)):
        r = rectangles[i]
        animators.append(self.animateRectangle(r, offset, scale, steps))

      for i in xrange(steps):
        self.display.fill((255,255,255))
        for A in animators:
           abcd = A.next()
           pygame.draw.rect(self.display,
                      (240,64,64),
                      abcd,
                      2)
        yield 1
        
   def animateRectangle(self,r, offset, scale, steps):
        o_left = r.orig[0]
        left = r.rect[0] - offset[0]
        o_top = r.orig[1]
        top = r.rect[1] - offset[1]
        xchange = iter(x_range(o_left, left, steps))
        ychange = iter(x_range(o_top, top, steps))
        scale_change = iter(xfloat_range(1.0, scale, steps))
        for i in xrange(steps):
           x = xchange.next()
           y = ychange.next()
           s = scale_change.next()
           a,b,c,d = [ z * s for z in x, y, r.rect.width, r.rect.height ]
           yield a,b,c,d

if __name__ == "__main__":

   Ticker().run()

