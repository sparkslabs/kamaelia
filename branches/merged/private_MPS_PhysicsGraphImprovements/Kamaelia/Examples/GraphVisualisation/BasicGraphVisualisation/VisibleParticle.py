#!/usr/bin/env python

# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import Physics
import UI

import pygame
from pygame.locals import *

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
        self.addHandler(MOUSEBUTTONDOWN, lambda event: ParticleDragger(event,self))
        self.addHandler(KEYDOWN, self.quit)
        
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
    for i in xrange(N):
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
