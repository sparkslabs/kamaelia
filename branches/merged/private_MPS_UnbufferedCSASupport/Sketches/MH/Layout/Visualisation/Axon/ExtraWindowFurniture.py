#!/usr/bin/env python

# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
