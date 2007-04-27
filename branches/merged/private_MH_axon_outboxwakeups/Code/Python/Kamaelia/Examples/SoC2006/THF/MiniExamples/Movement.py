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

import Axon
from Kamaelia.UI.OpenGL.SimpleCube import SimpleCube
from Kamaelia.UI.OpenGL.Movement import LinearPath, PathMover, SimpleMover, SimpleRotator, SimpleBuzzer

points = [(3,3,-20),
          (4,0,-20),
          (3,-3,-20),
          (0,-4,-20),
          (-3,-3,-20),
          (-4,0,-20),
          (-3,3,-20),
          (0,4,-20),
          (3,3,-20),
         ]
path = LinearPath(points, 1000)

cube1 = SimpleCube(size=(1,1,1)).activate()
pathmover = PathMover(path).activate()
pathmover.link((pathmover,"outbox"), (cube1,"position"))

cube2 = SimpleCube(size=(1,1,1)).activate()
simplemover = SimpleMover(borders=(3,5,7)).activate()
simplemover.link((simplemover,"outbox"), (cube2,"position"))

cube3 = SimpleCube(size=(1,1,1), position=(-1,0,-15)).activate()
rotator = SimpleRotator().activate()
rotator.link((rotator,"outbox"), (cube3,"rel_rotation"))

cube4 = SimpleCube(size=(1,1,1), position=(1,0,-15)).activate()
buzzer = SimpleBuzzer().activate()
buzzer.link((buzzer,"outbox"), (cube4,"scaling"))

Axon.Scheduler.scheduler.run.runThreads()  
# Licensed to the BBC under a Contributor Agreement: THF
