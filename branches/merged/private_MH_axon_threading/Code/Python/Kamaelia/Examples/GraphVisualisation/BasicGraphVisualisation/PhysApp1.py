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

from VisibleParticle import VisibleParticle
# from ParticleDragger import ParticleDragger
from Kamaelia.Visualisation.PhysicsGraph.ParticleDragger import ParticleDragger

import Kamaelia.Physics as Physics
import Kamaelia.UI.MH
import pygame
from random import randrange

# ?
from pygame.locals import *

import random

from Axon.Component import component

class ParticleDragger(Kamaelia.UI.MH.DragHandler):
    pass

class __ParticleDragger(Kamaelia.UI.MH.DragHandler):
     def detect(self, pos, button):
         inRange = self.app.physics.withinRadius( pos, self.app.particleRadius )
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

class PhysApp1(Kamaelia.UI.MH.PyGameApp, component):
    """Simple physics demonstrator app"""

    def __init__(self, screensize, fullscreen = False, nodes = None, initialTopology=[], border=100):
        super(PhysApp1, self).__init__(screensize, "Physics test 1, drag nodes to move them", fullscreen)
        self.border = border
        self.initialTopology = list(initialTopology)
        self.particleRadius = 20
        self.nodes = nodes
        self.physics = None
        self.X = 5

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

    def extra(self):
       if self.physics:
          if random.randrange(0,100)<5:
             self.makeParticle(str(self.X), "randompos", "circle", 20)
             self.X += 1
          if random.randrange(0,100)<25:
             start = self.physics.particleDict.keys()[random.randrange(0,len(self.physics.particleDict.keys()))]
             end = start
             while end == start:
                end = self.physics.particleDict.keys()[random.randrange(0,len(self.physics.particleDict.keys()))]
             self.makeBond(self.physics.particleDict[start].ID, self.physics.particleDict[end].ID)


    def mainLoop(self):
        self.screen.fill( (255,255,255) )
        
        self.drawGrid()
        
        for p in self.physics.particles:
            p.renderBonds(self.screen)

        for p in self.physics.particles:
            p.renderSelf(self.screen)
            
        self.physics.run(1)
#        self.extra()
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
