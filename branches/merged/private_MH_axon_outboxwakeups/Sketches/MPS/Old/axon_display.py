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
 # Thoughts for future:
 #
 # If we recieve a new digraph & component list, we should use
 # these to replace the existing one, and re-calculate the node
 # positions. Obviously, as things stand this isn't possible at
 # present, since this isn't integrated into Axon/etc, but it is a
 # likely future step.
 #
 # More immediate points:
 #   * Need a way of representing sub-components.
 #   * Need a way of integrating this into the system - and then
 #     acting as an introspection tool. (Not a huge deal, but needs
 #     doing)
 #   * Would be nice to allow nodes to be clickable.
 #   * Would be nice to allow editing via clicking
 #
 # Other:
 #   * If we do start integrating into a system, having a means of
 #     exporting (visual) snapshots of the running system would be
 #     very useful.
 #   * More intelligent node placement is desirable. The current
 #     approach is pretty dumb and based on a circle. Maybe this
 #     should change toa linear assumption unless linkages exist? 
 #     Dunno. (This sort of thing can be whole research projects in
 #     themselves - as things like graphviz show...)
#

import pygame
from pygame.locals import *
import random
import math
import time

donthogresource = True   
def slices(num):
   v = 360/float(num)
   x=0
   for i in xrange(num):
      yield int(i*v)

def radial_to_cartesian(angle, length=100, offset=(500,250)):
   x = math.cos(math.radians(angle))*length+offset[0]
   y = math.sin(math.radians(angle))*length+offset[1]
   return int(x),int(y)

class app:
   def __init__(self):
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
                   if donthogresource:
                      time.sleep(0.1)

   def box(self,size=(10,10),location=(100,100),colour=(127,127,127)):
         pygame.draw.rect(self.screen, colour, (location,size))

   def arrow(self,start, end,size=14):
      (sx,sy),(ex,ey) = start,end
      # The following calculations dealing with calculating the
      # position/size of the arrow heads
      lx = ex-sx
      ly = ey-sy
      lh = math.sqrt(lx**2 + ly**2)
      factor = lh/size
      mx,my = ex-(lx/factor),ey-(ly/factor)
      factor2 = lh/size
      nnlx = ly/factor2
      nnly = lx/factor2
      mmx1,mmy1 = mx+(nnlx/2),my-(nnly/2)
      mmx2,mmy2 = mx-(nnlx/2),my+(nnly/2)

      pygame.draw.line(self.screen, (224,10,10), start, end,2)
      pygame.draw.polygon(self.screen, (224,10,10), [
                          (ex,ey), (mmx1,mmy1), (mmx2,mmy2)])

   def init(self):
           background = self.Background()
           self.text("Hello There")

   def main(self):
      while 1:
         # This is where changes to the display can be made. For example:
         """
         colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
         location = (random.randint(0,1000),random.randint(0,500))
         size = (random.randint(0,(1000-location[0])),random.randint(0,(500-location[1])))
         self.box(size,location,colour)
         """
         # This needs to be a generator... (Note, this fits in neatly with
         # the component system. This is not exactly accidental!)
         yield 1

class myapp3(app):
   def __init__(self, parts, digraph):
      app.__init__(self)
      self.digraph = digraph
      self.parts = parts
      self.nodes = []

   def init(self):
      background = self.Background()

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

   def smoketest():
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
   smoketest = staticmethod(smoketest)

class myapp4(app):
   def __init__(self, component):
      app.__init__(self)
#      x = myapp4(component)
#      #  [ name, boxes, subcomponents, digraph]

#      wrapperinfo, parts, digraph = component
      self.component = component
      self.parts = component[2]
      self.digraph = component[3]
      self.nodes = []

   def init(self):
      background = self.Background()

   def draw_graph(self):
      for edge in self.digraph:
         if not edge[0] == edge[1]:
            try:
               self.arrow(self.node_pos[edge[0]], self.node_pos[edge[1]])
            except KeyError,k:
               print "DEPRECATION: Key Error", k

   def draw_nodes(self):
      for node in self.node_pos:
         stripped_name = node[node.find(".")+1:]
         self.text(stripped_name,location=self.node_pos[node],size=20)

   def draw_parts(self):
      brightblue = (10,10,240)
      for part in self.part_info:
         location,radius = self.part_info[part]
         self.text(part,location=location,size=28)
         pygame.draw.circle(self.screen,brightblue,location, radius,2)

   def makePart(self, component, radius,centre):
      print "COMPONENT", component
      print "\n"
      (partname, boxes, subparts, digraph) = component
      self.part_info[partname] = (centre,radius)
      numpoints = len(boxes)
      for j in xrange(numpoints):
         box = boxes[j]
         box_name = "%s.%s" % (partname,box)
         self.nodes.append(box_name )
         angle = (int(j * (360.0/numpoints)) +20) %360
         self.node_pos[box_name] = radial_to_cartesian(angle,radius,centre)
      if subparts is not None:
         num_parts = len(subparts)
         for i in xrange(num_parts):
            part = subparts[i]
            angle = int(i * (360.0/num_parts))
            part_centre = radial_to_cartesian(angle,int(radius/1.7))
            print "SUB", radius/3.7, part_centre, part
            self.makePart(part, int(radius/3.7),part_centre)

   def calculate_node_positions(self,radius,centre):
      self.node_pos = {}
      self.part_info = {}
      self.makePart(self.component, radius,centre)

   def main(self):
      self.calculate_node_positions(radius=220, centre=(500,250))
      while 1:
          self.draw_graph()
          self.draw_nodes()
          self.draw_parts()
          yield 1

   def smoketest():
      digraph1 = [
         ("system1._outbox","producer.inbox"),  
         ("producer.outbox","DCT.inbox"),
         ("producer.signal","DCT.control"),
         ("DCT.outbox","HUFF.inbox"),
         ("DCT.signal","HUFF.control"),
         ("HUFF.outbox","RLE.inbox"),  
         ("HUFF.signal","RLE.control"),   
         ("RLE.outbox","consumer.inbox"),
         ("RLE.signal","consumer.control"),
         ("consumer.signal","system1._control"),
         ("consumer.outbox","system1._inbox"),
      ]

      sp = ["sp",["inbox", "outbox", "signal","control"], None,None]
      sc = ["sc",["inbox", "outbox", "signal","control"], None,None]
      digraph2 = [
         ("sp.outbox","sc.inbox"),
         ("sp.signal","sc.control"),
         ("sp.signal","producer.control"),
      ]

      # name, boxes, subcomponents, digraph
      producer = ["producer",["inbox", "outbox", "signal","control"], [sp,sc],digraph2]
      transformer1 = ["DCT",["inbox", "outbox", "signal","control"], None,None]
      transformer2 = ["HUFF",["inbox", "outbox", "signal","control"], None,None]
      transformer3 = ["RLE",["inbox", "outbox", "signal","control"], None,None]
      consumer = ["consumer",["inbox", "outbox", "signal","control"],None,None]


      # The following list consists of the following structure:
      #  [ name, boxes, subcomponents, digraph]
      component1 =  ["system1", 
                     ["inbox", "outbox", "_inbox", "_outbox", "_control"],
                     [ producer, transformer1, transformer2, transformer3, consumer],
                     digraph1,
                    ]

      x = myapp4(component1)
      x._main()
   smoketest = staticmethod(smoketest)

if __name__ == '__main__':

   #myapp3.smoketest()
   myapp4.smoketest()
