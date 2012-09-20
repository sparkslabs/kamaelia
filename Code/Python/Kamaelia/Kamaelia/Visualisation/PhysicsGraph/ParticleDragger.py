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

"""\
================================
Drag handler for Topology Viewer
================================

A subclass of Kamaelia.UI.MH.DragHandler that implements "click and hold"
dragging of particles for the TopologyViewer.



Example Usage
-------------
See source for TopologyViewer.



How does it work?
-----------------
This is an implementation of Kamaelia.UI.MH.DragHandler. See that for more
details.

The detect() method uses the withinRadius method of the physics attribute of the
'app' to determine which (if any) particle the mouse is hovering over when the
drag is started. If there is no particle, then the drag does not begin.

At the start of the drag, the particle is 'frozen' to prevent motion due to the
physics model of the topology viewer. This is achieved by calling the freeze()
and unfreeze() methods of the particle. The particle is also 'selected'.

During the drag the particle's coordinates are updated and the physics model is
notified of the change.
"""


from Kamaelia.UI.MH import DragHandler

class ParticleDragger(DragHandler):
    """\
    ParticleDragger(event,app) -> new ParticleDragger object.
    
    Implements mouse dragging of particles in a topology viewer. Bind the
    handle(...) class method to the MOUSEBUTTONDOWN pygame event to use it (via
    a lambda function or equivalent)
                    
    Keyword Arguments:
    
    - event  -- pygame event object cuasing this
    - app    -- PyGameApp component this is happening in
    """

    def detect(self, pos, button):
        """detect( (x,y), button) -> (x,y) of particle or False if mouse (x,y) not over a particle"""
        
        # find particles under the mouse pos
        pos = int(pos[0] + self.app.left), int(pos[1] + self.app.top)
        inRange = self.app.physics.withinRadius( pos, self.app.biggestRadius )
        P = 0
        RSQUARED = 1
        inRange = list(filter(lambda x : x[P].radius*x[P].radius >= x[RSQUARED], inRange))
        
        if len(inRange) > 0:
            # of those in range, find one whose centre is nearest to the mouse pos
            best = -1
            for (p,rsquared) in inRange:
                if best < 0 or rsquared < best:
                    best = rsquared
                    self.particle = p
                  
            self.particle.freeze() # tell the particle its not allowed to move (zero velocity)
             
            # select this particle
            self.app.selectParticle(self.particle)

            # return the drag start coordinates             
            return self.particle.getLoc()
        else:
            self.app.selectParticle(None)
            return False

    def drag(self,newx,newy):
        """\
        Handler for the duration of the dragging operation.
        
        Updates the particle position as it is dragged.
        """
        self.particle.pos = (newx,newy)
        self.app.physics.updateLoc(self.particle)

    def release(self,newx, newy):
        """\
        Handler for the end of the dragging operation
        
        Updates the particle position before releasing it.
        """
        self.drag(newx, newy)
        self.particle.unFreeze()                


