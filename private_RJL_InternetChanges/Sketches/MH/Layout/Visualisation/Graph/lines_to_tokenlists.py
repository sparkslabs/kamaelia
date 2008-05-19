#!/usr/bin/env python

# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
