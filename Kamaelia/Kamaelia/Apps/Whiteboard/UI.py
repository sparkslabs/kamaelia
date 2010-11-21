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
#
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.Chassis.Graphline import Graphline

def PagingControls(left,top):
    return Graphline(
                PREV  = Button(caption="<<",
                                size=(63,32), 
                                position=(left, top),
                                msg='prev'),
                NEXT  = Button(caption=">>",
                                size=(63,32), 
                                position=(left+64, top),
                                msg='next'),
                CHECKPOINT  = Button(caption="checkpoint",
                                size=(63,32),
                                position=(left+128, top),
                                msg="checkpoint"),
                NEWPAGE = Button(caption="new page",
                                 size=(63,32),
                                 position=(left+192, top),
                                 msg="new"),
                linkages = {
                    ("PREV","outbox") : ("", "outbox"),
                    ("NEXT","outbox") : ("", "outbox"),
                    ("CHECKPOINT","outbox") : ("", "outbox"),
                    ("NEWPAGE","outbox") : ("", "outbox"),
                }
           )

def LocalPagingControls(left,top):
    return Graphline(  
                REMOTEPREV = Button(caption="~~<<~~",
                                    size=(63,32), 
                                    position=(left, top),
                                    msg=[['prev']]),
                REMOTENEXT = Button(caption="~~>>~~",
                                    size=(63,32), 
                                    position=(left+64, top),
                                    msg=[['next']]),
                linkages = {
                    ("REMOTEPREV","outbox") : ("", "outbox"),
                    ("REMOTENEXT","outbox") : ("", "outbox"),
                }
           )

def Eraser(left,top):
    return Button(caption="Eraser", size=(64,32), position=(left,top))

def ClearPage(left,top):
    return Button(caption="clear", size=(63,32), position=(left, top), msg=[["clear"]])
