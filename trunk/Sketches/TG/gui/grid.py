import pygame
from pygame.color import THECOLORS as colours
from pygame.draw import line
from pygame.rect import Rect

from guiShard import guiShard

class grid(object):
    def __init__(self, surface, x, y, maxw, maxh, xspacing = 75, yspacing = 36):
        
        self.container = None #set by container when added
        self.x = x
        self.y = y
        self.xspacing = xspacing
        self.yspacing = yspacing
        self.border = 1
        self.colour = colours['grey90']
        
        self.rootshard = None
        
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
    
    def snapToCol(self, x):
        diffs = [abs(c - x) for c in self.coldividers]
        newx, col = min((x, i) for i, x in enumerate(diffs))
        return col
        
    def snapToRow(self, y):
        diffs = [abs(r - y) for r in self.rowdividers]
        newy, row = min((y, i) for i, y in enumerate(diffs))
        return row

    def snapToGrid(self, x, y):
        col, row = self.snapToCol(x), self.snapToRow(y)
        return self.colCoord(col), self.rowCoord(row)
    
    def rowCoord(self, row):
        return self.rowdividers[row] + 2*self.border
    
    def colCoord(self, col):
        return self.coldividers[col]
    
    def maxRows(self):
        return len(self.rowdividers)
        
    def maxCols(self):
        return len(self.coldividers)
    
    def handleMouseDown(self, x, y):
        if self.container.floating:
            col, row = self.snapToCol(x), self.snapToRow(y)
            # depending on occupation, add float label to grid cell
            # add to draw list
            if not self.rootshard:
                g = guiShard(self.container.floating, None, row, range(0, self.maxCols()-1))
                self.rootshard = g
            else:
                self.rootshard.add(self.container.floating, row, col)
            
            self.container.floating.erase(self.container.screen)
            self.container.floating = None
    
    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))
        if self.rootshard:
            self.rootshard.draw(surface)
        
        return [self.bounds()]


if __name__ == '__main__':
    from gui import *
    main()
    