from pygame.draw import rect
from pygame.color import THECOLORS as colours
from pygame.rect import Rect

from random import randint

nicecolours = [c for k, c in colours.items() if not ('grey' in k or 'gray' in k or 'black' in k)]
darkcolours = [x for x in nicecolours if x[0]+x[1]+x[2] < 500]

def pickColour():
    return darkcolours[randint(0, len(darkcolours)-1)]

class guiShard(object):
    def __init__(self, floating, parent, row, cols):
        
        self.floating = floating
        self.colour = pickColour()
        
        self.grid = floating.container().grid
        
        self.row = row
        self.cols = cols
        
        self.rect = self.makeRect()
        
        self.parent = parent
        self.children = []
    
    def draw(self, surface):
        rect(surface, self.colour, self.rect, 0)
        for c in self.children:
            c.draw(surface)
    
    def makeRect(self):
        x = self.grid.colCoord(self.cols[0])
        y = self.grid.rowCoord(self.row)
        width = self.grid.xspacing*len(cols)
        height = self.grid.yspacing
        return Rect(x, y, width, height)
    
    def resize(self, newcols):
        self.cols = newcols
        self.rect = self.makeRect()
    
    def calculateCols(self, newcol):
        return [newcol]
    
    def add(self, floating, row, col):
        if row == self.row:
            cols = self.calculateCols(col)
            self.children += [guiShard(floating, self, row+1, cols)]
        else:
            for c in self.children:
                if col in c.cols:
                    c.add(floating, row, col)
                    return
            print 'no child covers col', col
            


if __name__ == '__main__':
    from gui import *
    main()