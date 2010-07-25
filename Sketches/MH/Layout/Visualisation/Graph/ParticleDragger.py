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


