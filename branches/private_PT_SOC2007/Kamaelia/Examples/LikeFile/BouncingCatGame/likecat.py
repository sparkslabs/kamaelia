#!/usr/bin/env python


# testing a sprite-based system with likefile parts.

from Axon.LikeFile import likefile, schedulerThread
import time, Axon
from Sprites.BasicSprite import BasicSprite
from Sprites.SpriteScheduler import SpriteScheduler
from Simplegame import *


class catMaker(Axon.Component.component):
    """discards input, makes one cat per item on inbox."""
    def main(self):
        self.spritescheduler = SpriteScheduler(cat_args, cat_sprites, background, screen_surface, MyGamesEvents).activate()
        yield 1 # to make sure spritescheduler's main gets called once - there's code outside the loop there that needs to run.
        while True:
            while self.dataReady("inbox"):
                discardedfornow = self.recv("inbox")
                cat_appear_wav.play()
                self.spritescheduler.allsprites.add(make_cat(*self.spritescheduler.cat_args))
            self.pause()
            yield 1

bg = schedulerThread(slowmo=0.01).start()
catmaker = likefile(catMaker())

max_cats = 10
for i in xrange(0, max_cats):
    time.sleep(0.5)
    catmaker.put(i)
print "cats over!"
time.sleep(5)
