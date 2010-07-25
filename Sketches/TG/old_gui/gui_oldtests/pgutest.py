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