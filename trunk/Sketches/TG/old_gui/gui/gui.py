# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pygame
from pygame import display
from pygame.locals import *
from pygame.color import THECOLORS as colours
from pygame.draw import *
from pygame.rect import *

from toolbar import toolbar
from box import box
from label import cancel, clear
from grid import grid
from container import container
from arrows import forward, back

def main():
    pygame.init()
    screen = display.set_mode((640, 480))
    display.set_caption('shard gui')
    
    screen.fill(colours['white'])
    pygame.display.update()
    
    t = toolbar(things = [box('label.png'), box('label.png')])
    c = cancel('label.png')
    cl = clear('label.png')
    f = forward('label.png')
    b = back('label.png')
    t.add([c, cl, b, f])
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