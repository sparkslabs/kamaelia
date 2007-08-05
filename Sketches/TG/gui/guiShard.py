from pygame.draw import rect
from pygame.color import THECOLORS as colours
from pygame.rect import Rect

from random import randint

def pickColour():
    return colours.values()[randint(0, len(colours)-1)]

class guiShard(object):
    def __init__(self, floating, parent, row, cols):
        
        self.floating = floating
        self.colour = pickColour()
        
        self.grid = floating.container().grid
        
        self.row = row
        self.cols = cols
        
        x = self.grid.colCoord(self.cols[0])
        y = self.grid.rowCoord(self.row)
        width = self.grid.xspacing*len(cols)
        height = self.grid.yspacing
        self.rect = Rect(x, y, width, height)
        
        self.parent = parent
        self.children = [] # dict? need occupied cols info?
    
    def draw(self, surface):
        rect(surface, self.colour, self.rect, 0)
        for s in self.children:
            s.draw(surface)
    
    def add(self, floating, row, col):
        if row == self.row:
            cols = [col]  # work out which cols it should cover
            self.children += [guiShard(floating, self, row+1, cols)]
        else:
            #find correct child and call add() on it
            pass


if __name__ == '__main__':
    from gui import *
    main()