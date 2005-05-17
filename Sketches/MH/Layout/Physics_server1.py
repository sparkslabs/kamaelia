#!/usr/bin/env python

# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

# first test of Physics module

import pygame
from pygame.locals import *

from random import randrange
import random
import time

from Axon.Scheduler import scheduler as _scheduler
import Axon as _Axon

import Physics
from PyGameApp import PyGameApp, DragHandler


component = _Axon.Component.component

class Particle(Physics.Particle):
    """Version of Physics.Particle with added rendering functions,
    and a list of particles it is bonded to."""

    def __init__(self, position, ID, pname, radius):
        super(Particle,self).__init__(position, 0, (0.0, 0.0), ID )
        self.radius = radius
        self.bondedTo = []
        self.labelText = pname
        
        font = pygame.font.Font(None, 24)
        self.label = font.render(self.labelText, False, (0,0,0))
        
    def getBonded(self):
        return self.bondedTo
        
    def renderBonds(self, surface):
        """Renders lines representing the bonds going from this particle"""
        for p in self.bondedTo:
            pygame.draw.line(surface, (128,128,255), [int(i) for i in self.pos],  [int(i) for i in p.pos])
        
    def renderSelf(self, surface):
        """Renders a circle with the particle name in it"""
        pygame.draw.circle(surface, (255,128,128), (int(self.pos[0]), int(self.pos[1])), self.radius)
        surface.blit(self.label, (int(self.pos[0]) - self.label.get_width()/2, int(self.pos[1]) - self.label.get_height()/2))

def QuitHandler(event):
   raise "QUIT EVENT"

class ParticleDragger(DragHandler):
     def detect(self, pos):
         inRange = self.app.physics.indexer.withinRadius( pos, self.app.particleRadius )
         if len(inRange) > 0:
             self.particle = inRange[0]
             self.particle.freeze()
             return self.particle.getLoc()
         else:
             return False

     def drag(self,newx,newy):
         self.particle.pos = (newx,newy)
         self.app.physics.indexer.updateLoc(self.particle)

     def release(self,newx, newy):
         self.drag(newx, newy)
         self.particle.unFreeze()                

class PhysApp1(PyGameApp):
    """Simple physics demonstrator app"""

    def __init__(self, screensize, nodes = None, initialTopology=[], border=100):
        super(PhysApp1, self).__init__(screensize, "Physics test 1, drag nodes to move them", border)
        self.initialTopology = list(initialTopology)
        self.particleRadius = 20
        self.nodes = nodes

    def makeBond(self, source, dest):
        self.physics.particleDict[source].addBond(self.physics.particleDict, dest)

    def makeParticle(self, ID, label, position, nodetype, particleRadius):
        if position == "randompos":
           xpos = randrange(self.border,self.screensize[0]-self.border,1)
           ypos = randrange(self.border,self.screensize[1]-self.border,1)
        else:
           xpos,ypos = position
        particle = Particle( (xpos, ypos), ID, label, particleRadius)
        self.physics.add( particle )

    def initialiseComponent(self):
        self.addHandler(MOUSEBUTTONDOWN, lambda event: ParticleDragger(event,self))
#        self.addHandler(KEYDOWN, QuitHandler)
        
        self.laws    = Physics.SimpleLaws(bondLength = 100)
        self.physics = Physics.ParticleSystem(self.laws, [], 0)
        
        for node in self.nodes:
           self.makeParticle(*node)

        for source,dest in self.initialTopology:
           self.makeBond(source, dest)
        return 1

    def handleCommunication(self):
        if self.dataReady("inbox"):
           message = self.recv("inbox")
           if message[0] == "ADD":
              if message[1] == "NODE":
                 self.makeParticle(*(message[2]))
              elif message[1] == "LINK":
                 self.makeBond(*(message[2]))

    def mainLoop(self):
        self.handleCommunication()
        self.screen.fill( (255,255,255) )
        
        self.drawGrid()
        
        for p in self.physics.particles:
            p.renderBonds(self.screen)

        for p in self.physics.particles:
            p.renderSelf(self.screen)
            
        self.physics.run()
        return 1

    def drawGrid(self):
        for i in range(0,self.screen.get_height(), int(self.laws.maxInteractRadius)):
            pygame.draw.line(self.screen, (200,200,200),
                             (0,i),
                             (self.screen.get_width(),i) )

        for i in range(0,self.screen.get_width(), int(self.laws.maxInteractRadius)):
            pygame.draw.line(self.screen, (200,200,200), 
                             (i,0), 
                             (i,self.screen.get_height()) )

