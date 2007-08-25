from pygame.rect import Rect
from pygame.draw import rect
from pygame.locals import *
from pygame.color import THECOLORS as colours

class toolbar(object):
    
    def __init__(self, things = [], height = 0, x = 0, y = 0):
        """
        things must have width and height attributes and a draw() method;
        x and y attributes for drawing from top-left corner are also
        assumed (set but not read)
        things must be the same height; either height or at least one thing
        must be given, preferably a thing
        """
        
        self.container = None #set by container when added
        self.border = 1
        self.colour = colours['black']
        self.x = x
        self.y = y
        self.things = []
        self.endx = x
        if not things:
            self.height = height
        else:
            self.height = things[0].height
        self.height += 2*self.border
        
        self.add(things)
    
    def width(self):
        return self.endx - self.x + self.border
    
    def bounds(self):
        return Rect(self.x, self.y, self.width(), self.height)
    
    def contains(self, x, y):
        return self.bounds().collidepoint(x, y)
    
    def add(self, things):
        self.things += list(things)
        
        for thing in things:
            thing.toolbar = self
            thing.x = self.endx + self.border
            thing.y = self.y + self.border
            
            self.endx += thing.width + self.border
        
        self.rect = self.bounds()
    
    def handleMouseDown(self, e):
        x, y = e.pos
        thing = self.findThing(x, y)
        if thing:
            thing.handleMouseDown(e)
    
    def findThing(self, x, y):
        if not self.contains(x, y):
            return None
        
        for t in self.things:
            if (t.x + t.width) >= x:
                return t
        return None
    
    def draw(self, surface):
        rect(surface, self.colour, self.bounds())
        d = [self.bounds()]
            
        for t in self.things:
            d += t.draw(surface)
        
        return d


if __name__ == '__main__':
    from gui import *
    main()