from pgu.gui.app import Desktop
from pgu.gui.basic import *
from pgu.gui import *

import pygame
from pygame.locals import *
from pygame.color import THECOLORS
from pygame.draw import *
from pygame.rect import *

pygame.init()
screen = pygame.display.set_mode((640, 480),0,8)
pygame.display.set_caption('glom')

d = Desktop()

c = Container(width=640,height=50)
b = Label('pop')
a = Label('Quit')
#c.add(b, 0, 0)
s = Spacer(4, b.style.height)
#c.add(s, b.style.width, 0)
#c.add(a, s.style.width+b.style.width, 0)

def onclick(val):
    print val

b.connect(CLICK, onclick, 'pop')
a.connect(CLICK, d.quit)

t = Table()

t.tr()
t.add(b)
t.add(s)
t.add(a)

c.add(t, 0, 0)

d.run(c, screen)