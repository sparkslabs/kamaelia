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

from Kamaelia.Util.Console import ConsoleReader
from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from Kamaelia.UI.OpenGL.PygameWrapper import PygameWrapper
from Kamaelia.UI.Pygame.MagnaDoodle import MagnaDoodle

# override pygame display service
ogl_display = OpenGLDisplay.getDisplayService()
PygameDisplay.setDisplayService(ogl_display[0])

TICKER = Ticker(size = (150, 150)).activate()
TICKER_WRAPPER = PygameWrapper(wrap=TICKER, position=(4, 1,-10), rotation=(-20,15,3)).activate()
MAGNADOODLE = MagnaDoodle(size=(200,200)).activate()
MAGNADOODLEWRAPPER = PygameWrapper(wrap=MAGNADOODLE, position=(-2, -2,-10), rotation=(20,10,0)).activate()
READER = ConsoleReader().activate()

READER.link( (READER,"outbox"), (TICKER, "inbox") )

Axon.Scheduler.scheduler.run.runThreads()  
# Licensed to the BBC under a Contributor Agreement: THF
