#!/usr/bin/env python

import pygame
from Kamaelia.Support.Particles import Particle as BaseParticle

class GenericParticle(BaseParticle):
    """\
    A generic particle type with picture, shape, color and size customable
    Adapted from MPS.Experiments.360.CreatorIconComponent
    """
   
    def __init__(self, position, ID = None, type='', name='', pic=None, shape='circle', 
                 color=None, width=None, height=None, radius=None):
        super(GenericParticle,self).__init__(position=position, ID = ID )
        self.type = type
        self.set_label(name)
        #self.name = name
        self.picture = pic
        self.shape = shape
        self.color = color
        self.left = 0
        self.top = 0
        self.selected = False
        if pic is not None:
            self.picture = pygame.image.load(pic).convert()
            if (width is not None) and (height is not None):
                self.width = float(width)
                self.height = float(height)
                from pygame.transform import smoothscale           
                self.picture = smoothscale(self.picture, (self.width,self.height))
            else:
                self.width = self.picture.get_width()
                self.height = self.picture.get_height()
            from math import sqrt
            self.radius = sqrt(self.width*self.width+self.height*self.height)/2
        else:
            if shape == 'circle':
                if radius is not None:
                    self.radius = float(radius)
                else:
                    self.radius = 30
            else:
                if (width is not None) and (height is not None):
                    self.width = float(width)
                    self.height = float(height)
                else:
                    self.width = 60
                    self.height = 60
                from math import sqrt
                self.radius = sqrt(self.width*self.width+self.height*self.height)/2             
        
        
    def set_label(self, newname):
        self.name = newname
        pygame.font.init()
        font = pygame.font.Font(None, 20)
        self.slabel   = font.render(self.name, True, (0,0,0))
        self.slabelxo = - self.slabel.get_width()/2
        self.slabelyo = - self.slabel.get_height()/2
        description = self.type+" : "+self.name
        self.desclabel = font.render( description, True, (0,0,0), (255,255,255))
        
            
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
        if self.picture is not None:
            picture_rect = surface.blit(self.picture, (x- self.width/2, y - self.height/2))
            surface.blit(self.slabel, (x - self.slabel.get_width()/2, y + self.height/2) )
            if self.selected:
                pygame.draw.rect(surface, (0,0,0), picture_rect, 2)
        else:
            if self.shape == 'circle':
                if self.color is not None:
                    colorMap = {'blue': (128,128,255), 'pink': (255,128,128)}
                    pygame.draw.circle(surface, colorMap[self.color], (x,y), self.radius)
                else:
                    pygame.draw.circle(surface, (255,128,128), (x,y), self.radius)
                if self.selected:
                    pygame.draw.circle(surface, (0,0,0), (x,y), self.radius, 2)
            else:
                if self.color is not None:
                    colorMap = {'blue': (128,128,255), 'pink': (255,128,128)}
                    pygame.draw.rect(surface, colorMap[self.color], (x- self.width/2, y - self.height/2, self.width, self.height))
                else:
                    pygame.draw.rect(surface, (255,128,128), (x- self.width/2, y - self.height/2, self.width, self.height))
                if self.selected:
                    pygame.draw.rect(surface, (0,0,0), (x- self.width/2, y - self.height/2, self.width, self.height), 2)
            surface.blit(self.slabel, (x - self.slabel.get_width()/2, y - self.slabel.get_height()/2) )                
    
    
    def setOffset( self, (x,y) ):
        """\
        Set the offset of the top left corner of the rendering area.
        
        If this particle is at (px,py) it will be rendered at (px-x,py-y).
        """
        self.left = x
        self.top  = y

    def select( self ):
        """Tell this particle it is selected"""
        if self.selected:
            self.deselect()
        else:
            self.selected = True

    def deselect( self ):
        """Tell this particle it is deselected"""
        self.selected = False
 
