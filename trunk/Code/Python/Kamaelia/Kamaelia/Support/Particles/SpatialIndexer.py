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
"""\
=================================
Fast spatial indexing of entities
=================================

A SpatialIndexer object is an index of entities that provides fast lookups of
entities whose coordinates are within a specified radius of a specified point.
You can have as many, or few, spatial dimensions as you like.

This is particularly useful for computationally intensive tasks such as
calculating interactions between particles as performed, for example, by the
Particle and ParticleSystem classes.



Example Usage
-------------

Creating and index and registering two entities with it at (1,2) and (12,34).
We also tell the SpatialIndexer that the 'usual' radius we'll be searching over
is 5 units::

    >>> class Entity:
    ...   def __init__(self, coords):
    ...     self.coords = coords
    ...   def getLoc(self):
    ...     return self.coords
    ...
    >>> index = SpatialIndexer(proxDist=5.0)
    >>> a = Entity((1.0, 2.0))
    >>> b = Entity((12.0, 34.0))
    >>> index.add(a,b)
    
Only 'a' is within 10 units of (0,0)::
    
    >>> index.withinRadius((0,0), 10.0) == [(a,5.0)]
    True

The returned tuples are of the form: (entity, distance-squared)

Neither point is within 1 unit of (0,0)::

    >>> index.withinRadius((0,0), 1.0)
    []

Both 'a' and 'b' are within 50 units of (0,0)::
    
    >>> index.withinRadius((0,0), 50.0) == [(a,5.0), (b,1300)]
    True

We can ask the same, but request that 'a' be excluded::
    
    >>> filter = lambda particle : particle != a
    >>> index.withinRadius((0,0), 50.0, filter) == [(b,1300)]
    True

If we remove 'a' then only 'b' will be found::
    
    >>> index.remove(a)
    >>> index.withinRadius((0,0), 50.0) == [(b, 1300.0)]
    True

If we change the position of b we must *notify* the SpatialIndexer::
    
    >>> index.withinRadius((0,0), 10.0) == []
    True
    >>> b.coords=(5.0,6.0)
    >>> index.withinRadius((0,0), 10.0) == [(b, 61.0)]
    False
    >>> index.updateLoc(b)
    >>> index.withinRadius((0,0), 10.0) == [(b, 61.0)]
    True



How does it work?
-----------------

SpatialIndexer stores entities in an associative data structure, indexed by
their spatial location. Simply put, it breaks space into a grid of cells. The
coordinates of that cell index into a dictionary. All particles that fall within
a given cell are stored in a list in that dictionary entry.

It can then rapidly search for cells overlapping the area we want to search and
return those entities that fall within that area.

The size of the cells is specified during initialisation. Choose a size roughly
equal to the radius you'll most often be searching over. Too small a value will
case SpatialIndexer to spend too long enumerating through cells. To big a cell
size and far more entities will be searched that necessary.

Entities must provide a getLoc() method that returns a tuple of the coordinates
of that entity.

Use the add(...) and remove(...) methods to register and deregister entities
from the spatial index.

If you change the coordinates of an entity, the SpatialIndexer must be notified
by calling its updateLoc(...) method.
"""


# optimisation to speed up access to these functions:
from operator import mul as _mul
from operator import sub as _sub


class SpatialIndexer(object):
   """\
   SpatialIndexer(proxDist) -> new SpatialIndexer object

   Creates an indexing object, capable of quickly finding entities within a
   given radius of a given point.

   Optimise by setting proxDist to the radius you'll most commonly use when
   wanting to find entities.
   """
      
   def __init__(self, proxDist = 1.0):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      if proxDist <= 0.0:
         raise ValueError
      
      self.cellSize = proxDist
      
      self.cells = {}    # each dict entry is cellCoord -> list of entities
      self.entities = {} # each dict entry is entity -> cellCoord
      
      
   def _coord2cell(self, *coords):
      """Convert coordinate tuple into cell address tuple)"""
      return tuple([int(coord // self.cellSize) for coord in coords])
      
   def updateAll(self):
      """Notify the indexer that the positions of all entities may have changed."""
      self.updateLoc(*self.entities.keys())
      
      
   def updateLoc(self, *entities):
      """Add new entit(ies), or notify of a position change of entit(ies)."""
      for entity in entities:
         try:
            oldCell = self.entities[entity]
         except KeyError:
            oldCell = None
         
         newCell = self._coord2cell(*entity.getLoc())
         
         if newCell != oldCell:
            if oldCell != None:
               self.cells[oldCell].remove(entity)
 
            try:
                self.cells[newCell].append(entity)
            except KeyError:
                self.cells[newCell] = [entity]
               
            self.entities[entity] = newCell
            
   add = updateLoc
            
   def remove(self, *entities):
      """Notify that entit(ies) no longer exist (remove them)"""
      for entity in entities:
         if self.entities.has_key(entity):
            self.cells[ self.entities[entity] ].remove(entity)
            del self.entities[entity]
      
                        
   def withinRadius(self, centre, radius, filter=(lambda particle:True)):
      """\
      withinRadius(centre,radius[,filter]) -> list of (entity,distSquared)

      Returns a list of zero or more (entity,distSquared) tuples, respresenting
      those within the specified circle (centre and radius).

      The list can be pre-filtered by an optional filter function:
           filter(particle) -> True if the particle can be included in the list
      """
      # optimisation to speed up access to these functions:
      __sub, __mul = _sub, _mul
      
      lbound = [ int((coord-radius) // self.cellSize) for coord in centre ]
      ubound = [ int((coord+radius) // self.cellSize) for coord in centre ]
      
      rsquared = radius * radius
      
      inRange = []
      
      cell = lbound[:]# [ coord for coord in lbound ]
      inc = 0
      while inc == 0:
      
        # go through all entities in this cell
        try:
            for entity in self.cells[tuple(cell)]:
                if filter(entity):
                    # measure the distance from the coord
                    entcoord = entity.getLoc()
                    
                    sep = map(__sub, centre, entcoord)
                    distsquared = sum(map(__mul, sep,sep))
                    
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
    