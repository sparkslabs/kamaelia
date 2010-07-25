#!/usr/bin/env python
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

# testing a sprite-based system with likefile parts.

from Axon.likefile import LikeFile, schedulerThread
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
catmaker = LikeFile(catMaker())
catmaker.activate()

max_cats = 10
for i in xrange(0, max_cats):
    time.sleep(0.5)
    catmaker.put(i)
print "cats over!"
time.sleep(5)