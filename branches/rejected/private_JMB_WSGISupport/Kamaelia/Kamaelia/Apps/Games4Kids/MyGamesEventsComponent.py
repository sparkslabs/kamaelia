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
