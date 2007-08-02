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

class im(Image):
    def event(self, e):
        if (e.type == KEYDOWN):
            if(e.key == K_b):
                print'b'
                self.blur()

def onclick(value):
    print 'click',value

def toggle(imold, imnew, container):
    container.remove(imold)
    container.add(imnew, 0, 0)

c = Container()
image = im('bsqer.png')
otherim = im('sqer.png')
image.connect(CLICK, onclick, 'pop')
c.add(image, 0, 0)
c.connect(CLICK, toggle, image, otherim, c)
Desktop().run(c, screen)

def main():
    while 1:
        for e in pygame.event.get():
            if( e.type == QUIT ):
                return
            elif (e.type == KEYDOWN):
                if(e.key == K_ESCAPE):
                    return
                if(e.key == K_b):
                    image.blur()
        d.update(screen)

#d = Desktop()
#d.init(image, screen)
#main()