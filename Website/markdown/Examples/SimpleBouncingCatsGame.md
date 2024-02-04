---
pagename: Examples/SimpleBouncingCatsGame
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook Example]{style="font-size:24pt;font-weight:600"}

[How can I\...?]{style="font-size:18pt"}

Example 9 : Simple component based game using pygame. This demonstrates
use of a collection of simple physics behaviours components, Graphline
to bind these to a BasicSprite component, an EventHandler to show how to
deal with keyboard handling, a fanout component to help co-ordinate
shutdown, and a specialised scheduler - the SpriteScheduler component to
run these. [Components used:
]{style="font-weight:600"}[Graphline](/Components/pydoc/Kamaelia.Util.Graphline.Graphline.html),
[BasicSprite](/Components/pydoc/Kamaelia.UI.Pygame.BasicSprite.BasicSprite.html),
[SpriteScheduler](/Components/pydoc/Kamaelia.UI.Pygame.SpriteScheduler.SpriteScheduler.html),
[EventHandler]{style="font-style:italic;color:#ff0004"},
[fanout](/Components/pydoc/Kamaelia.Util.Fanout.fanout.html),
[bouncingFloat](/Components/pydoc/Kamaelia.Physics.Behaviours.bouncingFloat.html),
[cartesianPingPong](/Components/pydoc/Kamaelia.Physics.Behaviours.cartesianPingPong.html),
[loopingCounter](/Components/pydoc/Kamaelia.Physics.Behaviours.loopingCounter.html),
[continuousIdentity](/Components/pydoc/Kamaelia.Physics.Behaviours.continuousIdentity.html),
[continuousZero](/Components/pydoc/Kamaelia.Physics.Behaviours.continuousZero.html),
[continuousOne](/Components/pydoc/Kamaelia.Physics.Behaviours.continuousOne.html)

[Warnings]{style="font-weight:600"}: if you\'re less than 4 you\'ll love
this game ;-) Also, This isn\'t quite integrated with the PyGameApp
code, but shows a nice way of writing simple games.

```{.python}
#!/usr/bin/python

import pygame
import random
import os

from Kamaelia.Util.Graphline import Graphline
from Kamaelia.UI.Pygame.BasicSprite import BasicSprite
from Kamaelia.Physics.Behaviours import bouncingFloat, cartesianPingPong, loopingCounter, continuousIdentity,  continuousZero, continuousOne
from Kamaelia.UI.Pygame.EventHandler import EventHandler
from Kamaelia.Util.Fanout import fanout
from Kamaelia.UI.Pygame.SpriteScheduler import SpriteScheduler

banner_location = "banner.gif"
cat_location    = "cat.gif"
cat_pop_wav_file     = "hold.wav"
cat_appear_wav_file  = "KDE_Beep_Bottles.wav"
screensize      = (700,550)
back_colour     = (255,255,255)
border          = 40
flags = pygame.DOUBLEBUF

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
        if x not in ("README","CVS"):
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
       shutdown_fanout = fanout(["rotator","translation","scaler", "imaging","self_shutdown"]),
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
                    sprite.togglePause()
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
                sprite.pause()
        if key == 113: # "Q"
            raise "QUIT"
        if key == 117: # "U"
            # UNPAUSE ALL MOVEMENT
            for sprite in where.allsprites.sprites():
                sprite.unpause()
        if key == 116: # "T"
            # Toggle PAUSE ALL MOVEMENT
            for sprite in where.allsprites.sprites():
                sprite.togglePause()

screen_surface = pygame.display.set_mode(screensize, flags)
background = makeAndInitialiseBackground(banner_location, screensize, screen_surface,back_colour)
cat_sprites = make_cats(cat_location, screensize, border,1)
cat_args = (cat_location, screensize, border)

try:
    SpriteScheduler(cat_args, cat_sprites, background, screen_surface, MyGamesEvents).run()
except:
    pass
```

**Source:** Examples/example9/Simplegame.py

