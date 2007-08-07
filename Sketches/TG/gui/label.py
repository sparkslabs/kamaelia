from box import box

from pygame.color import THECOLORS as colours
from pygame import font

class label(box):
    def __init__(self, imname, text, x = 0, y = 0):
        super(label, self).__init__(imname, x, y)
        
        self.font = font.SysFont("Times New Roman", 25)
        self.colour = colours['blue']
        
        textim = self.font.render(text, True, self.colour)
        
        self.xborder = (self.width - textim.get_width())/2
        self.yborder = (self.height - textim.get_height())/2
        
        self.surface.blit(textim, (self.x + self.xborder, self.y + self.yborder))
        

class cancel(label):
    def __init__(self, imname, x = 0, y = 0):
        super(cancel, self).__init__(imname, 'cancel', x, y)
        
        self.redraw = None
    
    def handleMouseDown(self, e):
        if self.container().floating:
            self.redraw = self.container().floating.erase(self.container().screen)
            self.container().floating = None
    
    def draw(self, surface):
        r = super(cancel, self).draw(surface)
        if self.redraw:
            r += self.redraw
        
        return r

class clear(label):
    def __init__(self, imname, x = 0, y = 0):
        super(clear, self).__init__(imname, 'clear', x, y)
    
    def handleMouseDown(self, e):
        self.container().grid.clear()


if __name__ == '__main__':
    from gui import *
    main()