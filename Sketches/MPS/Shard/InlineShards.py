#
# This is where we will put shards that come from *inside* the main method.
#
#
def MOUSEBUTTONDOWN_handler(self):
    if  event.button == 1:
        self.drawing = True
    elif event.button == 3:
        self.oldpos = None
        self.drawBG()
        self.blitToSurface()

def MOUSEBUTTONUP_conditional_handler(self):
    self.drawing = False
    self.oldpos = None

def MOUSEMOTION_handler(self):
    if self.drawing and self.innerRect.collidepoint(*event.pos):
        if self.oldpos == None:
            self.oldpos = event.pos
        else:
            pygame.draw.line(self.display, (0,0,0), self.oldpos, event.pos, 3)
            self.oldpos = event.pos
        self.blitToSurface()
