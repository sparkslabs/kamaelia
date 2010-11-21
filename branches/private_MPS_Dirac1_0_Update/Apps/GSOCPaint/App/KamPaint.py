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

from pygame.locals import *
from Axon.experimental.Process import ProcessGraphline

from Kamaelia.Chassis.Seq import Seq

from Kamaelia.Util.ConsoleEcho import consoleEchoer
from Kamaelia.Apps.GSOCPaint.ToolBox import ToolBox
from Kamaelia.Apps.GSOCPaint.Core import DisplayConfig
from Kamaelia.Apps.GSOCPaint.Core import Paint

ProcessGraphline(
     COLOURS = Seq(
          DisplayConfig(width=270, height=600),
          ToolBox(size=(270, 600)),
          ),

     WINDOW1 = Seq(
               DisplayConfig(width=555, height=520),
               Paint(bgcolour=(100,100,172),position=(10,10), size = (500,500), transparent = False),
                ),
      linkages = {
          ("COLOURS", "outbox") : ("WINDOW1", "inbox"),
      }
).run()
# Licensed to the BBC under a Contributor Agreement: THF/DK
