from pygame.draw import rect
from pygame.color import THECOLORS as colours
from pygame.rect import Rect

from random import randint

from gridparts import row, column

nicecolours = [c for k, c in colours.items() if not ('grey' in k or 'gray' in k or 'black' in k)]
darkcolours = [x for x in nicecolours if x[0]+x[1]+x[2] < 400]

def pickColour():
    return darkcolours[randint(0, len(darkcolours)-1)]

class guiShard(object):
    def __init__(self, floating, parent, row, cols):
        
        self.floating = floating
        self.grid = floating.container().grid
        self.shardGen = floating.shardGen
        
        self.colour = pickColour()
        
        self.row = row
        self.cols = cols
        
        for c in self.cols:
            c.add(self, row = row)
            self.row.add(self, col = c)
        
        self.parent = parent
        self.children = []
    
    # return shard code generator, see gui/shardGen.py
    def getShardGen(self):
        self.shardGen.children = [c.getShardGen() for c in self.children]
        return self.shardGen
    
    def draw(self, surface):
        rect(surface, self.colour, self.makeRect(), 0)
        for c in self.children:
            c.draw(surface)
    
    def makeRect(self):
        x = self.cols[0].x
        y = self.row.y
        width = self.row.colwidth*len(self.cols)
        height = self.row.height
        return Rect(x, y, width, height)
    
    def centre(self):
        return self.makeRect().centerx
    
    def minwidth(self):
        if not self.children: return 1
        else: return len(self.children)
    
    def resize(self, newcols):
        for c in self.cols:
            c.add(None, row = self.row)
            self.row.add(None, col = c)
        
        self.cols = list(newcols)
        for c in self.cols:
            c.add(self, row = self.row)
            self.row.add(self, col = c)
    
    def addChild(self, floating, index):
        # no columns given as a temporary value
        self.children.insert(index, guiShard(floating, self, self.row.next(), []))
        self.repack()
    
    # row, cols numbers changed to objects!
    def newChildIndex(self, newx):
        for c in self.children: # assumes children ordered in display l-r
            if newx < c.centre():
                return self.children.index(c) + self.cols[0]
        return len(self.children) + self.cols[0] # if no child applies, new is last
    
    def repack(self):
        if not self.children:
            return
        
        rem = self.spaceRemaining()
        sizes = [(c.minwidth(), c) for c in self.children]
        while rem != 0:
            sizes.sort()
            sizes[0] = (sizes[0][0]+1, sizes[0][1]) # increment width
            rem -= 1 # decrement spare cols
        
        # sort into child order
        sizes.sort(lambda x,y: self.children.index(x[1]) - self.children.index(y[1]))
        
        widths = [c[0] for c in sizes]            
        starts = [sum(widths[0:i])+self.cols[0] for i in xrange(0, len(widths))]
        ends = [widths[i] + starts[i] for i in xrange(0, len(starts))]
        for i in xrange(0, len(sizes)):
            child = sizes[i][1]
            newcols = range(starts[i], ends[i])
            child.resize(newcols)
            child.repack()
    
    def spaceRemaining(self):
        totalminw = sum([c.minwidth() for c in self.children])
        rem = len(self.cols) - totalminw
        return rem
    
    def childAt(self, col):
        for c in self.children:
            if col in c.cols:
                return c
    
    def add(self, floating, row, x):
        if row != self.row:
            col = self.grid.snapToCol(x)
            if self.children:
                self.childAt(col).add(floating, row, x)
                return
        
        if self.spaceRemaining():
            self.addChild(floating, self.newChildIndex(x))
        else:
            print 'error, not enough room'
    
    def handleMouseDown(self, x, y):
        # x, y relative to grid
        col = self.grid.snapToCol(x)
        row = self.grid.snapToRow(y)
        if row == self.row:
            self.grid.shardhist.add(self)
        else:
            if self.children:
                self.childAt(col).handleMouseDown(x, y)
    
    def __str__(self):
        return 'r'+str(self.row)+'/cs'+ str(self.cols)
    
    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    from gui import *
    main()