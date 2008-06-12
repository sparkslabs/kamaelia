#!/usr/bin/env python

import pygame
from Kamaelia.Support.Particles import Particle as BaseParticle

from pygame.transform import smoothscale

class GenericParticle(BaseParticle):
    """\
    =========================
    A generic particle class
    =========================
    
    A generic particle type with picture, shape, color and size customable and updatable
    Adapted from MPS.Experiments.360.Creator.IconComponent and .PPostbox
    """
   
    def __init__(self, position, ID = None, type='', name='', pic=None, shape='circle', 
                 color=None, width=None, height=None, radius=None):
        super(GenericParticle,self).__init__(position=position, ID = ID )
        self.type = type
        pygame.font.init()
        self.set_label(name)
        #self.name = name
        self.picture = None
        self.shape = None
        self.radius = None
        self.width = None
        self.height = None
        
        self.set_radius(radius)
        self.set_width(width)
        self.set_height(height)
        
        self.color = None        
        self.left = 0
        self.top = 0
        self.selected = False
        self.bondedRelations = {}

        if pic is not None:
            self.set_pic(pic)
        else:
            self.set_color(color)
            self.set_shape(shape)
                       
        
    def updateAttrs(self, **attrs):
        for key,value in attrs.iteritems():
            methodName = 'set_' + key
            if hasattr(self,methodName):
                method = getattr(self,methodName)
                method(value)
    
    def set_width(self, width):
        if width is not None:
            self.width = int(width)
            if self.height is None:
                self.height = self.width
            if self.picture is not None:
                self.height = self.picture.get_height()
                self.picture = smoothscale(self.picture, (self.width,self.height))
            self.radius = ((self.width*self.width+self.height*self.height)**0.5)/2
        else:
            self.width = width
    
    def set_height(self, height):
        if height is not None:
            self.height = int(height)
            if self.width is None:
                self.width = self.height
            if self.picture is not None:
                self.width = self.picture.get_width()
                self.picture = smoothscale(self.picture, (self.width,self.height))
            self.radius = ((self.width*self.width+self.height*self.height)**0.5)/2
        else:
            self.height = height
                                
    def set_radius(self, radius):
        if radius is not None:
            self.radius = int(radius)
        else:
            self.radius = radius
        
    def set_color(self, color):
        if color is not None:
            if isinstance(color, str):
                colorMap = {'blue': (128,128,255), 'pink': (255,128,128)}
                if colorMap.has_key(color):
                    self.color = colorMap[color]
                else:
                    print 'Only '+colorMap.keys().__str__()+' available' 
            else:
                self.color = color
        else:
            self.color = (255,128,128)
        
    def set_label(self, newname):
        self.name = newname
        font = pygame.font.Font(None, 20)        
        self.slabel   = font.render(self.name, True, (0,0,0))
        self.slabelxo = - self.slabel.get_width()/2
        self.slabelyo = - self.slabel.get_height()/2
        description = self.type+" : "+self.name
        self.desclabel = font.render( description, True, (0,0,0), (255,255,255))
        
    def set_pic(self, pic):
        self.picture = pygame.image.load(pic).convert()
        if (self.width is not None) and (self.height is not None):
            self.picture = smoothscale(self.picture, (self.width,self.height))
            
        else:
            self.width = self.picture.get_width()
            self.height = self.picture.get_height()  
        self.radius = ((self.width*self.width+self.height*self.height)**0.5)/2
        self.shape = None
        self.color = None
        
    def set_shape(self, shape):
        if shape is not None:
            self.shape = shape
            self.picture = None
            if self.color is None:
                self.color = (255,128,128)
            if shape == 'circle':
                self.width = None
                self.height = None
                if self.radius is None:
                    self.radius = 30
            else:
                if self.width is None:
                    self.width = 60
                if self.height is None:
                    self.height = 60
                self.radius = ((self.width*self.width+self.height*self.height)**0.5)/2
            

    
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
            px = int(p.pos[0] -self.left)
            py = int(p.pos[1] - self.top)
            # Draw a link
            pygame.draw.line(surface, (128,128,255), (x,y),  (px,py))
            
            # Draw a pretty arrow on the line, showing the direction
            arrow_colour = (0,160,0)
            
            direction = ( (px-x), (py-y) )
            length    = ( direction[0]**2 + direction[1]**2 )**0.5
            
            """Make the position of the arrow relative to the intersection
            between arc and the bond line rather than the centre of particle"""
            intersection_x = x - self.radius*(x-px)/length
            intersection_y = y - self.radius*(y-py)/length
            intersection_px = px - p.radius*(px-x)/length
            intersection_py = py - p.radius*(py-y)/length
            intersection_relationLabel = ( (2*intersection_x+intersection_px)/3, 
                                           (2*intersection_y+intersection_py)/3 )
            arrowHead = ( (intersection_x+intersection_px*2)/3, (intersection_y+intersection_py*2)/3 )
            direction = [ 6*n / length for n in direction ]
            
            norm      = ( -direction[1], direction[0] )
            
            leftarrow  = ( arrowHead[0] - direction[0] - norm[0], arrowHead[1] - direction[1] - norm[1] )
            rightarrow = ( arrowHead[0] - direction[0] + norm[0], arrowHead[1] - direction[1] + norm[1] )
            
            pygame.draw.line(surface, arrow_colour, arrowHead, leftarrow  )
            pygame.draw.line(surface, arrow_colour, arrowHead, rightarrow )
            
            # Add text on the link to show the relation
            if self.bondedRelations.has_key(p):
                font = pygame.font.Font(None, 15)
                self.relationLabel = font.render(" "+self.bondedRelations[p]+" ", True, (0,0,0), )
                relationLabel_pos = (intersection_relationLabel[0]-self.relationLabel.get_width()/2,  
                                     intersection_relationLabel[1]-self.relationLabel.get_height()/2)
                surface.blit(self.relationLabel, relationLabel_pos)  
        yield 2
        
        # Draw a particle
        if self.picture is not None:
            picture_rect = surface.blit(self.picture, (x- self.width/2, y - self.height/2))
            surface.blit(self.slabel, (x - self.slabel.get_width()/2, y + self.height/2) )
            
            if self.selected:
                
                pygame.draw.rect(surface, (0,0,0), picture_rect, 2)
                surface.blit(self.desclabel, (72,16) )
        else:
            if self.shape == 'circle':
                pygame.draw.circle(surface, self.color, (x,y), self.radius)
                if self.selected:
                    pygame.draw.circle(surface, (0,0,0), (x,y), self.radius, 2)
                    surface.blit(self.desclabel, (72,16) )
            else:
                pygame.draw.rect(surface, self.color, (x- self.width/2, y - self.height/2, self.width, self.height))
                if self.selected:
                    pygame.draw.rect(surface, (0,0,0), (x- self.width/2, y - self.height/2, self.width, self.height), 2)
                    surface.blit(self.desclabel, (72,16) )
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
 
