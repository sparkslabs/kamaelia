
print "loading Actions"
import pygame

def main(x):
   print x

def pink(self,*args):
    self.background = 0xF6D0D2
    self.redraw()

def blue(self,*args):
    self.background = 0xD2D0F6
    self.redraw()

def foo(self,*args):
    pygame.draw.line(self.display, (0,0,0), (self.x-5,self.y),(self.x+5,self.y),self.width)
    pygame.draw.line(self.display, (0,0,0), (self.x+5,self.y),(self.x,self.y+20),self.width)
    pygame.draw.line(self.display, (0,0,0), (self.x, self.y+20),(self.x-5,self.y),self.width)
    self.dirty = True

def move(self, *args):
    if len(args) == 2:
        P = [ int(x) for x in args ]
        self.x = P[0]
        self.y = P[1]
        foo(self)

def line(self, *args):
    if len(args) == 4:
        P = [ int(x) for x in args ]
        pygame.draw.line(self.display, self.colour, (P[0],P[1]),(P[2],P[3]),self.width)
        self.dirty = True
    else:
        print "Hmm", repr(args)

def setwidth(self, *args):
    if len(args) == 1:
        self.width = int(args[0])

def setcolour(self, *args):
    if len(args) == 3:
        self.colour = [ int(x) for x in args ]

def quit(self,*args):
    raise "CRASH AND BURN!!!!"

actions = [
   ("pink", pink),
   ("blue", blue),
   ("foo", foo),
   ("move", move),
   ("line", line),
   ("quit", quit),
   ("colour", setcolour),
   ("width", setwidth),
]
