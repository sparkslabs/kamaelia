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


# grammar rules for tranforming groups of recognised into new output symbols

# (replacement_symbol, rule)
# 'rule' is a list:
#   first symbol, (2nd symbol, bounds restrictions), (3rd symbol, bounds restrictions), ...)
# 'bounds restrictions' = (max bounds, min bounds)
# bounds' are (left,top,width,height) measured in bounding space
# minimum bound can be substituted with None to specify no minimum bound

# bounding space is a grid system based on the bounding box of the first symbol
# in the grammar sequence.
#
# The coordinates (3,3) -> (5,5) cover the volume of the stroke
#
#           +-----------------+
#           | 3,3 | 4,3 | 5,3 |
#           |-----------------|
#           | 3,4 | 4,4 | 5,4 |
#           |-----------------|
#           | 3,5 | 4,5 | 5,5 |
#           +-----------------+
#
# Coordinates outside of those bounds are a little more complicated. To cope with
# situations where charaters may be particularly narrow or wide, the grid spacing
# differs.
# 
# For narrow (thin) strokes:
#   grid square width AND height = 1/3rd the height of the stroke:
#
# For short (wide) strokes:
#   grid square width AND height = 1/3rd the width of the stroke.
#
# Eg, for a tall narrow stroke:
# 
#    0,1 :   :   : : : :   :   :
#        :   :   : : : :   :   :
#    ----+---+---+-+-+-+---+---+---
#        :   :   : : : :   :   :
#        :   :   : : : :   :   :
#    ----+---+---+=====+---+---+---
#    0,3 :   :   | | | |   :   :
#        :   :   | | | |   :   :
#    ----+---+---|-+-+-|---+---+---
#        :   :   | | | |   :   :
#        :   :   | | | |   :   :
#    ----+---+---|-+-+-|---+---+---
#        :   :   | | | |   :   :
#        :   :   | | | |   :   :
#    ----+---+---+=====+---+---+---
#        :   :   : : : :   :   :
#        :   :   : : : :   :   :
#    ----+---+---+-+-+-+---+---+---
#        :   :   : : : :   :   : 8,7
#        :   :   : : : :   :   :
#
# This makes specifying of bounds less sensitive to the exact width of a tall and
# narrow stroke, or the exact height of a short and wide stroke.

# this list is ordered: best matches first

BCK=chr(8)

grammar = [
       ("f",  [ "f0" ]),
        ("",  [ "f0",(" ", ((2,3, 7,4), None) )
              ] ),
    (BCK+"i", [ "l", (".", ((1,0, 7,3), None) )
              ] ),
              
        ("",  [ "j", (".", ((1,0, 7,3), None) )
              ] ),
              
    (BCK+"k", [ "l", ("c", ((2,3, 7,6), (6,5, 6,5)) )
              ] ),
        
    (BCK+"t", [ "l", (" ", ((1,3, 6,4), (3,3, 3,3)) )
              ] ),
    (BCK+"t", [ "l", (" ", ((1,3, 6,4), (3,4, 3,4)) )
              ] ),
    (BCK+"t", [ "c", (" ", ((1,3, 6,4), (3,3, 3,3)) )
              ] ),
    (BCK+"t", [ "c", (" ", ((1,3, 6,4), (3,4, 3,4)) )
              ] ),
              
    (BCK+"x", [ "\\",("\n",((2,2, 6,6), (3,3, 5,5)) )
              ] ),
        
        ("?", [ "?0",(".", ((1,6, 7,8), None) )
              ] ),
        ("?", [ "?1",(".", ((1,6, 7,8), None) )
              ] ),
    (BCK+"!", [ "l", (".", ((1,6, 7,8), None) )
              ] ),
              
    (BCK+'"', [ "'", ("'", ((2,2, 8,6), None) )
              ] ),
    ]

