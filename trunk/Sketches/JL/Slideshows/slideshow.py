#!/usr/bin/python
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
#

from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.UI.Pygame.KeyEvent import KeyEvent
from Chooser_jlei import Chooser
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Console import ConsoleEchoer
from Axon.Ipc import producerFinished, shutdownMicroprocess

import os

path = "Slides"
extn = ".gif"
allfiles = os.listdir(path)
files = list()
K_esc = 27
for fname in allfiles:
    if fname[-len(extn):]==extn:
        files.append(os.path.join(path,fname))

files.sort()

g = Graphline(
     CHOOSER = Chooser(items = files),
     IMAGE = Image(size=(800,600), position=(8,48)),
     NEXT = Button(caption="Next", msg="NEXT", position=(72,8)),
     PREVIOUS = Button(caption="Previous", msg="PREV",position=(8,8)),
     FIRST = Button(caption="First", msg="FIRST",position=(256,8)),
     LAST = Button(caption="Last", msg="LAST",position=(320,8)),
     RANDOM = Button(caption="Random", msg="RANDOM", position=(500,8)), 
     #KeyEvent stuff
     keys = KeyEvent( key_events = {K_esc: (shutdownMicroprocess(), "outbox")}),
     output = ConsoleEchoer(),
     
     linkages = {
        ("NEXT","outbox") : ("CHOOSER","inbox"),
        ("PREVIOUS","outbox") : ("CHOOSER","inbox"),
        ("FIRST","outbox") : ("CHOOSER","inbox"),
        ("LAST","outbox") : ("CHOOSER","inbox"),
	("RANDOM", "outbox") : ("CHOOSER", "inbox"),
        ("CHOOSER","outbox") : ("IMAGE","inbox"),
#	("keys", "outbox") : ("output", "inbox")
        ("keys", "outbox") : ("IMAGE", "control")
     }
)

g.run()

# 6 May 2007 -- escape message isn't being sent to Chooser inbox
# 14 May 2007 -- closes pygame window, but not cleanly.

