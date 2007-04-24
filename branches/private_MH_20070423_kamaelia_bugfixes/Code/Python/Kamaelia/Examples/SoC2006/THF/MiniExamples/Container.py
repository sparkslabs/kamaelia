#!/usr/bin/env python
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

from Kamaelia.UI.OpenGL.SimpleButton import SimpleButton
from Kamaelia.UI.OpenGL.SimpleCube import SimpleCube
from Kamaelia.UI.OpenGL.ArrowButton import ArrowButton
from Kamaelia.UI.OpenGL.Movement import SimpleRotator, SimpleMover
from Kamaelia.UI.OpenGL.Container import Container

from Kamaelia.Chassis.Graphline import Graphline

o1 = SimpleButton(size=(1,1,1)).activate()
o2 = SimpleCube(size=(1,1,1)).activate()
o3 = ArrowButton(size=(1,1,1)).activate()

containercontents = {
    o1: {"position":(0,1,0)},
    o2: {"position":(1,-1,0)},
    o3: {"position":(-1,-1,0)},
}

Graphline(
    OBJ1=o1,
    OBJ2=o2,
    OBJ3=o3,
    CONTAINER=Container(contents=containercontents, position=(0,0,-10)),
    MOVER=SimpleMover(amount=(0.01,0.02,0.03)),
    ROTATOR=SimpleRotator(amount=(0,0.1,0)),
    linkages = {
        ("MOVER", "outbox") : ("CONTAINER","position"),
        ("ROTATOR", "outbox") : ("CONTAINER","rel_rotation")
    }
).run()
# Licensed to the BBC under a Contributor Agreement: THF
