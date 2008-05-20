#!/usr/bin/env python

import pygame
from Kamaelia.Visualisation.PhysicsGraph.RenderingParticle import RenderingParticle

class BlueParticle(RenderingParticle):
    """\
    A particle type filled with blue
    """
    def __init__(self, **argd):
        super(BlueParticle, self).__init__(**argd) 
    def render(self, surface):
        """\
        Multi-pass rendering generator.

        Renders this particle in multiple passes to the specified pygame surface -
        yielding the number of the next pass to be called on between each. Completes
        once it is fully rendered.
        """
        x = int(self.pos[0]) - self.left
        y = int(self.pos[1]) - self.top
        
        yield 1
        for p in self.bondedTo:
            pygame.draw.line(surface, (255,128,128), (x,y),  (int(p.pos[0] -self.left),int(p.pos[1] - self.top)) )
        
        yield 2
        pygame.draw.circle(surface, (128,128,255), (x,y), self.radius)
        if self.selected:
            pygame.draw.circle(surface, (0,0,0), (x,y), self.radius, 2)
        surface.blit(self.label, (x - self.label.get_width()/2, y - self.label.get_height()/2)) 