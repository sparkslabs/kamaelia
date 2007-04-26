#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#
# Simple game which can keep small children happy :-)
#
# Bounces images round the screen, rotating, scaling etc. Left clicking
# makes a beep and adds an image, right clicking removes. Nice and simple
# game for small kids :)
#
# Provides a basis for simple games.
#
# Left mouse button - Add an image
# Right mouse button - Remove an image (if over an image, that image)
# Middle mouse button - freeze/unfreeze a moving image if over an image
# Key "P" - Freeze (Pause) all images. (Can still add new moving images)
# Key "U" - Unfreeze (Unpause) all images.
# Key "T" - Pause all moving things, unpause all not moving things (toggle)
# Key "Q" - Quit
#

import pygame
import random
import os

from Kamaelia.Chassis.Graphline import Graphline

from Kamaelia.Automata.Behaviours import bouncingFloat, cartesianPingPong, loopingCounter, continuousIdentity, continuousZero, continuousOne
from Kamaelia.UI.Pygame.EventHandler import EventHandler
from Kamaelia.Util.Fanout import Fanout
from Sprites.BasicSprite import BasicSprite
from Sprites.SpriteScheduler import SpriteScheduler

banner_location = "banner.gif"
cat_location    = "cat.gif"
cat_pop_wav_file     = "hold.wav"
cat_appear_wav_file  = "KDE_Beep_Bottles.wav"
screensize      = (700,550)
back_colour     = (255,255,255)
border          = 40
flags = pygame.DOUBLEBUF # | pygame.FULLSCREEN # 

cat_pop_wav = pygame.mixer.Sound(cat_pop_wav_file)
cat_appear_wav = pygame.mixer.Sound(cat_appear_wav_file)

pygame.init()
# --------------------------------------------------------------------------

def makeAndInitialiseBackground(banner_location, screensize, 
                                screen_surface, back_colour):
    #
    # Load images for background
    #
    banner_surface = pygame.image.load(banner_location)
    banner = banner_surface.convert()
    surface = banner_surface
    width = banner_surface.get_width()
    height = banner_surface.get_height()

    #
    # Calculate position for image, relative to screen size.
    # This is calculated as a rectangle
    #
    horizonal_to_move = (screensize[0] - width)/2
    vertical_to_move = (screensize[1] - height)/2
    rect = banner_surface.get_rect()
    rect = rect.move([horizonal_to_move,vertical_to_move])

    # Create the actual background, and then insert the image(s) into the
    # background.
    #
    background = pygame.Surface(screen_surface.get_size())
    background = background.convert()
    background.fill(back_colour)
    background.blit(banner_surface, rect)

    #
    # Finally, return the completed background.
    #
    return background

def randomFromRangeExcludingZero(min,max):
    result = 0
    while result == 0:
        result = random.randint(min,max)
    return result

def make_cat(cat_location, screensize, border ):
    # Get the cat again!
    files = list()
    for x in os.listdir("pictures"):
        if x not in ("README","CVS",".svn"):
            files.append(x)

    image_location = files[random.randint(0,len(files)-1)]

    cat_surface = pygame.image.load("pictures/"+image_location)
    cat = cat_surface.convert()
    cat.set_colorkey((255,255,255), pygame.RLEACCEL)

    rotation_speed = randomFromRangeExcludingZero(-2,2)  
    scale_speed = float(randomFromRangeExcludingZero(-1,1))
    position = list( (random.randint(border,screensize[0]-border),
                     random.randint(border,screensize[1]-border)))

    newCat = BasicSprite(image=cat)

    X = Graphline(
       newCat = newCat,
       rotator = loopingCounter(rotation_speed),
       translation = cartesianPingPong(position,screensize[0],screensize[1],border),
       scaler = bouncingFloat(scale_speed),
       imaging = continuousIdentity(cat),
       shutdown_fanout = Fanout(["rotator","translation","scaler", "imaging","self_shutdown"]),
       linkages = {
           ("rotator","outbox" ) : ("newCat", "rotator"),
           ("translation","outbox" ) : ("newCat", "translation"),
           ("scaler","outbox" ) : ("newCat", "scaler"),
           ("imaging","outbox" ) : ("newCat", "imaging"),
           ("newCat", "signal" ): ("shutdown_fanout", "inbox"),
           ("shutdown_fanout", "rotator") : ("rotator", "control"),
           ("shutdown_fanout", "translation") : ("translation", "control"),
           ("shutdown_fanout", "scaler") : ("scaler", "control"),
           ("shutdown_fanout", "imaging") : ("imaging", "control"),
           ("shutdown_fanout", "self_shutdown") : ("shutdown_fanout", "control"),
       }
    ).activate()

    return newCat

def make_cats(cat_location, screensize, border, numberCats=20):
    cat_sprites = []
    for i in range(numberCats):
        # Need to load the image separately for each sprite...
        newCat = make_cat(cat_location, screensize, border)
        cat_sprites.append(newCat)
    return cat_sprites

class MyGamesEvents(EventHandler):
    def __init__(self, cat_args, trace=1, ):
        self.trace = 0
        self.cat_args = cat_args
    def mousebuttondown(self, pos, button, where):
        if button == 1:
            channel = cat_appear_wav.play()
            newCat = make_cat(*self.cat_args)
            cat_sprite = newCat
            where.allsprites.add(cat_sprite)
        if button == 2:
            sprites = where.allsprites.sprites()
            for sprite in sprites:
                if sprite.rect.collidepoint(*pos):
                    sprite.toggleFreeze()
        if button == 3:
           # Make a sprite disappear
           channel = cat_pop_wav.play()
           sprites = where.allsprites.sprites()
           popped = 0
           for sprite in sprites:
               if sprite.rect.collidepoint(*pos):
                   spriteToZap = sprite
                   spriteToZap.shutdown()
                   where.allsprites.remove(spriteToZap)
                   return
           try:
               spriteToZap = sprites[len(sprites)-1]
           except IndexError:
               pass
           else:
               spriteToZap.shutdown()
               where.allsprites.remove(spriteToZap)
    def keydown(self, unicode, key, mod, where):
        if key == 112: # "P"
            # PAUSE ALL MOVEMENT
            for sprite in where.allsprites.sprites():
                sprite.freeze()
        if key == 113: # "Q"
            raise "QUIT"
        if key == 117: # "U"
            # UNPAUSE ALL MOVEMENT
            for sprite in where.allsprites.sprites():
                sprite.unfreeze()
        if key == 116: # "T"
            # Toggle PAUSE ALL MOVEMENT
            for sprite in where.allsprites.sprites():
                sprite.toggleFreeze()

# screen_surface = pygame.display.set_mode(screensize, DOUBLEBUF|FULLSCREEN)
screen_surface = pygame.display.set_mode(screensize, flags)
background = makeAndInitialiseBackground(banner_location, screensize, screen_surface,back_colour)
cat_sprites = make_cats(cat_location, screensize, border,1)
cat_args = (cat_location, screensize, border)

try:
    SpriteScheduler(cat_args, cat_sprites, background, screen_surface, MyGamesEvents).run()
except:
    pass

