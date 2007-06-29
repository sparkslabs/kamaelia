#!/usr/bin/env python

#
# Proper likefile control of a sprite handler
#

from likefile import LikeFile, schedulerThread
import time, Axon, os, random, pygame, math, threading
from Sprites.BasicSprite import BasicSprite
from Sprites.SpriteScheduler import SpriteScheduler
from Kamaelia.UI.Pygame.EventHandler import EventHandler
from Simplegame import *

from Kamaelia.Automata.Behaviours import bouncingFloat, cartesianPingPong, loopingCounter, continuousIdentity, continuousZero, continuousOne
from Kamaelia.Util.Fanout import Fanout

bg = schedulerThread().start()

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

    newCat = CatSprite(image=cat)
    newCat.activate() # to register it with the sprite scheduler, this is a hack.

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
    )
    return X

cat_args = (cat_location, screensize, border)
spritescheduler = SpriteScheduler(cat_args, [], background, screen_surface, MyGamesEvents).activate()

catlist = []
while True:
    input = raw_input(">>> ").lower()
    try: command, args = input.split(' ', 1)
    except ValueError: command, args = input, ''

    if command == "status":
        print "there are %s threads active and %s components" % (threading.activeCount(), len(Axon.Scheduler.scheduler.run.threads))
    elif command == "add":
        count = 1
        if args and int(args) > 1: count = int(args)
        for i in xrange(1, count):
            newcat = LikeFile(make_cat(*cat_args))
            newcat.activate()
            catlist.append(newcat)
            print "added a cat."
            time.sleep(0.1)