#!/usr/bin/env python 

import pygame
from pygame.locals import *
import string

screen_width=400
screen_height=300
tabs_height = 100
text_height=18
background_color = (255,255,255)
text_color=(0,0,0)
        
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
screenRect = screen.get_rect()
screen.fill(background_color)

scratch = screen.copy()
font = pygame.font.Font(None, 14)
linelen = screen_width/font.size('a')[0]
keepRect = pygame.Rect((0, text_height), (screen_width, screen_width-text_height))
scrollingRect = pygame.Rect((0, 0), (screen_width, screen_height - text_height))
writeRect = pygame.Rect((0, screen_height-text_height), (screen_width, text_height))

def setText(text):
    screen.fill(background_color)
    update(text)
    
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

pygame.display.update()
done = False
string_buffer = ""
while not done:
    for event in pygame.event.get():
        if (event.type == KEYDOWN):
            char = event.unicode
            if char == '\n' or char == '\r':
                print string_buffer
                string_buffer = ''
            elif event.key == K_BACKSPACE:
                string_buffer = string_buffer[:len(string_buffer)-1]
            elif event.key == K_ESCAPE:
                done = True
            else:
                string_buffer += char
            setText(string_buffer)
