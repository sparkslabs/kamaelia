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

from chunks_to_lines import chunks_to_lines
from lines_to_tokenlists import lines_to_tokenlists
from TopologyViewerComponent import TopologyViewerComponent

class TopologyViewerServer(pipeline):
    def __init__(self, noServer = False, serverPort = None, **dictArgs):
        """particleTypes = dictionary mapping names to particle classes
        
           All remaining named arguments are passed onto the TopologyViewerComponent
        """
        
        from Kamaelia.SingleServer import SingleServer
        from Kamaelia.Util.ConsoleEcho import consoleEchoer
        
        pipe = [chunks_to_lines(),
                lines_to_tokenlists(),
                TopologyViewerComponent(**dictArgs),
                consoleEchoer() ]
                
        if not noServer:
            if serverPort == None:
                serverPort = 1500
            pipe.insert(0, SingleServer(port=serverPort))
            

        super(TopologyViewerServer, self).__init__(*pipe)
         


