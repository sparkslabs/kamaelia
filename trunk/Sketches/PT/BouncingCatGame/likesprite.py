#!/usr/bin/env python

#
# Proper likefile control of a sprite handler
#

from likefile import LikeFile, schedulerThread
import time, Axon, os, random, pygame
from Sprites.BasicSprite import BasicSprite
from Sprites.SpriteScheduler import SpriteScheduler
from Kamaelia.UI.Pygame.EventHandler import EventHandler
from Simplegame import cat_location, screensize, border, background, screen_surface, randomFromRangeExcludingZero

bg = schedulerThread(slowmo=0.01).start()

global spritescheduler


class MyGamesEvents(EventHandler):
    def __init__(self, cat_args, trace=1, ):
        self.trace = 0
        self.cat_args = cat_args
    def keydown(self, unicode, key, mod, where):
        if key == 113: # "Q"
            raise "QUIT"

class CatSprite(BasicSprite):
    def main(self):
        spritescheduler.allsprites.add(self)
        while True:
            self.pause()
            yield 1

def make_cat(cat_location, screensize, border):
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

    newCat = CatSprite(image=cat)
    return newCat

cat_args = (cat_location, screensize, border)
spritescheduler = SpriteScheduler(cat_args, [], background, screen_surface, MyGamesEvents).activate()

newcat = make_cat(*cat_args)
time.sleep(1)

likecat = LikeFile(make_cat(*cat_args), extrainboxes="rotator")
likecat.activate()
for x in xrange(0, 360):
    time.sleep(0.01)
    likecat.put(x, "rotator")