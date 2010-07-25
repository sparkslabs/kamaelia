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