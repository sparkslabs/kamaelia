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
from pygame.rect import Rect

class floating(object):
    def __init__(self, startx, starty, label):
        
        self.label = label
        
        self.x = startx
        self.y = starty
        self.width = label.width
        self.height = label.height
        
        self.surface = label.surface.copy()
        self.surface.set_alpha(100)
        
        self.oldsurf = label.surface.copy()
        
        self.oldx = startx
        self.oldy = starty
    
    def handleMouseMove(self, e):
        self.x, self.y = e.pos
    
    def bounds(self):
        return Rect(self.x, self.y, self.width, self.height)
    
    def container(self):
        return self.label.container()
    
    def erase(self, surface):
        r = [Rect(self.oldx, self.oldy, self.width, self.height)]
        surface.blit(self.oldsurf, (self.oldx, self.oldy))
        self.oldx = self.x
        self.oldy = self.y
        self.oldsurf = surface.subsurface(self.bounds()).copy()
        return r
    
    def draw(self, surface):
        if not surface.get_rect().contains(self.bounds()):
            return []
        
        if self.container().grid.contains(self.x, self.y):
            self.x, self.y = self.container().grid.snapToGrid(self.x, self.y)
        
        r = self.erase(surface)        
        surface.blit(self.surface, (self.x, self.y))
        return r + [self.bounds()]


class shardFloat(floating):
    def __init__(self, startx, starty, shardLabel):
        super(shardFloat, self).__init__(startx, starty, shardLabel)
        
        self.shardGen = shardLabel.makeGen()

if __name__ == '__main__':
    from gui import *
    main()