#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import sys; sys.path.append("../../THF/3D/")

from Object3D import Object3D
from Util3D import Vector
import Axon
class Bunch: pass
    
class CubeRotator(Axon.Component.component):
    def main(self):
        while 1:
            yield 1
            cmd = Bunch()
            cmd.type = "rel_rotation"
            cmd.value = Vector(0.1, 0.1, 0.1)
            self.send(cmd, "outbox")

class CubeMover(Axon.Component.component):
    def main(self):
        x,y,z = 3.0, 3.0, -20.0
        dx = -0.03
        dy = -0.03
        dz = -0.03
        while 1:
            yield 1
            cmd = Bunch()
            cmd.type = "postition" #
            cmd.value = Vector(x, y, z)
            self.send(cmd, "outbox")
            x +=dx
            y +=dy
            z +=dz
            if abs(x)>5: dx = -dx
            if abs(y)>5: dy = -dy
            if abs(z+20)>10: dz = -dz
            print x, y, abs(x), abs(y)


from Kamaelia.Util.ConsoleEcho import consoleEchoer
from Kamaelia.Util.Graphline import Graphline

Graphline(
    CUBEC = Object3D(pos=Vector(0, 0,-12), name="Center cube"),
    CUBET = Object3D(pos=Vector(0,4,-20), name="Top cube"),
    CUBER = Object3D(pos=Vector(4,0,-22), name="Right cube"),
    CUBEB = Object3D(pos=Vector(0,-4,-18), name="Bottom cube"),
    CUBEL = Object3D(pos=Vector(-4, 0,-15), name="Left cube"),
    ROTATOR = CubeRotator(),
    MOVER = CubeMover(),
    ECHO = consoleEchoer(),
    linkages = {
        ("CUBEC", "outbox") : ("ECHO", "inbox"),
        ("CUBET", "outbox") : ("ECHO", "inbox"),
        ("CUBER", "outbox") : ("ECHO", "inbox"),
        ("CUBEB", "outbox") : ("ECHO", "inbox"),
        ("CUBEL", "outbox") : ("ECHO", "inbox"),
        ("ROTATOR", "outbox") : ("CUBEC", "3dcontrol"),
        ("MOVER", "outbox") : ("CUBEC", "3dcontrol"),
    } ).run()
