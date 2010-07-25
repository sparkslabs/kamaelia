#!/usr/bin/env python
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
# -------------------------------------------------------------------------

# Simple topography viewer server - takes textual commands from a single socket
# and renders the appropriate graph

import pygame
from pygame.locals import *

import random, time, re, sys

from Axon.Scheduler import scheduler as _scheduler
import Axon as _Axon

import Physics
from Physics import Particle as BaseParticle
from UI import PyGameApp, DragHandler

component = _Axon.Component.component

from Kamaelia.Util.PipelineComponent import pipeline

class chunks_to_lines(component):
   """Takes in chunked textual data and breaks it at line breaks into lines."""

   def main(self):
      gotLine = False
      line = ""
      while 1: 
         pos = line.find("\n")
         if pos > -1:
            self.send(line[:pos], "outbox")
            line = line[pos+1:] 
         else:
            if self.dataReady("inbox"):
               chunk = self.recv("inbox")
               chunk = chunk.replace("\r", "")
               line = line + chunk
            else:
               self.pause()
         yield 1


