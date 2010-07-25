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
from pygame import image
from pygame.rect import Rect
from floating import floating

class box(object):
    def __init__(self, imname, x = 0, y = 0):
        self.surface = image.load(imname).convert()
        self.x = x
        self.y = y
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.toolbar = None # set by toolbar when added
    
    def container(self):
        if self.toolbar:
            return self.toolbar.container
    
    def bounds(self):
        return Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):   
        surface.blit(self.surface, (self.x, self.y))
        return [self.bounds()]


if __name__ == '__main__':
    from gui import *
    main()