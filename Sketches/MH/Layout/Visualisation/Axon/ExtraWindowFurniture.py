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

import Visualisation
from Visualisation.Graph import TopologyViewerServer, BaseParticle
from Physics import SimpleLaws, MultipleLaws

import pygame
from pygame.locals import *

class ExtraWindowFurniture(object):
    """Rendering for some extra 'furniture' for this 'axon/kamaelia' branded version
       of the TopologyViewer.
    """
    def __init__(self):
        super(ExtraWindowFurniture,self).__init__()
        
        self.logo = pygame.image.load("kamaelia_logo.png")
        
        biggest = max( self.logo.get_width(), self.logo.get_height() )
        from pygame.transform import rotozoom
        self.logo = rotozoom(self.logo, 0.0, 64.0 / biggest)
        
    def render(self, surface):
        """Rendering generator, draws kamaelia logo. Awwww!"""
        yield 10
        surface.blit(self.logo, (8,8))
        
    def setOffset( self, (x,y) ):
        pass
