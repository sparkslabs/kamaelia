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

# Simple topography viewer server - takes textual commands from a single socket
# and renders the appropriate graph

from UI import DragHandler

class ParticleDragger(DragHandler):
    """Works with the TopologyViewerComponent to provide particle selecting
    and dragging functionality"""

    def detect(self, pos, button):
        # find particles under the mouse pos
        pos = int(pos[0] + self.app.left), int(pos[1] + self.app.top)
        inRange = self.app.physics.withinRadius( pos, self.app.biggestRadius )
        inRange = filter(lambda (p, rsquared) : p.radius*p.radius >= rsquared, inRange)
        
        # deselect any particle already selected
        if self.app.selectedParticle != None:
            self.app.selectedParticle.deselect()
            
        if len(inRange) > 0:
            # of those in range, find one whose centre is nearest to the mouse pos
            best = -1
            for (p,rsquared) in inRange:
                if best < 0 or rsquared < best:
                    best = rsquared
                    self.particle = p
                  
            self.particle.freeze() # tell the particle its not allowed to move (zero velocity)
             
            # select this particle
            self.app.selectedParticle = self.particle
            self.particle.select()

            # return the drag start coordinates             
            return self.particle.getLoc()
        else:
            self.app.selectedParticle = None
            return False

    def drag(self,newx,newy):
        self.particle.pos = (newx,newy)
        self.app.physics.updateLoc(self.particle)

    def release(self,newx, newy):
        self.drag(newx, newy)
        self.particle.unFreeze()                


