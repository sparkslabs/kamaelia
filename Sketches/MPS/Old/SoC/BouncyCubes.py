#!/usr/bin/env python
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
