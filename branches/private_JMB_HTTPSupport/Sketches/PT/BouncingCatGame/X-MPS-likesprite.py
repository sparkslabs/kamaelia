#!/usr/bin/env python

#
# Proper likefile control of a sprite handler
#

from likefile import LikeFile, schedulerThread
import time, Axon, os, random, pygame, math
from Sprites.BasicSprite import BasicSprite
from Sprites.SpriteScheduler import SpriteScheduler
from Kamaelia.UI.Pygame.EventHandler import EventHandler
from Simplegame import cat_location, screensize, border, background, screen_surface, randomFromRangeExcludingZero
import Axon

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

    newCat = CatSprite(image=cat)
    return newCat

cat_args = (cat_location, screensize, border)
spritescheduler = SpriteScheduler(cat_args, [], background, screen_surface, MyGamesEvents).activate()


#newcat = make_cat(*cat_args)

class SolarSystem(Axon.ThreadedComponent.threadedcomponent):
    def __init__(self, *cat_args):
        super(SolarSystem, self).__init__()
        self.the_sun = LikeFile(make_cat(*cat_args), extrainboxes = ("translation", "imaging"))
        self.the_sun.activate()
        self.planet = LikeFile(make_cat(*cat_args), extrainboxes = ("translation", "rotator", "imaging"))
        self.planet.activate()
        self.sun_position = tuple([x/2 for x in screensize])
        self.planet_position = (screensize[0]/4.0, screensize[1]/2)
        self.planet_velocity = (0.0, 10)

    # ugh, I should be using numpy but it works, that's the important thing
    # This is merely a test of likefile. Really, kamaelia components should be written for a physics simulation like this.

    def acceleration(self, pos_planet, pos_sun):
        g = 200 # fudge factor
        # F = ma, but F is proportional to distance ** -2
        # neatly removing the need to calculate a square root for the distance
        direction = (pos_planet[0] - pos_sun[0], pos_planet[1] - pos_sun[1])
        magnitude = direction[0] ** 2 + direction[1] ** 2
        return tuple([g * x/magnitude for x in direction])

    def apply_acceleration_to_velocity(self, velocity, accn):
        return (velocity[0] + accn[0], velocity[1] + accn[1])

    def apply_velocity_to_position(self,position, velocity):
        return (position[0] + velocity[0], position[1] + velocity[1])

    def main(self):
        self.the_sun.put(self.sun_position, "translation")

        while True:
            time.sleep(0.01)
            self.planet.put(self.planet_position, "translation")
            accn = self.acceleration(self.sun_position, self.planet_position)
            self.planet_velocity = self.apply_acceleration_to_velocity(self.planet_velocity, accn)
            self.planet_position = self.apply_velocity_to_position(self.planet_position, self.planet_velocity)


SolarSystem(*cat_args).activate()

while 1:
   time.sleep(100)
