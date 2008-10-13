#!/usr/bin/python
#
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
                            

#Pipeline(
#    SubscribeTo("PLAYERS"),
#    PureTransformer(lambda x: repr(x)+"\n"),
#    ConsoleEchoer(),
#).activate()

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
    BasicSprite("/home/zathras/Incoming/Princess.png", name = "mouse", border=40),
    PureTransformer(lambda x: ("Mouse", x)),
    PublishTo("PLAYERS"),
).activate()


Pipeline(
    SubscribeTo("PLAYERS"),
    PlayerAnalyser(),
    Distancer(),
    ConsoleEchoer(),
).activate()

SpriteScheduler(BasicSprite.allSprites()).run()
