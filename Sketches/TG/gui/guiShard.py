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
        self.minwidth = 1
        
        self.parent = parent
        self.children = []
    
    def draw(self, surface):
        rect(surface, self.colour, self.makeRect(), 0)
        for c in self.children:
            c.draw(surface)
    
    def makeRect(self):
        x = self.grid.colCoord(self.cols[0])
        y = self.grid.rowCoord(self.row)
        width = self.grid.xspacing*len(self.cols)
        height = self.grid.yspacing
        return Rect(x, y, width, height)
    
    def centre(self):
        return self.makeRect().centerx
    
    def resize(self, newcols):
        self.cols = list(newcols)
    
    def addChild(self, floating, index):
        # column 0 given as a temporary value
        self.children.insert(index, guiShard(floating, self, self.row+1, [0]))
        self.repack()
        self.minwidth += 1
    
    def newChildIndex(self, newx):
        for c in self.children: # assumes children ordered in display l-r
            if x < c.centre():
                return self.children.index(c)
        return len(self.children) # if no child applies, new is last
    
    # doesn't repack children's children etc.
    def repack(self):
        if not self.children:
            return
        totalminw = 0
        for c in self.children:
            totalminw += c.minwidth
        
        rem = len(self.cols) - totalminw
        if rem < 0:
            print 'error, not enough room'
            return
        else:
            sizes = [(c.minwidth, c) for c in self.children]
            while rem != 0:
                sizes.sort()
                sizes[0] = (sizes[0][0]+1, sizes[0][1]) # increment width
                rem -= 1 # decrement spare cols
            
            # sort into child order
            sizes.sort(lambda x,y: self.children.index(x[1]) - self.children.index(y[1]))
            widths = [c[0] for c in sizes]            
            starts = [sum(widths[0:i]) + self.cols[0] for i in xrange(0, len(widths))]
            print starts
            ends = [widths[i] + starts[i] for i in xrange(0, len(starts))]
            for i in xrange(0, len(sizes)):
                child = sizes[i][1]
                newcols = range(starts[i], ends[i])
                #print newcols
                child.resize(newcols)
                child.repack()
            print
    
    def add(self, floating, row, x):
        if row == self.row:
            self.addChild(floating, self.newChildIndex(x))
        else:
            col = self.grid.snapToCol(x)
            for c in self.children:
                if col in c.cols:
                    c.add(floating, row, col)
                    return
            print 'no child covers col', col
    
    def __str__(self):
        return 'r'+str(self.row)+'/cs'+ str(self.cols)
    
    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    from gui import *
    main()