class node_message_parser(component):
   def __init__(self):
      super(node_message_parser, self).__init__()
      self._thread = self.main()

   def main(self):
      while 1:
         if self.dataReady("inbox"):
            line = self.recv("inbox")
            message = line.split(" ")
            if message[0] == "ADD" and message[1] == "NODE":
               if message[4] != "randompos":
                  x,y = message[4][1:-1].split(",")
                  x = int(x)
                  y = int(y)
                  message[4] = (x,y)
               if message[5] == "circle":
                  message[6] = int(message[6])
            self.send( (message[0],message[1], tuple(message[2:])), "outbox")
            yield 1
         else:
            yield None

class chunks_to_lines(component):
   def main(self):
      gotLine = False
      line = ""
      while 1: 
         pos = line.find("\n")
         if pos > -1:
            self.send(line[:line.find("\n")], "outbox")
            line = line[line.find("\n")+1:] 
         else:
            if self.dataReady("inbox"):
               chunk = self.recv("inbox")
               chunk = chunk.replace("\r", "")
               line = line + chunk
            else:
               self.pause()
         yield 1

class testHarness(component):
   def __init__(self, someComponent, messages, checkerComponent = None, rate = 0.1):
       super(testHarness, self).__init__()
       self.component = someComponent
       self.rate = rate
       self.messages = messages
       self.checkerComponent = checkerComponent

   def main(self):
      app = self.component# self.componentClass( *self.args)
      self.addChildren(app)
      self.link((self,"outbox"), (app,"inbox"))
      if self.checkerComponent:
         self.link((app,"outbox"),(self.checkerComponent,"inbox"))
         self.link((app,"signal"),(self.checkerComponent,"control"))
         self.addChildren(self.checkerComponent)
      yield _Axon.Ipc.newComponent(*(self.children))
      t = time.time()
      M = 0
      while 1:
         if (time.time() -t)>self.rate:
            t = time.time()
            if M < len(self.messages):
                self.send(self.messages[M])
                M = M + 1
            else:
               self.pause()
         yield 1

class pipeline(component):
   def __init__(self, *components):
      super(pipeline,self).__init__()
      self.components = list(components)
   def main(self):
      self.addChildren(*self.components)
      pipeline = self.components[:]
      source = pipeline[0]
      del pipeline[0]
      while len(pipeline)>0:
         dest = pipeline[0]
         del pipeline[0]
         self.link((source,"outbox"), (dest,"inbox"))
         self.link((source,"signal"), (dest,"control"))
         source = dest
      self.link((self,"inbox"), (self.components[0],"inbox"), passthrough=1)
      self.link((self,"control"), (self.components[0],"control"), passthrough=1)
      self.link((self.components[-1],"outbox"), (self,"outbox"), passthrough=2)
      self.link((self.components[-1],"signal"), (self,"signal"), passthrough=2)
      yield _Axon.Ipc.newComponent(*(self.children))
      while 1:
         self.pause()
         yield 1

if __name__=="__main__":
    source = """\
ADD NODE 0 A randompos circle 20
ADD NODE 1 B randompos circle 20
ADD NODE 2 C randompos circle 20
ADD NODE 3 D randompos circle 20
ADD NODE 4 E randompos circle 20
ADD NODE 5 F randompos circle 20
ADD NODE 6 G randompos circle 20
ADD NODE 7 H randompos circle 20
ADD NODE 8 I randompos circle 20
ADD NODE 9 J randompos circle 20
ADD LINK 0 1
ADD LINK 0 2
ADD LINK 0 3
ADD LINK 1 5
ADD LINK 1 2
ADD LINK 1 6
ADD LINK 3 1
ADD LINK 4 1
ADD LINK 5 3
ADD LINK 5 4
ADD LINK 6 2
ADD LINK 6 4
ADD LINK 7 0
ADD LINK 7 2
ADD LINK 8 3
ADD LINK 8 5
ADD LINK 9 4
ADD LINK 9 6
"""

    chunks = []

    for point in range(0,len(source),32):
       chunks.append(source[point:(point+32)])


    from Kamaelia.SingleServer import SingleServer
    _app = testHarness(pipeline(chunks_to_lines(),
                               node_message_parser(),
                               PhysApp1((640, 480), [], [])),
                      chunks, rate=0)
    app  = pipeline(SingleServer(port=1500),
                    chunks_to_lines(),
                    node_message_parser(),
                    PhysApp1((640, 480), [], []))
    app.activate()
    _scheduler.run.runThreads(slowmo=0)


