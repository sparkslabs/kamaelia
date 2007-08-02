from pygame import image
from pygame.rect import Rect
from floating import floating

class box(object):
    def __init__(self, imname, x = 0, y = 0):
        self.surface = image.load(imname).convert()
        self.x = x
        self.y = y
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.toolbar = None # set by toolbar when added
    
    def container(self):
        if self.toolbar:
            return self.toolbar.container
    
    def bounds(self):
        return Rect(self.x, self.y, self.width, self.height)
    
    def handleMouseDown(self, e):
        if self.container().floating:
            self.container().floating.erase(self.container().screen)
        
        self.container().floating = floating(self.x, self.y, self)
    
    def draw(self, surface):   
        surface.blit(self.surface, (self.x, self.y))
        return [self.bounds()]


if __name__ == '__main__':
    from gui import *
    main()