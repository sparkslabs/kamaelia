#!/usr/bin/env python
#
# (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.Chassis.Graphline import Graphline

def PagingControls(left,top):
    return Graphline(
                PREV  = Button(caption="<<",
                                size=(63,32), 
                                position=(left, top),
                                msg='prev'),
                NEXT  = Button(caption=">>",
                                size=(63,32), 
                                position=(left+64, top),
                                msg='next'),
                CHECKPOINT  = Button(caption="checkpoint",
                                size=(63,32),
                                position=(left+128, top),
                                msg="checkpoint"),
                NEWPAGE = Button(caption="new page",
                                 size=(63,32),
                                 position=(left+192, top),
                                 msg="new"),
                linkages = {
                    ("PREV","outbox") : ("", "outbox"),
                    ("NEXT","outbox") : ("", "outbox"),
                    ("CHECKPOINT","outbox") : ("", "outbox"),
                    ("NEWPAGE","outbox") : ("", "outbox"),
                }
           )

def LocalPagingControls(left,top):
    return Graphline(  
                REMOTEPREV = Button(caption="~~<<~~",
                                    size=(63,32), 
                                    position=(left, top),
                                    msg=[['prev']]),
                REMOTENEXT = Button(caption="~~>>~~",
                                    size=(63,32), 
                                    position=(left+64, top),
                                    msg=[['next']]),
                linkages = {
                    ("REMOTEPREV","outbox") : ("", "outbox"),
                    ("REMOTENEXT","outbox") : ("", "outbox"),
                }
           )

def Eraser(left,top):
    return Button(caption="Eraser", size=(64,32), position=(left,top))

def ClearPage(left,top):
    return Button(caption="clear", size=(63,32), position=(left, top), msg=[["clear"]])
