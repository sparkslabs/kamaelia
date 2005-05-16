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

import Physics
from PyGameApp import PyGameApp, DragHandler

import pygame
from pygame.locals import *

from random import randrange

class Particle(Physics.Particle):
    """Version of Physics.Particle with added rendering functions,
    and a list of particles it is bonded to."""

    def __init__(self, position, pname, radius):
        Physics.Particle.__init__(self, position, 0, (0.0, 0.0) )
        self.pname = pname
        self.radius = radius
        self.bondedTo = []
        
        font = pygame.font.Font(None, 24)
        self.label = font.render(self.pname, False, (0,0,0))
        
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


class PhysApp1(PyGameApp):
    """Simple physics demonstrator app"""

    class ParticleDragger(DragHandler):
        def detect(self, pos):
            inRange = self.app.physics.indexer.withinRadius( pos, app.particleRadius )
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



    def __init__(self, screensize):
        PyGameApp.__init__(self, screensize, "Physics test 1, drag nodes to move them")


    def initialiseComponent(self):
        self.addHandler(MOUSEBUTTONDOWN, lambda event: self.ParticleDragger(event,self))
        
        self.particleRadius = 20
        
        self.laws    = Physics.SimpleLaws(bondLength = 100)
        self.physics = Physics.ParticleSystem(self.laws, [], 0)
        
        for i in range(0,7):
            self.physics.add( Particle( (randrange(100,500,1),
                                         randrange(100,300,1)), str(i), self.particleRadius) )
            
        self.physics.particles[0].bondedTo += [self.physics.particles[1]]
        self.physics.particles[1].bondedTo += [self.physics.particles[2]]
        self.physics.particles[2].bondedTo += [self.physics.particles[0]]
        self.physics.particles[1].bondedTo += [self.physics.particles[3]]
        self.physics.particles[1].bondedTo += [self.physics.particles[4]]
        self.physics.particles[3].bondedTo += [self.physics.particles[5]]
        self.physics.particles[3].bondedTo += [self.physics.particles[6]]
        self.physics.particles[2].bondedTo += [self.physics.particles[6]]

    def mainLoop(self):
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



if __name__=="__main__":
    app = PhysApp1( (640, 480) )
    app.mainloop()
