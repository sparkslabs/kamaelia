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

import string

class CharacterFIFO(object):
    """An efficient character queue type (designed to work in O(n) time for n characters)."""
    def __init__(self):
        self.queuearray = []
        self.length = 0
        self.startboundary = 0
        self.linecount = 0

        self.newlinechecked = [0, 0]
        self.newlinelength = 0
        
    def push(self, text):
        """\
        Adds a string to the back of the queue.
        """
        
        if text:
            self.queuearray.append(text)
            self.length += len(text)
        
    def __len__(self):
        return self.length
    
    def popline(self):
        """\
        Returns a string containing all the characters until the first '\n' symbol and
        removes those characters (and the '\n') from the queue.
        """
        
        if self.length == 0:
            return None
        
        foundlineending = False        
        while self.newlinechecked[0] < len(self.queuearray):
            while self.newlinechecked[1] < len(self.queuearray[self.newlinechecked[0]]):
                if self.queuearray[self.newlinechecked[0]][self.newlinechecked[1]] == "\n":
                    foundlineending = True
                    break
                else:
                    self.newlinechecked[1] += 1
                    self.newlinelength += 1
            
            if foundlineending:
                break
            
            self.newlinechecked[0] += 1
            self.newlinechecked[1] = 0
        
        if foundlineending:
            result = self.poplength(self.newlinelength + 1)
            self.newlinelength = 0
            self.newlinechecked[0] = 0
            self.newlinechecked[1] = self.startboundary
            return result
        else:
            return None
            
    def poplength(self, length):
        """\
        Returns a string containing the first <length> characters in the queue
        and removes those characters from the queue.
        """
        
        if len(self) < length:
            raise IndexError
        else:
            thischunk = []
            sizeneeded = length
            while 1:
                chunk = self.queuearray[0]
                sizeneeded -= len(chunk) - self.startboundary
                
                if sizeneeded < 0: # new start boundary in the middle of this chunk
                    thischunk.append(chunk[self.startboundary:len(chunk) + sizeneeded])
                    self.startboundary = len(chunk) + sizeneeded
                else: # this chunk is completely within the requested string
                    if self.startboundary > 0:
                        thischunk.append(chunk[self.startboundary:])
                    else:
                        thischunk.append(chunk)
                    
                    self.queuearray.pop(0)
                    self.startboundary = 0
                    
                if sizeneeded <= 0:
                    break

            if length > self.newlinelength:
                self.newlinelength = 0
                self.newlinechecked = [0, self.startboundary]
            else:
                self.newlinelength -= length
                self.newlinechecked[0] -= len(thischunk)
            self.length -= length
            return string.join(thischunk, "")
