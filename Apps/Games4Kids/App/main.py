#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------

import Axon
import pygame
from Kamaelia.Chassis.Pipeline import Pipeline

from Kamaelia.Apps.Games4Kids.BasicSprite import BasicSprite
from Kamaelia.Apps.Games4Kids.SpriteScheduler import SpriteScheduler
from Kamaelia.Apps.Games4Kids.MyGamesEventsComponent import MyGamesEventsComponent
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Util.Console import ConsoleEchoer

class Quitter(Axon.Component.component):
    def main(self):
        self.pause()
        yield 1
        self.scheduler.stop()
        yield 1

Pipeline(
    KeyEvent( outboxes = { "outbox": ""},
              key_events = { pygame.K_q: ("start_up", "outbox") }),
    Quitter(),
).activate()

class PlayerAnalyser(Axon.Component.component):
    def main(self):
        players = {}
        while True:
            if not self.anyReady():
                self.pause()
                yield 1
            for update in self.Inbox("inbox"):
                player, pos = update
                players[player] = pos
#            print "woo", players
            self.send(players, "outbox") # XXXX Note this is broken
            yield 1

import math

class Distancer(Axon.Component.component):
    def main(self):
        distance = {}
        while True:
            changed = False
            for positions_dictionary in self.Inbox("inbox"):
                for key in positions_dictionary:
                    ax,ay = positions_dictionary[key]
                    for other in positions_dictionary:
                        if key == other:
                            continue 
                        else:
                           changed = True
                           bx,by = positions_dictionary[other]
                           dx = ax-bx
                           dy = ay-by
                           d = int(math.sqrt((dx*dx)+(dy*dy)))
                           distance[ (key,other) ] = d
            if changed:
                self.send(repr(distance)+"\n", "outbox") # XXXX Note this is broken
            yield 1
                            

from Kamaelia.Util.Backplane import *
Backplane("PLAYERS").activate()

Pipeline(
    MyGamesEventsComponent(up="p", down="l", left="a", right="s"),
    BasicSprite("cat.png", name = "cat", border=40),
    PureTransformer(lambda x: ("Cat ", x)),
    PublishTo("PLAYERS"),
).activate()

Pipeline(
    MyGamesEventsComponent(up="up", down="down", left="left", right="right"),
    BasicSprite("mouse.png", name = "mouse", border=40),
    PureTransformer(lambda x: ("Mouse", x)),
    PublishTo("PLAYERS"),
).activate()

#Pipeline(
#    SubscribeTo("PLAYERS"),
#    PureTransformer(lambda x: repr(x)+"\n"),
#    ConsoleEchoer(),
#).activate()

Pipeline(
    SubscribeTo("PLAYERS"),
    PlayerAnalyser(),
    Distancer(),
    ConsoleEchoer(),
).activate()

SpriteScheduler(BasicSprite.allSprites()).run()
