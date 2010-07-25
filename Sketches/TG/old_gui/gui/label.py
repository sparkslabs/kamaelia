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
from box import box
from shardGen import shardGen
from floating import shardFloat

from pygame.color import THECOLORS as colours
from pygame import font

class label(box):
    def __init__(self, imname, text, x = 0, y = 0):
        super(label, self).__init__(imname, x, y)
        
        self.font = font.SysFont("Times New Roman", 25)
        self.colour = colours['blue']
        
        textim = self.font.render(text, True, self.colour)
        
        self.xborder = (self.width - textim.get_width())/2
        self.yborder = (self.height - textim.get_height())/2
        
        self.surface.blit(textim, (self.x + self.xborder, self.y + self.yborder))
        

class cancel(label):
    def __init__(self, imname, x = 0, y = 0):
        super(cancel, self).__init__(imname, 'cancel', x, y)
        
        self.redraw = None
    
    def handleMouseDown(self, e):
        if self.container().floating:
            self.redraw = self.container().floating.erase(self.container().screen)
            self.container().floating = None
    
    def draw(self, surface):
        r = super(cancel, self).draw(surface)
        if self.redraw:
            r += self.redraw
        
        return r

class clear(label):
    def __init__(self, imname, x = 0, y = 0):
        super(clear, self).__init__(imname, 'clear', x, y)
    
    def handleMouseDown(self, e):
        self.container().grid.clear()


class shardLabel(label):
    def __init__(self, shardclass, name, imname):
        super(shardLabel, self).__init__(imname, name)
        
        self.shard = shardclass
    
    def handleMouseDown(self, e):
        if self.container().floating:
            self.container().floating.erase(self.container().screen)
        
        self.container().floating = shardFloat(self.x, self.y, self)
    
    def makeGen(self):
        return shardGen(self.shard)


if __name__ == '__main__':
    from gui import *
    main()