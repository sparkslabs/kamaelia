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
class history(object):
    def __init__(self, grid):
        super(history, self).__init__()
        
        self.grid = grid
        self.clear()
    
    def current(self):
        if not self.empty():
            return self.hist[self.mark]
        else: return None
    
    def empty(self):
        return not self.hist
    
    def add(self, rootshard):
        if not self.empty() and self.current() == None:
            self.hist.pop()
        self.hist += [rootshard]
        self.setEnd()
        return rootshard
    
    def setEnd(self):
        self.mark = len(self.hist) - 1
        return self.mark
    
    def latest(self):
        if not self.empty():
            return self.hist[len(self.hist)-1]
        else: return None
    
    def oldest(self):
        if not self.empty():
            return self.hist[0]
        else: return None
    
    def forward(self):
        if not self.empty():
            if self.current() != self.latest():
                self.mark += 1
            
            return self.current()
    
    def back(self):
        if not self.empty():
            if self.current() != self.oldest():
                self.mark -= 1
            
            return self.current()
    
    def clear(self):
        self.hist = []
        self.mark = -1



if __name__ == '__main__':
    from gui import *
    main()