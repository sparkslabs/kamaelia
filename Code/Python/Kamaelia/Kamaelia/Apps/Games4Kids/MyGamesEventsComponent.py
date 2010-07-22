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


from Kamaelia.UI.Pygame.EventHandler import EventHandler
from Axon.Component import component
import pygame

from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
def MyGamesEventsComponent(up="p", down="l", left="a", right="s"):
    if len(left)>1: left = left.upper()
    else: left = left.lower()
    if len(right)>1: right = right.upper()
    else: right = right.lower()
    if len(up)>1: up = up.upper()
    else: up = up.lower()
    if len(down)>1: down = down.upper()
    else: down = down.lower()

    return KeyEvent(outboxes = { "outbox" : "Normal place for message",
                                 "signal" : "Normal place for message",
                               },
                    key_events = {
                        eval("pygame.K_"+up): ("start_up", "outbox"),
                        eval("pygame.K_"+down): ("start_down", "outbox"),
                        eval("pygame.K_"+left): ("start_left", "outbox"),
                        eval("pygame.K_"+right): ("start_right", "outbox"),
                    },
                    key_up_events = {
                        eval("pygame.K_"+up): ("stop_up", "outbox"),
                        eval("pygame.K_"+down): ("stop_down", "outbox"),
                        eval("pygame.K_"+left): ("stop_left", "outbox"),
                        eval("pygame.K_"+right): ("stop_right", "outbox"),
                    }
        )
