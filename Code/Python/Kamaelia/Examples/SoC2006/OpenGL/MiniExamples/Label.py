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
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.UI.OpenGL.Label import Label
Graphline(
    Label1 = Label(caption="That", size=(2,2,1), sidecolour=(0,200,0), position=(-3,0,-10)),
    Label2 = Label(caption="Boy", bgcolour=(200,100,0), position=(3,0,-10)),
    Label3 = Label(caption="Needs", margin=15, position=(-1,0,-10), rotation=(30,0,10)),
    Label4 = Label(caption="Therapy!", fontsize=20, size=(1.3,0.3,1), position=(1,0,-10)),
    ECHO = ConsoleEchoer(),
    linkages = {
        ("Label1", "outbox") : ("ECHO", "inbox"),
        ("Label2", "outbox") : ("ECHO", "inbox"),
        ("Label3", "outbox") : ("ECHO", "inbox"),
        ("Label4", "outbox") : ("ECHO", "inbox"),            
    }
).run()
# Licensed to the BBC under a Contributor Agreement: THF
