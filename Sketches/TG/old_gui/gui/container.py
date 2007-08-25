import pygame
from pygame.locals import *

class container(object):
    floating = None
    
    def __init__(self, toolbar, grid, screen):
        
        self.toolbar = toolbar
        self.grid = grid
        
        self.toolbar.container = self
        self.grid.container = self
        
        self.screen = screen
    
    def handleEvent(self, e):
        if e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            if self.toolbar.contains(x, y):
                self.toolbar.handleMouseDown(e)
            elif self.grid.contains(x, y):
                self.grid.handleMouseDown(x, y)
        
        elif e.type == MOUSEMOTION:
            self.handleMouseMove(e)
    
    def handleMouseMove(self, e):
        if self.floating:
            self.floating.handleMouseMove(e)
            
    def draw(self, surface):
        rs = self.toolbar.draw(surface) + self.grid.draw(surface)
        if self.floating:
            rs += self.floating.draw(surface)
        return rs


if __name__ == '__main__':
    from gui import *
    main()