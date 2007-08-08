import pygame
from pygame.color import THECOLORS as colours
from pygame.draw import line
from pygame.rect import Rect

from guiShard import guiShard
from history import history

class grid(object):
    def __init__(self, surface, x, y, maxw, maxh, xspacing = 75, yspacing = 36):
        
        self.container = None #set by container when added
        self.x = x
        self.y = y
        self.xspacing = xspacing
        self.yspacing = yspacing
        self.border = 1
        self.colour = colours['grey90']
        
        self.shardhist = history(self)
        
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
        
        self.colcentres = []
        for i in xrange(0, len(self.coldividers)-1):
            self.colcentres += [(self.coldividers[i] + self.coldividers[i+1])/2]
        
        self.rowcentres = []
        for i in xrange(0, len(self.rowdividers)-1):
            self.rowcentres += [(self.rowdividers[i] + self.rowdividers[i+1])/2]
    
    def contains(self, x, y):
        return self.bounds().collidepoint(x, y)
    
    def bounds(self):
        return Rect(self.x, self.y, self.surface.get_width(), self.height)
    
    def snapToCol(self, x):
        for i in range(1, len(self.coldividers)):
            if x < self.coldividers[i]:
                #print 'col', i
                return i-1

    def snapToRow(self, y):
        for i in range(1, len(self.rowdividers)):
            if y < self.rowdividers[i]:
                #print 'row', i
                return i-1

    def snapToGrid(self, x, y):
        col, row = self.snapToCol(x), self.snapToRow(y)
        return self.colCoord(col), self.rowCoord(row)
    
    def rowCoord(self, row):
        return self.rowdividers[row] + 2*self.border
    
    def colCoord(self, col):
        return self.coldividers[col]
    
    def maxRows(self):
        return len(self.rowcentres)
        
    def maxCols(self):
        return len(self.colcentres)
    
    def handleMouseDown(self, x, y):
        x -= self.x  #adjust coords relative to col/rowdividers, etc.
        y -= self.y
        if self.container.floating:
            row = self.snapToRow(y)
            if not self.shardhist.current():
                g = guiShard(self.container.floating, None, row, range(0, self.maxCols()))
                self.shardhist.add(g)
            else:
                self.shardhist.current().add(self.container.floating, row, x)
            
            self.container.floating.erase(self.container.screen)
            self.container.floating = None
        else:
            if self.shardhist.current():
                self.shardhist.current().handleMouseDown(x, y)
    
    def clear(self):
        self.shardhist.add(None)
    
    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))
        if self.shardhist.current():
            self.shardhist.current().draw(surface)
        
        return [self.bounds()]


if __name__ == '__main__':
    from gui import *
    main()
    