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
        
        cols = maxw / self.xspacing # int div
        rows = maxh / self.yspacing
        
        self.width = cols*xspacing
        self.height = rows*yspacing
        
        xborder = (maxw - self.width)/2
        yborder = (maxh - selfheight)/2
        coldividers = [i*self.xspacing + xborder for i in xrange(0, cols)]
        rowdividers = [i*self.yspacing + yborder for i in xrange(0, rows)]
        
        self.cols = [column(self, c, y, xspacing, self.height, yspacing) for c in coldividers]
        self.rows = [row(self, x, r, yspacing, self.width, xspacing) for r in rowdividers]
                
        self.surface = pygame.Surface((maxw, maxh)).convert()
        self.surface.fill(colours["white"])
        for c in self.cols: c.draw(surface)
    
    
    def contains(self, x, y):
        return self.bounds().collidepoint(x, y)
    
    def bounds(self):
        return Rect(self.x, self.y, self.width, self.height)
    
    def snapToCol(self, x):
        for c in self.cols:
            if c.contains(x):
                return self.cols.index(c)

    def snapToRow(self, y):
        for r in self.rows:
            if r.contains(y):
                return self.rows.index(r)
    
    def snapToGrid(self, x, y):
        col, row = self.snapToCol(x), self.snapToRow(y)
        return self.colCoord(col), self.rowCoord(row)
    
    def rowCoord(self, row):
        return self.rows[row].start# + 2*self.border
    
    def colCoord(self, col):
        return self.cols[col].start
    
    def handleMouseDown(self, x, y):
        x -= self.x  #adjust coords relative to self.surface
        y -= self.y
        if self.container.floating:
            row = self.snapToRow(y)
            if not self.shardhist.current():
                g = guiShard(self.container.floating, None, self.rows[row], self.cols[:]))
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
    