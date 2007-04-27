#!/usr/bin/env python

# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
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
         


