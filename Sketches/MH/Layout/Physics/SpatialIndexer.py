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

from operator import mul as _mul
from operator import sub as _sub

class SpatialIndexer(object):
   """Allows fast spatial lookups of entities -
      quickly find all entities within a given radius of a set of coordinates.
      
      Optimised by specifying the most commonly used proximity distance.
      This affects the speed of lookups and the size of the internal data structure.
      
      Entities must provide a getLoc() method that returns the coordinates as a tuple.
      
      To first register entities or if they change coordinates, something must call
      updateLoc(<entities>). If entities are removed, something must call remove(<entities>)
      """
      
   def __init__(self, proxDist = 1.0):
      if proxDist <= 0.0:
         raise ValueError
      
      self.cellSize = proxDist
      
      self.cells = {}    # each dict entry is cellCoord -> list of entities
      self.entities = {} # each dict entry is entity -> cellCoord
      
      
   def _coord2cell(self, *coords):
      return tuple([int(coord // self.cellSize) for coord in coords])
      
   def updateAll(self):
      """Update all entities"""
      self.updateLoc(*self.entities.keys())
      
      
   def updateLoc(self, *entities):
      """Add new entit(ies), or notify of a position change of entit(ies)."""
      for entity in entities:
         try:
            oldCell = self.entities[entity]
         except KeyError:
            oldCell = None
#         if self.entities.has_key(entity):
#            oldCell = self.entities[entity]
#         else:
#            oldCell = None
         
         newCell = self._coord2cell(*entity.getLoc())
         
         if newCell != oldCell:
            if oldCell != None:
               self.cells[oldCell].remove(entity)
 
            try:
                self.cells[newCell].append(entity)
            except KeyError:
                self.cells[newCell] = [entity]
#            if not self.cells.has_key(newCell):
#               self.cells[newCell] = [entity]
#            else:
#               self.cells[newCell].append(entity)
               
            self.entities[entity] = newCell
            
   add = updateLoc
            
   def remove(self, *entities):
      """Notify that entit(ies) no longer exist (remove them)"""
      for entity in entities:
         if self.entities.has_key(entity):
            self.cells[ self.entities[entity] ].remove(entity)
            del self.entities[entity]
      
                        
   def withinRadius(self, centre, radius, filter=(lambda particle:True)):
      """Returns a list of zero or more (particle, distSquared) tuples,
         representing those particles within radius distance of the
         specified centre coords.

         distance-squared from the centre coords is returned too to negate
         any need you may have to calculate it again yourself.

         You can specify a filter function that takes a candidate particle
         as an argument and should return True if it is to be included
         (if it is within the radius, of course). This is to allow efficient
         pre-filtering of the particles before the distance test is done.
      """
      __sub, __mul = _sub, _mul
      
      lbound = [ int((coord-radius) // self.cellSize) for coord in centre ]
      ubound = [ int((coord+radius) // self.cellSize) for coord in centre ]
      
      rsquared = radius * radius
      
      inRange = []
      
      cell = lbound[:]# [ coord for coord in lbound ]
      inc = 0
      while inc == 0:
      
        # go through all entities in this cell
#        if self.cells.has_key(tuple(cell)):
        try:
            for entity in self.cells[tuple(cell)]:
                if filter(entity):
                    # measure the distance from the coord
#                    distsquared = 0.0
                    entcoord = entity.getLoc()
                    
                    sep = map(__sub, centre, entcoord)
                    distsquared = sum(map(__mul, sep,sep))
                    
#                    for j in range(0, len(centre)):
#                        sep = (centre[j] - entcoord[j])
#                        distsquared += sep*sep
                        
                    # if within range, then add to the list of nodes to return
                    if distsquared <= rsquared:
                        inRange.append( (entity, distsquared) )
        except KeyError:
            pass
            
        # increment coordinates onto next cell.
        # As each coord reaches ubound, do 'carry'
        inc = 1
        for i in range(0,len(cell)):
           cell[i] += inc
           if cell[i] > ubound[i]:
              cell[i] = lbound[i]
              inc = 1
           else:
              inc = 0
               
      return inRange
      
      
if __name__ == "__main__":
    x = SpatialIndexer()
    print x.withinRadius( (0,0), 1.0)
    
    class Entity(object):
      def __init__(self, coords):
        self.coords = coords
      def getLoc(self):
        return self.coords
        
    a = Entity((0.1, 0.2))
    b = Entity((1.2, 3.4))
    x.add(a,b)
    print x.withinRadius( (0,0), 1.0)
    print 
    print x.withinRadius( (0,0), 0.1)
    print
    print x.withinRadius( (0,0), 5)
    print
    x.remove(a)
    print x.withinRadius( (0,0), 5)
    