import pygame
# uses methods defined in Drawing

class MouseEventHandler:
    """
    Code adapted slightly from MagnaDoodle.py and moved into separate module
    Methods added back to ShardMagnaDoodle using shard wrapper function
    """
    def handleMouseDown(self, event):
        if event.button == 1:
            self.drawing = True
        elif event.button == 3:
            self.oldpos = None
            
            # in Drawing
            self.drawBG()
            self.blitToSurface()
      
    def handleMouseUp(self, event):
        if event.button == 1:
            self.drawing = False
            self.oldpos = None
      
    def handleMouseMotion(self, event):
        if self.drawing and self.innerRect.collidepoint(*event.pos):
            if self.oldpos == None:
                self.oldpos = event.pos
            else:
                pygame.draw.line(self.display, (0,0,0), self.oldpos, event.pos, 3)
                self.oldpos = event.pos
            self.blitToSurface() # in Drawing
      
    def handleMouseEvents(self, fromBox = "inbox"):
        while self.dataReady(fromBox):
            for event in self.recv(fromBox):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleMouseDown(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handleMouseUp(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.handleMouseMotion(event)
   
    def registerMouseListeners(self):
        self.send( { "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                            "surface" : self.display},
                            "display_signal")
      
        self.send( { "ADDLISTENEVENT" : pygame.MOUSEBUTTONUP,
                            "surface" : self.display},
                            "display_signal")
      
        self.send( { "ADDLISTENEVENT" : pygame.MOUSEMOTION,
                            "surface" : self.display},
                            "display_signal")
    
    def test(self):
        print repr(self)