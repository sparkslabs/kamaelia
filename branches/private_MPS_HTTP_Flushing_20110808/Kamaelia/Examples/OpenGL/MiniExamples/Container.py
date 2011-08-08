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
