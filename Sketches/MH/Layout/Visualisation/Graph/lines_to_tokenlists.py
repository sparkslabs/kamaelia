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

import pygame
from pygame.locals import *

import random, time, re, sys

from Axon.Scheduler import scheduler as _scheduler
import Axon as _Axon

import Physics
from Physics import Particle as BaseParticle
from UI import PyGameApp, DragHandler

component = _Axon.Component.component

from Kamaelia.Util.PipelineComponent import pipeline

class lines_to_tokenlists(component):
    """Takes in lines and outputs a list of tokens on each line.
      
       Tokens are separated by white space.
      
       Tokens can be encapsulated with single or double quote marks, allowing you
       to include white space. If you do this, backslashs should be used to escape
       a quote mark that you want to include within the token. Represent backslash
       with a double backslash.
      
       Example:
           Hello world "how are you" 'john said "hi"' "i replied \"hi\"" end
      
         Becomes:
         [ 'Hello',
           'world',
           'how are you',
           'john said "hi"', 
           'i replied "hi"',
           'end' ]
    """
    def __init__(self):
        super(lines_to_tokenlists, self).__init__()
        
        doublequoted = r'(?:"((?:(?:\\.)|[^\\"])*)")'
        singlequoted = r"(?:'((?:(?:\\.)|[^\\'])*)')"
        unquoted     = r'([^"\'][^\s]*)'
        
        self.tokenpat = re.compile( r'\s*(?:' + unquoted +
                                          "|" + singlequoted +
                                          "|" + doublequoted +
                                          r')(?:\s+(.*))?$' )
        
   
    def main(self):
       
        while 1:
           while self.dataReady("inbox"):
               line = self.recv("inbox")
               tokens = self.lineToTokens(line)
               if tokens != []:
                   self.send(tokens, "outbox")
           yield 1
    
           
    def lineToTokens(self, line):
        tokens = []    #re.split("\s+",line.strip())
        while line != None and line.strip() != "":
            match = self.tokenpat.match(line)
            if match != None:
                (uq, sq, dq, line) = match.groups()
                if uq != None:
                    tokens += [uq]
                elif sq != None:
                    tokens += [ re.sub(r'\\(.)', r'\1', sq) ]
                elif dq != None:
                    tokens += [ re.sub(r'\\(.)', r'\1', dq) ]
            else:
                return []
        return tokens
