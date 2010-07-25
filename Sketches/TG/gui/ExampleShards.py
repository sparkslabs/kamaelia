#!/usr/bin/python
# -*- coding: utf-8 -*-
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

#from ShardCore import Shardable, Fail
import pygame
import Axon
from Kamaelia.UI.PygameDisplay import PygameDisplay


#
# Reusable Shards
#

def waitBox(self,boxname):
    """Generator. yields 1 until data ready on the named inbox."""
    waiting = True
    while waiting:
        if self.dataReady(boxname): return
        else: yield 1

def blitToSurface(self):
    self.send({"REDRAW":True, "surface":self.display}, "display_signal")

def addListenEvent(self, event):
    self.send({ "ADDLISTENEVENT" : pygame.__getattribute__(event),
                "surface" : self.display},
                "display_signal")
