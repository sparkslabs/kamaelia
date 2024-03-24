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

# Checked 2024/03/24

import UI

class ParticleDragger(UI.MH.DragHandler):
     def detect(self, pos, button):
         inRange = self.app.physics.withinRadius( pos, app.particleRadius )
         if len(inRange) > 0:
             self.particle = inRange[0][0]
             self.particle.freeze()
             return self.particle.getLoc()
         else:
             return False

     def drag(self,newx,newy):
         self.particle.pos = (newx,newy)
         self.app.physics.updateLoc(self.particle)

     def release(self,newx, newy):
         self.drag(newx, newy)
         self.particle.unFreeze()                

