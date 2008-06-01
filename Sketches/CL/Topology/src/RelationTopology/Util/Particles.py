#!/usr/bin/env python

import pygame
from Kamaelia.Visualisation.PhysicsGraph.RenderingParticle import RenderingParticle

class GenericParticle(RenderingParticle):
    """\
    A generic particle type with color and picture customable
    TODO: shape, size customable
    """
    extraArgd = {}
    def __init__(self, **argd):
        self.extraArgd = {}     
        if argd.has_key('pic'):
            self.extraArgd.update({'pic':argd['pic']})
            argd.pop('pic')
        if argd.has_key('color'):
            self.extraArgd.update({'color':argd['color']})
            argd.pop('color')           
        super(GenericParticle, self).__init__(**argd)
        
        
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
            pygame.draw.line(surface, (128,128,255), (x,y),  (int(p.pos[0] -self.left),int(p.pos[1] - self.top)) )
        
        yield 2
        if self.extraArgd.has_key('pic'):
            picture = pygame.image.load(self.extraArgd['pic']).convert()
            picture_rect = surface.blit(picture, (x,y))

        if self.extraArgd.has_key('color'):
            pygame.draw.circle(surface, eval(self.extraArgd['color']), (x,y), self.radius)
        else:
            pygame.draw.circle(surface, (255,128,128), (x,y), self.radius)
        
        if self.extraArgd.has_key('pic'):
            if self.selected:
                pygame.draw.rect(surface, (0,0,0), picture_rect, 2)
        else:
            if self.selected:
                pygame.draw.circle(surface, (0,0,0), (x,y), self.radius, 2)
        
        surface.blit(self.label, (x - self.label.get_width()/2, y - self.label.get_height()/2)) 
