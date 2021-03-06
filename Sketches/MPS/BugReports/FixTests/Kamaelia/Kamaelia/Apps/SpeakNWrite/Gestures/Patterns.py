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

# STROKE PATTERNS & MULTI-STROKE GRAMMARS


# patterns are a dictionary.
# for each output symbol, there is a list of possible patterns.


# each pattern is a list of points that the stroke is expect to pass through
# and information about how the path, up to that point may curve.

# [(x,y,00), (x1,y1,c1), (x2,y2,c2), ...]
#  x,y = coordinates in 1.0x1.0 normalised square that the stroke is expected to pass through
#  c   = expected curvature:  0 = none/either
#                            +1 = bulges out to the RHS of this segment
#                            -1 = bulges out to the LHS of this segment
#  For the first point, there is no preceeding segment to look at the curvature of,
#  so specify a curvature of 00

BCK = chr(8)

patterns = {
    "a" : [ (( 5.0,  0.3), [(0.9, 1.0, 00), (0.4, 1.0, +1), (0.0, 0.4, +1), (0.4, 0.0, +1),
                            (0.9, 0.5, +1), (0.9, 0.9,  0), (0.9, 0.5,  0), (1.0, 0.0, +1)] ),
            (( 5.0,  0.3), [(0.4, 1.0, 00), (0.3, 1.0, +1), (0.0, 0.4, +1), (0.2, 0.0, +1),
                            (0.4, 0.5, +1), (0.5, 0.8,  0), (0.6, 0.5,  0), (1.0, 0.0, +1)] ),
          ],
    "b" : [ (( 9.0,  0.5), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.0, 0.2,  0),
                            (0.5, 0.6, -1), (1.0, 0.3, -1), (0.5, 0.0, -1), (0.0, 0.0, -1)] ),
            (( 9.0,  0.5), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.2,  0), (0.5, 0.0, +1),
                            (1.0, 0.2, +1), (0.5, 0.5, +1), (0.2, 0.3, +1)] ),
            (( 9.0,  0.5), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.0, 0.1,  0),
                            (0.5, 0.3, -1), (1.0, 0.2, -1), (0.5, 0.0, -1), (0.0, 0.0, -1)] ),
            (( 9.0,  0.5), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.2,  0), (0.5, 0.0, +1),
                            (1.0, 0.1, +1), (0.5, 0.3, +1), (0.2, 0.2, +1)] ),
          ],
    "c" : [ (( 5.0,  0.3), [(1.0, 0.9, 00), (0.5, 1.0, +1), (0.0, 0.5, +1), (0.5, 0.0, +1),
                            (1.0, 0.1, +1)] ),
            (( 5.0,  0.3), [(0.5, 1.0, 00), (0.0, 0.5, +1), (0.5, 0.0, +1), (1.0, 0.1, +1)] ),
          ],
    "d" : [ (( 9.0,  1.5), [(0.8, 0.5, 00), (0.4, 0.5, +1), (0.0, 0.2, +1), (0.5, 0.0, +1),
                            (0.9, 0.5, +1), (0.9, 1.0, +1), (0.9, 0.5, +1), (1.0, 0.0, +1)] ),
            (( 9.0,  1.5), [(0.8, 0.5, 00), (0.4, 0.5, +1), (0.0, 0.2, +1), (0.5, 0.0, +1),
                            (1.0, 0.5, +1), (1.0, 1.0, +1)] ),
          ],
    "e" : [ (( 3.0,  0.3), [(0.1, 0.5, 00), (1.0, 0.7, +1), (0.5, 1.0, +1), (0.0, 0.5, +1),
                            (0.5, 0.0, +1), (0.9, 0.1, +1)] ),
          ],
    # f - see grammar rules for optional dash
    "f" : [ (( 4.0,  1.5), [(1.0, 1.0, 00), (0.5, 0.8, +1), (0.5, 0.5, +1), (0.4, 0.0, -1),
                            (0.0, 0.3, -1), (0.5, 0.5, -1), (1.0, 0.5,  0)] ),
          ],
    "f0": [ (( 8.0,  2.0), [(1.0, 1.0, 00), (0.5, 1.0, +1), (0.0, 0.8, +1), (0.0, 0.5,  0),
                            (0.0, 0.0,  0)] ),
            (( 8.0,  2.0), [(1.0, 1.0, 00), (0.5, 0.8, +1), (0.5, 0.5, +1), (0.5, 0.2, -1),
                            (0.0, 0.0, -1)] ),
          ],
    "g" : [ (( 5.0,  0.3), [(1.0, 1.0, 00), (0.5, 1.0, +1), (0.0, 0.8, +1), (0.5, 0.6, +1),
                            (1.0, 0.9, +1), (1.0, 1.0,  0), (1.0, 0.5, -1), (0.5, 0.0, -1),
                            (0.0, 0.1, -1)] ),
            (( 5.0,  0.3), [(1.0, 1.0, 00), (0.5, 1.0, +1), (0.0, 0.8, +1), (0.5, 0.6, +1),
                            (1.0, 0.8, +1), (1.0, 0.5,  0), (0.5, 0.0, -1), (0.0, 0.1, -1)] ),
            (( 5.0,  0.3), [(1.0, 1.0, 00), (0.7, 1.0, +1), (0.4, 0.8, +1), (0.7, 0.6, +1),
                            (1.0, 0.9, +1), (1.0, 1.0,  0), (1.0, 0.5, -1), (0.5, 0.0, -1),
                            (0.0, 0.2, -1)] ),
          ],
    "h" : [ (( 8.0,  1.5), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.0, 0.3,  0),
                            (0.5, 0.4, -1), (1.0, 0.3, -1), (1.0, 0.0, -1)] )
          ],
    # i - see grammar rules
    # j - see grammar rules for optional '.'
    "j" : [ (( 8.0,  1.5), [(1.0, 1.0, 00), (1.0, 0.5,  0), (0.0, 0.0, -1)] )
          ],
    "k" : [ (( 8.0,  1.5), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.0, 0.2,  0),
                            (0.9, 0.6, -1), (0.1, 0.3, +1), (1.0, 0.0, +1)] ),
            (( 8.0,  1.5), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.0, 0.3,  0),
                            (0.5, 0.5, -1), (0.8, 0.4, -1), (0.5, 0.3, -1), (0.0, 0.3, -1),
                            (1.0, 0.0, -1)] ),
          ],
    "l" : [ ((999.,  0.5), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.5, 0.0,  0),
                            (1.0, 0.0,  0)] ),
            ((999.,  3.0), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0)] ),
          ],
    "m" : [ (( 3.0,  0.3), [(0.0, 0.0, 00), (0.0, 0.5,  0), (0.2, 1.0, -1), (0.5, 0.6, -1),
                            (0.5, 0.2,  0), (0.5, 0.6,  0), (0.7, 1.0, -1), (1.0, 0.5, -1),
                            (1.0, 0.0,  0)] ),
            (( 3.0,  0.3), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.0, 0.5,  0),
                            (0.2, 1.0, -1), (0.5, 0.6, -1), (0.5, 0.2,  0), (0.5, 0.6,  0),
                            (0.7, 1.0, -1), (1.0, 0.5, -1), (1.0, 0.2,  0)] ),
            (( 3.0,  0.3), [(0.0, 0.0, 00), (0.0, 0.5,  0), (0.2, 1.0, -1), (0.5, 0.6,  0),
                            (0.7, 1.0,  0), (1.0, 0.5, -1), (1.0, 0.0,  0)] ),
            (( 3.0,  0.3), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.0, 0.5,  0),
                            (0.2, 1.0, -1), (0.5, 0.6, -1), (0.7, 1.0,  0), (1.0, 0.5, -1),
                            (1.0, 0.0,  0)] ),
          ],
    "n" : [ (( 3.0,  0.3), [(0.0, 0.0, 00), (0.0, 0.5, -1), (0.5, 1.0, -1), (1.0, 0.5, -1),
                            (1.0, 0.0, -1)] ),
            (( 3.0,  0.3), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.0, 0.5, -1),
                            (0.5, 1.0, -1), (1.0, 0.5, -1), (1.0, 0.0, -1)] ),
          ],
    "o" : [ (( 3.0,  0.3), [(0.5, 1.0, 00), (1.0, 0.5, -1), (0.5, 0.0, -1), (0.0, 0.5, -1),
                            (0.5, 1.0, -1)] ),
            (( 3.0,  0.3), [(1.0, 0.5, 00), (0.5, 0.0, -1), (0.0, 0.5, -1), (0.5, 1.0, -1),
                            (1.0, 0.5, -1)] ),
            (( 3.0,  0.3), [(0.5, 0.0, 00), (0.0, 0.5, -1), (0.5, 1.0, -1), (1.0, 0.5, -1),
                            (0.5, 0.0, -1)] ),
            (( 3.0,  0.3), [(0.0, 0.5, 00), (0.5, 1.0, -1), (1.0, 0.5, -1), (0.5, 0.0, -1),
                            (0.0, 0.5, -1)] ),
            (( 3.0,  0.3), [(0.5, 1.0, 00), (0.0, 0.5, -1), (0.5, 0.0, -1),(1.0, 0.5, -1),
                            (0.5, 1.0, -1)] ),
            (( 3.0,  0.3), [(1.0, 0.5, 00), (0.5, 1.0, -1), (0.0, 0.5, -1), (0.5, 0.0, -1),
                            (1.0, 0.5, -1)] ),
            (( 3.0,  0.3), [(0.5, 0.0, 00), (1.0, 0.5, -1), (0.5, 1.0, -1), (0.0, 0.5, -1),
                            (0.5, 0.0, -1)] ),
            (( 3.0,  0.3), [(0.0, 0.5, 00), (0.5, 0.0, -1), (1.0, 0.5, -1), (0.5, 1.0, -1),
                            (0.0, 0.5, -1)] ),
          ],
    "p" : [ (( 9.0,  1.5), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.0, 0.5,  0),
                            (0.5, 1.0, -1), (1.0, 0.8, -1), (0.5, 0.6, -1), (0.2, 0.6, -1)] ),
            (( 9.0,  1.5), [(0.0, 0.0,  0), (0.0, 0.5,  0), (0.5, 1.0, -1), (1.0, 0.8, -1),
                            (0.5, 0.6, -1), (0.2, 0.6, -1)] ),
          ],
    "q" : [ (( 9.0,  1.5), [(1.0, 1.0, 00), (0.5, 0.9, +1), (0.0, 0.8, +1), (0.5, 0.6, +1),
                            (0.9, 0.9, +1), (1.0, 0.5,  0), (1.0, 0.0,  0)] ),
            (( 5.0,  0.6), [(0.6, 1.0, 00), (0.3, 0.9, +1), (0.0, 0.8, +1), (0.3, 0.6, +1),
                            (0.6, 0.9, +1), (0.5, 0.5,  0), (0.5, 0.0,  0), (1.0, 0.3,  0)] ),
          ],
    "r" : [ (( 5.0,  0.5), [(0.0, 0.9, 00), (0.0, 0.5,  0), (0.0, 0.0,  0), (0.0, 0.7,  0),
                            (0.5, 1.0, -1), (1.0, 0.9, -1)] ),
            (( 5.0,  1.0), [(0.0, 0.0,  0), (0.0, 0.5,  0), (1.0, 1.0, -1)] ),
          ],
    "s" : [ (( 5.0,  0.3), [(1.0, 0.9, 00), (0.5, 1.0,  0), (0.0, 0.7, +1), (0.5, 0.5, +1),
                            (1.0, 0.3, -1), (0.5, 0.0, -1), (0.0, 0.1,  0)] ),
          ],
    # t - see grammar rules for multi stroke version
    "t" : [ (( 5.0,  0.3), [(0.5, 1.0, 00), (0.5, 0.5,  0), (0.2, 0.0, -1), (0.0, 0.2, -1),
                            (0.5, 0.4,  0), (1.0, 0.5,  0)] ),
          ],
    "u" : [ (( 5.0,  0.6), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.5, 0.0, +1), (1.0, 0.5, +1),
                            (1.0, 1.0,  0)] ),
            (( 5.0,  0.6), [(0.0, 1.0, 00), (0.0, 0.5,  0), (0.4, 0.0, +1), (0.8, 0.5, +1),
                            (0.8, 1.0,  0), (0.8, 0.5,  0), (1.0, 0.0, +1)] ),
          ],
    "v" : [ (( 5.0,  0.6), [(0.0, 1.0, 00), (0.3, 0.5,  0), (0.5, 0.0,  0), (0.7, 0.5,  0),
                            (1.0, 1.0,  0)] ),
          ],
    "w" : [ (( 3.0,  0.3), [(0.0, 1.0, 00), (0.2, 0.0,  0), (0.5, 0.5,  0), (0.8, 0.0,  0),
                            (1.0, 1.0,  0)] ),
            (( 3.0,  0.3), [(0.0, 1.0, 00), (0.2, 0.0,  0), (0.5, 1.0,  0), (0.8, 0.0,  0),
                            (1.0, 1.0,  0)] ),
          ],
    # x - see grammar rules for additional versions
    "x" : [ (( 3.0,  0.6), [(0.0, 1.0, 00), (0.5, 0.5, -1), (0.0, 0.0, -1), (0.5, 0.5, +1),
                            (1.0, 1.0, -1), (0.5, 0.5, +1), (1.0, 0.0, +1)] ),
          ],
    "y" : [ (( 8.0,  1.5), [(0.0, 1.0, 00), (0.5, 0.5, +1), (1.0, 1.0, +1), (1.0, 0.5,  0),
                            (0.5, 0.0, -1)] ),
          ],
    "z" : [ (( 5.0,  0.5), [(0.0, 1.0, 00), (0.5, 1.0,  0), (1.0, 1.0,  0), (0.5, 0.5,  0),
                            (0.0, 0.0,  0), (0.5, 0.0,  0), (1.0, 0.0,  0)] ),
          ],
    
    " " : [ (( 0.3,  0.0), [(0.0, 0.0, 00), (0.5, 0.0,  0), (1.0, 0.0,  0)] ),
          ],
    BCK : [ (( 0.3,  0.0), [(1.0, 0.0, 00), (0.5, 0.0,  0), (0.0, 0.0,  0)] ),
          ],
    "\\": [ (( 1.5,  0.3), [(0.0, 1.0, 00), (0.5, 0.5,  0), (1.0, 0.0,  0)] ),
          ],
     "@": [ (( 2.0,  0.5), [(0.7, 0.7, 00), (0.3, 0.5, +1), (0.4, 0.4, +1), (0.7, 0.7,  0),
                            (0.8, 0.3, +1), (1.0, 0.7, +1), (0.5, 1.0, +1), (0.0, 0.5, +1),
                            (0.5, 0.0, +1)] ),
          ],
     "&": [ (( 5.0,  1.0), [(1.0, 0.0, 00), (0.5, 0.4,  0), (0.0, 0.8, -1), (0.5, 1.0, -1),
                            (1.0, 0.8, -1), (0.5, 0.5,  0), (0.0, 0.2,  0), (0.5, 0.0, +1),
                            (0.8, 0.2, +1)] ),
            (( 5.0,  1.0), [(1.0, 0.0, 00), (0.5, 0.4,  0), (0.0, 0.8, -1), (0.3, 1.0, -1),
                            (0.6, 0.8, -1), (0.3, 0.5,  0), (0.0, 0.2,  0), (0.3, 0.0, +1),
                            (0.5, 0.2, +1)] ),
          ],
     "'": [ (( 8.0,  0.5), [(0.0, 1.0, 00), (0.5, 1.0,  0), (1.0, 1.0,  0), (1.0, 0.5,  0),
                            (1.0, 0.0,  0)] ),
          ],
     ",": [ (( 5.0,  0.3), [(1.0, 1.0, 00), (1.0, 0.5,  0), (1.0, 0.0,  0), (0.5, 0.0,  0),
                            (0.0, 0.0,  0)] ),
          ],
          
    "\n": [ (( 5.0,  0.3), [(1.0, 1.0, 00), (0.5, 0.5,  0), (0.0, 0.0,  0)] ),
          ],
    
    "?0": [ (( 9.0,  1.5), [(0.2, 0.8, 00), (0.5, 1.0, -1), (1.0, 0.6, -1), (0.5, 0.2, -1),
                            (0.5, 0.0, +1) ] ),
          ],
    "?1": [ (( 9.0,  1.5), [(0.0, 1.0, 00), (0.5, 1.0, -1), (1.0, 0.7, -1), (0.0, 0.5, -1),
                            (0.0, 0.0, +1) ] ),
          ],
    }

# also need to add a simple follow-on grammar
# specify that, for this pattern, we override if:
#     the previous symbol was X
#     this pattern falls within minimum and maxmum bounding boxes, relative to the previous pattern
#        the new symbol will actually be. overrides like this will not become the 'previous' pattern
#        bounding boxes

# we use BCK+"X" to substitute a symbol
# we can specify patterns with 

