#!/usr/bin/python
#
# Toy/Sketch using pygame to automatically create a visualisation of an Axon
# type system. Written semi-test first. (Each iteration is slightly more
# sophisticated than the last as you step through below)
#
# This would probably want rationalisation before any actual use in a real
# system, but it's a useful first stab - if only because it really is a
# first stab at an automated visualisation of data that can be extracted
# automatically from Axon. Next steps with this would be to model not just
# multiple components but nested components. (How this would be visualised of
# course is a different matter)
#

import pygame
from pygame.locals import *
import random
import time
   
class app:
   def __init__(self):
           import time
           # Initialise screen
           pygame.init()
           self.screen = pygame.display.set_mode((1000, 500))
           pygame.display.set_caption('Basic Pygame program')

   def text(self,text, location=None,size=36,colour=(10,10,10)):
           # Display some text
           font = pygame.font.Font(None, size)
           text = font.render(text, 1, (10, 10, 10))
           if location is None:
              textpos = text.get_rect()
              textpos.centerx = self.background.get_rect().centerx
           else:
              
              location = location[0]-text.get_rect().width/2, location[1]-text.get_rect().height/2
              textpos = location
           self.screen.blit(text, textpos)
#           self.background.blit(text, textpos)

   def Background(self,colour=(250,250,250)):
           # Fill background
           self.background = pygame.Surface(self.screen.get_size())
           self.background = self.background.convert()
           self.background.fill(colour)
           return self.background

   def _main(self):
           self.init()
           # Blit everything to the screen
           self.screen.blit(self.background, (0, 0))
           pygame.display.flip()
           g = self.main()
           # Event loop
           while 1:
                   g.next()
                   for event in pygame.event.get():
                           if event.type == QUIT:
                                   return

                   pygame.display.flip()
                   time.sleep(0.1)
   def box(self,size=(10,10),location=(100,100),colour=(127,127,127)):
         pygame.draw.rect(self.screen, colour, (location,size))

   def init(self):
           background = self.Background()
           self.text("Hello There")

   def main(self):
      while 1:
         colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
         location = (random.randint(0,1000),random.randint(0,500))
         size = (random.randint(0,(1000-location[0])),random.randint(0,(500-location[1])))
         self.box(size,location,colour)
         yield 1

def slices(num):
   v = 360/float(num)
   x=0
   for i in xrange(num):
      yield int(i*v)

import math

def radial_to_cartesian(angle, length=100, offset=(500,250)):
   x = math.cos(math.radians(angle))*length+offset[0]
   y = math.sin(math.radians(angle))*length+offset[1]
   return int(x),int(y)

class myapp(app):
   def __init__(self, digraph):
      app.__init__(self)
      self.digraph = digraph

   def init(self):
      background = self.Background()
   def main(self):
      numpoints = 5
      delta = 1
      while 1:
          points = []
          for i in slices(numpoints):
             points.append(radial_to_cartesian(i))
          for point in points:
             pygame.draw.line(self.screen, (10,10,10), (500,250),  [x+18 for x in point])
             self.text("a",location=point)
#             self.box(location=point)
          yield 1
          self.Background()
          self.screen.blit(self.background, (0, 0))
          numpoints = numpoints + delta
          if numpoints > 10 or numpoints < 5:
             delta = delta * -1

class myapp2(app):
   def __init__(self, digraph):
      app.__init__(self)
      self.digraph = digraph
      ephemeral = {}
      for s,e in self.digraph:
         ephemeral[s] = None
         ephemeral[e] = None
      self.nodes = ephemeral.keys()
      self.nodes.sort()

   def init(self):
      background = self.Background()
   def main(self):
      node_pos = {}
      numpoints = len(self.nodes)
      for i in xrange(numpoints):
         angle = int(i * (360.0/numpoints))
         node_pos[self.nodes[i]] = radial_to_cartesian(angle)
         
      while 1:
          for node in node_pos:
             self.text(node,location=node_pos[node])
          for edge in self.digraph:
             pygame.draw.line(self.screen, (10,10,10), node_pos[edge[0]], node_pos[edge[1]])

          yield 1
#          self.Background()
#          self.screen.blit(self.background, (0, 0))

def myapp2_test():
   digraph = [
      ("a","b"),
      ("b","c"),
      ("c","d"),
      ("d","e"),
      ("e","a"),
      ("a","c"),
      ("a","d"),
   ]
   x = myapp2(digraph)
   x._main()

class myapp3(app):
   def __init__(self, parts, digraph):
      app.__init__(self)
      self.digraph = digraph
      self.parts = parts
      self.nodes = []

   def init(self):
      background = self.Background()

   def arrow(self,start, end):
      for d in [-3,-2,-1,0,1,2,3]:
         x = start[0]+d
         y = start[1]+d
         pygame.draw.line(self.screen, (224,10,10), (x,y), end)

   def draw_graph(self):
      for edge in self.digraph:
         if not edge[0] == edge[1]:
            self.arrow(self.node_pos[edge[0]], self.node_pos[edge[1]])

   def draw_nodes(self):
      for node in self.node_pos:
         stripped_name = node[node.find(".")+1:]
         self.text(stripped_name,location=self.node_pos[node],size=20)

   def draw_parts(self):
      for part in self.part_info:
         location,radius = self.part_info[part]
         self.text(part,location=location,size=28)
         pygame.draw.circle(self.screen,(10,10,240),location, radius,2)

   def calculate_node_positions(self):
      self.node_pos = {}
      self.part_info = {}
      num_parts = len(self.parts)
      for i in xrange(num_parts):
         part = self.parts[i]
         shape = part[0]
         del part[0]
         angle = int(i * (360.0/num_parts))
         part_centre = radial_to_cartesian(angle,130)
         self.part_info[shape] = (part_centre,60)
         numpoints = len(part)
         for j in xrange(len(part)):
            node = part[j]
            node_name = "%s.%s" % (shape,node)
            self.nodes.append(node_name )
            angle = (int(j * (360.0/numpoints)) +20) %360
            self.node_pos[node_name] = radial_to_cartesian(angle,60,part_centre)

   def main(self):
      self.calculate_node_positions()
      while 1:
          self.draw_graph()
          self.draw_nodes()
          self.draw_parts()
          yield 1

if __name__ == '__main__': 

   def myapp3_test():
      producer = ["producer", "inbox", "outbox", "signal","control"]
      transformer1 = ["DCT", "inbox", "outbox", "signal","control"]
      transformer2 = ["HUFF", "inbox", "outbox", "signal","control"]
      transformer3 = ["RLE", "inbox", "outbox", "signal","control"]
      consumer = ["consumer","inbox", "outbox", "signal","control"]

      digraph1 = [
         ("producer.outbox","DCT.inbox"),
         ("producer.signal","DCT.control"),
         ("DCT.outbox","HUFF.inbox"),
         ("DCT.signal","HUFF.control"),
         ("HUFF.outbox","RLE.inbox"),  
         ("HUFF.signal","RLE.control"),   
         ("RLE.outbox","consumer.inbox"),
         ("RLE.signal","consumer.control"),
      ]
      x = myapp3([producer,transformer1,transformer2,transformer3,consumer], digraph1)
      x._main()

   myapp3_test()
