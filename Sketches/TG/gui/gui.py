import pygame
from pygame import display
from pygame.locals import *
from pygame.color import THECOLORS as colours
from pygame.draw import *
from pygame.rect import *

from toolbar import toolbar
from box import box
from cancel import cancel
from grid import grid
from container import container

def main():
    pygame.init()
    screen = display.set_mode((640, 480))
    display.set_caption('shard gui')
    
    screen.fill(colours['white'])
    pygame.display.update()
    
    t = toolbar(things = [box('label.png'), box('label.png')])
    c = cancel('label.png')
    t.add(c)
    g = grid(screen, 0, t.height, screen.get_width(), screen.get_height()-t.height)
    
    con = container(t, g, screen)
    
    done = False
    while not done:
        rs = con.draw(screen)
        display.update(rs)
        
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
                con.handleEvent(e)

    return


if __name__ == '__main__':
    main()