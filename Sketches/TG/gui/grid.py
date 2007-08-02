import pygame
from pygame.color import THECOLORS as colours
from pygame.draw import line
from pygame.rect import Rect

class grid(object):
    def __init__(self, surface, x, y, maxw, maxh, xspacing = 75, yspacing = 36):
        
        self.container = None #set by container when added
        self.x = x
        self.y = y
        self.xspacing = xspacing
        self.yspacing = yspacing
        self.border = 1
        self.colour = colours['grey90']
        
        # integer division
        cols = maxw / self.xspacing
        rows = maxh / self.yspacing
        
        self.width = cols*xspacing
        self.height = maxh
        
        self.surface = pygame.Surface((maxw, maxh)).convert()
        self.surface.fill(colours["white"])
        
        xborder = (maxw - self.width)/2
        yborder = yspacing/2
        
        self.coldividers = []
        self.rowdividers = []
        
        # vertical lines
        for i in xrange(0, cols + 1):
            colstart = i*self.xspacing + xborder
            self.coldividers += [colstart]
            line(self.surface, self.colour, (colstart, yborder), (colstart, self.height+yborder))
        
        # horizontal lines
        for i in xrange(0, rows):
            rowstart = i*self.yspacing + yborder
            self.rowdividers += [rowstart]
            line(self.surface, self.colour, (xborder, rowstart), (self.width+xborder, rowstart))
    
    def contains(self, x, y):
        return self.bounds().collidepoint(x, y)
    
    def bounds(self):
        return Rect(self.x, self.y, self.surface.get_width(), self.height)
    
    def snapToGrid(self, x, y):
        diffs = [abs(vert - x) for vert in self.coldividers]
        newx, xind = min((x, i) for i, x in enumerate(diffs))
        
        diffs = [abs(hor - y) for hor in self.rowdividers]
        newy, yind = min((y, i) for i, y in enumerate(diffs))
        
        return self.coldividers[xind], self.rowdividers[yind] + 2
    
    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))
        return [self.bounds()]


if __name__ == '__main__':
    from gui import *
    main()
    