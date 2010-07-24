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
