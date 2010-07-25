# -*- coding: utf-8 -*-
#simple scrolling textbox using Pygame
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
import time
import sys

def update(text):
    while len(text) > linelen:
        cutoff = text.rfind(' ', 0, linelen)
        updateLine(text[0:cutoff])
        text = text[cutoff + 1:]
    updateLine(text)
        
def updateLine(line):            
    lineSurf = font.render(line, True, text_color)    
    screen.fill(background_color)
    screen.blit(scratch, scrollingRect, keepRect)
    screen.blit(lineSurf, writeRect)
    scratch.fill(background_color)
    scratch.blit(screen, screen.get_rect())
    pygame.display.update()

## initialize the pygame stuff. The output window.
WHITE = (255, 255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255, 0,0)
screen_width=400
screen_height=300
tabs_height = 100
text_height=18
background_color = (255,255,255)
text_color=(0,0,0)
        
pygame.init()
screen = pygame.Surface((screen_width, screen_height))
screenRect = screen.get_rect()
screen.fill(background_color)

scratch = screen.copy()
font = pygame.font.Font(None, 14)
linelen = screen_width/font.size('a')[0]
keepRect = pygame.Rect((0, text_height), (screen_width, screen_width-text_height))
scrollingRect = pygame.Rect((0, 0), (screen_width, screen_height - text_height))
writeRect = pygame.Rect((0, screen_height-text_height), (screen_width, text_height))

window = pygame.display.set_mode((screen_width, screen_height+ tabs_height))
tabpane = pygame.Surface((screen_width, tabs_height))
tabpane.fill(BLUE)
tabRect = tabpane.get_rect()
tabRect.topleft = (0, 200)
window.blit(tabpane, tabRect)
screenRect.topleft = (0,0)
window.blit(screen, screenRect)

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
