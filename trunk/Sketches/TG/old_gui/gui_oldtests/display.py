from math import pi

# PyGame Constants
import pygame
import pygame.font
from pygame.locals import *
from pygame.color import THECOLORS as colours
from pygame.draw import *
from pygame.rect import *

class toolbar(object):
    floating = None
    
    def __init__(self, surface, things = [], x = 0, y = 0):
        """
        things must have width and height attributes and a draw() method;
        x and y attributes for drawing from top-left corner are also
        assumed (set but not read)
        """
        
        self.surface = surface
        self.border = 1
        self.colour = colours['black']
        self.x = x
        self.y = y
        self.things = []
        self.endx = x
        
        for t in things:
            self.add(t)
    
    def width(self):
        return self.endx - self.x + self.border
    
    def height(self):
        return max([t.height for t in self.things])# + 2*self.border
    
    def makeRect(self):
        return Rect(self.x, self.y, self.width(), self.height())
    
    def add(self, thing):
        self.things += [thing]
        
        thing.parent = self
        thing.x = self.endx + self.border
        thing.y = self.y + self.border
        
        self.endx += thing.width + self.border
        self.rect = self.makeRect()
    
    def handleEvent(self, e):
        if e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            thing = self.findThing(x, y)
            if thing:
                thing.handleMouseDown(e)
        elif e.type == MOUSEMOTION:
            if self.floating:
                self.floating.handleMouseMove(e)
    
    def findThing(self, x, y):
        if y > self.height():
            return None
        
        for t in self.things:
            if (t.x + t.width) >= x:
                return t
        return None
    
    def draw(self, surface = None):
        if not surface:
            surface = self.surface
        
        rect(surface, self.colour, self.makeRect())
        if self.floating:
            self.floating.draw(surface)
        for t in self.things:
            t.draw(surface)

class box(object):
    def __init__(self, imname, x = 0, y = 0):
        self.surface = pygame.image.load(imname).convert()
        self.x = x
        self.y = y
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.parent = None # set by toolbar when added
    
    def handleMouseDown(self, e):
        if self.parent.floating:
            self.parent.floating.erase(self.parent.surface)
        
        self.parent.floating = floating(self.x, self.y, self)
    
    def draw(self, surface = None):
        if not surface:
            surface = parent.surface
        
        surface.blit(self.surface, (self.x, self.y))

class cancel(box):
    def __init__(self, imname, x = 0, y = 0):
        super(cancel, self).__init__(imname, x, y)
                
        self.font = pygame.font.SysFont("Times New Roman", 25)
        textim = self.font.render('cancel', True, colours['blue']) #.convert() #fills in surface completely...
        self.xborder = (self.width - textim.get_width())/2
        self.yborder = (self.height - textim.get_height())/2
        
        self.surface.blit(textim, (self.x + self.xborder, self.y + self.yborder))
    
    def handleMouseDown(self, e):
        if self.parent.floating:
            self.parent.floating.erase(self.parent.surface)
            self.parent.floating = None

class floating(object):
    def __init__(self, startx, starty, parent):
        self.parent = parent
        self.x = startx
        self.y = starty
        self.width = parent.width
        self.height = parent.height
        
        self.surface = parent.surface.copy()
        self.surface.set_alpha(100)
        
        self.oldsurf = parent.surface.copy()
        
        self.oldx = startx
        self.oldy = starty
    
    def handleMouseMove(self, e):
        self.x, self.y = e.pos
    
    def erase(self, surface):
        surface.blit(self.oldsurf, (self.oldx, self.oldy))
        self.oldx = self.x
        self.oldy = self.y
        self.oldsurf = surface.subsurface((self.x, self.y, self.width, self.height)).copy()
    
    def draw(self, surface):
        if not surface.get_rect().contains((self.x, self.y, self.width, self.height)):
            return
        
        self.erase(surface)        
        surface.blit(self.surface, (self.x, self.y))

class grid(object):
    def __init__(self, surface, x, y, xspacing = 75, yspacing = 36):
        self.x = x
        self.y = y
        self.xspacing = xspacing
        self.yspacing = yspacing
        self.border = 1
        self.colour = colours['grey90']
        
        w = surface.get_width() - self.x
        h = surface.get_height() - self.y
        
        cols = w % self.xspacing
        rows = h % self.yspacing
        
        #self.width = 
        
        for i in xrange(0, cols):
            line(surface, self.colour, (i*self.xspacing, self.y), (i*self.xspacing, h))
        for i in xrange(0, rows):
            line(surface, self.colour, (self.x, i*self.yspacing), (w, i*self.yspacing))
    
    def snaptogrid(self, x, y):
        return x, y
    
    def draw(self, surface):
        w = surface.get_width() - self.x
        h = surface.get_height() - self.y
        
        cols = w % self.xspacing
        rows = h % self.yspacing
        
        for i in xrange(0, cols):
            line(surface, self.colour, (i*self.xspacing, self.y), (i*self.xspacing, h))
        for i in xrange(0, rows):
            line(surface, self.colour, (self.x, i*self.yspacing), (w, i*self.yspacing))

class container(object):
    def __init__(self, toolbar, grid, screen):
        self.toolbar = toolbar
        self.grid = grid
        self.screen = screen
        self.surface = pygame.Surface((screen.get_width(), screen.get_height()))
    
    def draw(self, surface):
        # have draw methods return list of dirty rects to be updated
        self.toolbar.draw(surface)
        self.grid.draw(surface)

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('glom')
    
    screen.fill(colours["white"])
    
    t = toolbar(screen)
    b2 = box('sqer.png')
    b1 = box('bsqer.png')
    c = cancel('bsqer.png')
    t.add(b2)
    t.add(b1)
    t.add(c)
    g = grid(screen, 0, t.height())
    
    con = container(t, g, screen)
    
    done = False
    while not done:
        pygame.display.update(con.draw(screen))
            
        events = pygame.event.get()
        for e in events:
            if(e.type == QUIT):
                done = True
                break
            elif(e.type == KEYDOWN):
                if(e.key == K_ESCAPE):
                    done = True
                    break
            else:
                t.handleEvent(e)

    return
    
main()
