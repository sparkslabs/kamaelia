import pygame

"""
Code adapted slightly from MagnaDoodle.py and moved into separate module
"""
    
def displaySetup(self, bgcolour, fgcolour, margin, size, transparent, position):
    """Test docstring for getshard() to parse"""
    self.backgroundColour = bgcolour
    self.foregroundColour = fgcolour
    self.margin = margin
    self.oldpos = None
    self.drawing = False
        
    self.size = size
    self.innerRect = pygame.Rect(10, 10, self.size[0]-20, self.size[1]-20)
        
    if transparent:
        transparency = bgcolour
    else:
        transparency = None
        
    self.disprequest = {"DISPLAYREQUEST" : True,
                                    "callback" : (self,"callback"),
                                    "events" : (self, "inbox"),
                                    "size": self.size,
                                    "transparency" : transparency}
    if not position is None:
        self.disprequest["position"] = position
            
def drawBG(self): # no docstring case for getshard() to parse
    self.display.fill( (255,0,0) )
    self.display.fill( self.backgroundColour, self.innerRect )
      
def blitToSurface(self):
    """
    Test docstring for getshard() to parse
    """
    self.send({"REDRAW":True, "surface":self.display}, "display_signal")
