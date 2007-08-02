from pygame.rect import Rect

class floating(object):
    def __init__(self, startx, starty, label):
        
        self.label = label
        
        self.x = startx
        self.y = starty
        self.width = label.width
        self.height = label.height
        
        self.surface = label.surface.copy()
        self.surface.set_alpha(100)
        
        self.oldsurf = label.surface.copy()
        
        self.oldx = startx
        self.oldy = starty
    
    def handleMouseMove(self, e):
        self.x, self.y = e.pos
    
    def bounds(self):
        return Rect(self.x, self.y, self.width, self.height)
    
    def container(self):
        return self.label.container()
    
    def erase(self, surface):
        r = [Rect(self.oldx, self.oldy, self.width, self.height)]
        surface.blit(self.oldsurf, (self.oldx, self.oldy))
        self.oldx = self.x
        self.oldy = self.y
        self.oldsurf = surface.subsurface(self.bounds()).copy()
        return r
    
    def draw(self, surface):
        if not surface.get_rect().contains(self.bounds()):
            return []
        
        if self.container().grid.contains(self.x, self.y):
            self.x, self.y = self.container().grid.snapToGrid(self.x, self.y)
        
        r = self.erase(surface)        
        surface.blit(self.surface, (self.x, self.y))
        return r + [self.bounds()]


if __name__ == '__main__':
    from gui import *
    main()