#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------

# Checked 2024/03/24

# first test of Physics module

import Physics
import UI

import pygame

from random import randrange
import random

from Axon.Component import component
# class component(object): pass

class VisibleParticle(Physics.Simple.Particle):
    """Version of Physics.Simple.Particle with added rendering functions,
    and a list of particles it is bonded to."""

    def __init__(self, position, pname, radius):
        super(VisibleParticle,self).__init__(position=position, ID=pname )
        self.radius = radius
        
        font = pygame.font.Font(None, 24)
        self.label = font.render(self.ID, False, (0,0,0))
        
    def renderBonds(self, surface):
        """Renders lines representing the bonds going from this particle"""
        for p in self.bondedTo:
            pygame.draw.line(surface, (128,128,255), [int(i) for i in self.pos],  [int(i) for i in p.pos])
        
    def renderSelf(self, surface):
        """Renders a circle with the particle name in it"""
        pygame.draw.circle(surface, (255,128,128), (int(self.pos[0]), int(self.pos[1])), self.radius)
        surface.blit(self.label, (int(self.pos[0]) - self.label.get_width()/2, int(self.pos[1]) - self.label.get_height()/2))


class ParticleDragger(UI.MH.DragHandler):
     def detect(self, pos, button):
         inRange = self.app.physics.withinRadius( pos, app.particleRadius )
         if len(inRange) > 0:
             self.particle = inRange[0][0]
             self.particle.freeze()
             return self.particle.getLoc()
         else:
             return False

     def drag(self,newx,newy):
         self.particle.pos = (newx,newy)
         self.app.physics.updateLoc(self.particle)

     def release(self,newx, newy):
         self.drag(newx, newy)
         self.particle.unFreeze()                

class PhysApp1(UI.MH.PyGameApp, component):
    """Simple physics demonstrator app"""

    def __init__(self, screensize, fullscreen = False, nodes = None, initialTopology=[], border=100):
        super(PhysApp1, self).__init__(screensize, "Physics test 1, drag nodes to move them", fullscreen)
        self.border = border
        self.initialTopology = list(initialTopology)
        self.particleRadius = 20
        self.nodes = nodes

    def makeBond(self, source, dest):
        self.physics.particleDict[source].makeBond(self.physics.particleDict, dest)

    def makeParticle(self, label, position, nodetype, particleRadius):
        if position == "randompos":
           xpos = randrange(self.border, self.screensize[0]-self.border, 1)
           ypos = randrange(self.border, self.screensize[1]-self.border, 1)
        else:
           xpos,ypos = position
        particle = VisibleParticle( (xpos, ypos), label, particleRadius)
        self.physics.add( particle )

    def initialiseComponent(self):
        self.addHandler(pygame.MOUSEBUTTONDOWN, lambda event: ParticleDragger(event,self))
        self.addHandler(pygame.KEYDOWN, self.quit)
        
        self.laws    = Physics.Simple.SimpleLaws(bondLength = 100)
        self.physics = Physics.Simple.ParticleSystem(self.laws, [], 0)
        
        for node in self.nodes:
           self.makeParticle(*node)

        for source,dest in self.initialTopology:
           self.makeBond(source, dest)

    def mainLoop(self):
        self.screen.fill( (255,255,255) )
        
        self.drawGrid()
        
        for p in self.physics.particles:
            p.renderBonds(self.screen)

        for p in self.physics.particles:
            p.renderSelf(self.screen)
            
        self.physics.run(1)
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



if __name__=="__main__":
    N,L = 4,2

    nodes = []
    for i in range(N):
       nodes.append((str(i), "randompos", "circle", 20))

    linkDict = {}
    while len(linkDict.keys()) <L:
       start = random.randrange(0,len(nodes))
       end = start
       while end == start:
          end = random.randrange(0,len(nodes))
       linkDict[ nodes[start][0],nodes[end][0] ] = None
    links = linkDict.keys()

    app = PhysApp1( (640, 480), False, nodes, links)
    X = N+1
    for i in app.main():
       if randrange(0,100)<5:
          app.makeParticle(str(X), "randompos", "circle", 20)
          X += 1
       if randrange(0,100)<25:
          start = app.physics.particleDict.keys()[random.randrange(0,len(app.physics.particleDict.keys()))]
          end = start
          while end == start:
             end = app.physics.particleDict.keys()[random.randrange(0,len(app.physics.particleDict.keys()))]
          app.makeBond(app.physics.particleDict[start].ID, app.physics.particleDict[end].ID)
