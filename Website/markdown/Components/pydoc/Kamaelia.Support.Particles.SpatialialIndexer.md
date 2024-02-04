---
pagename: Components/pydoc/Kamaelia.Support.Particles.SpatialialIndexer
last-modified-date: 2009-12-10
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Particles](/Components/pydoc/Kamaelia.Support.Particles.html){.reference}.[SpatialIndexer](/Components/pydoc/Kamaelia.Support.Particles.SpatialIndexer.html){.reference}
================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Fast spatial indexing of entities](#13){.reference}
    -   [Example Usage](#14){.reference}
    -   [How does it work?](#15){.reference}
:::

::: {.section}
Fast spatial indexing of entities {#13}
=================================

A SpatialIndexer object is an index of entities that provides fast
lookups of entities whose coordinates are within a specified radius of a
specified point. You can have as many, or few, spatial dimensions as you
like.

This is particularly useful for computationally intensive tasks such as
calculating interactions between particles as performed, for example, by
the Particle and ParticleSystem classes.

::: {.section}
[Example Usage]{#example-usage} {#14}
-------------------------------

Creating and index and registering two entities with it at (1,2) and
(12,34). We also tell the SpatialIndexer that the \'usual\' radius
we\'ll be searching over is 5 units:

``` {.literal-block}
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
```

Only \'a\' is within 10 units of (0,0):

``` {.literal-block}
>>> index.withinRadius((0,0), 10.0) == [(a,5.0)]
True
```

The returned tuples are of the form: (entity, distance-squared)

Neither point is within 1 unit of (0,0):

``` {.literal-block}
>>> index.withinRadius((0,0), 1.0)
[]
```

Both \'a\' and \'b\' are within 50 units of (0,0):

``` {.literal-block}
>>> index.withinRadius((0,0), 50.0) == [(a,5.0), (b,1300)]
True
```

We can ask the same, but request that \'a\' be excluded:

``` {.literal-block}
>>> filter = lambda particle : particle != a
>>> index.withinRadius((0,0), 50.0, filter) == [(b,1300)]
True
```

If we remove \'a\' then only \'b\' will be found:

``` {.literal-block}
>>> index.remove(a)
>>> index.withinRadius((0,0), 50.0) == [(b, 1300.0)]
True
```

If we change the position of b we must *notify* the SpatialIndexer:

``` {.literal-block}
>>> index.withinRadius((0,0), 10.0) == []
True
>>> b.coords=(5.0,6.0)
>>> index.withinRadius((0,0), 10.0) == [(b, 61.0)]
False
>>> index.updateLoc(b)
>>> index.withinRadius((0,0), 10.0) == [(b, 61.0)]
True
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#15}
--------------------------------------

SpatialIndexer stores entities in an associative data structure, indexed
by their spatial location. Simply put, it breaks space into a grid of
cells. The coordinates of that cell index into a dictionary. All
particles that fall within a given cell are stored in a list in that
dictionary entry.

It can then rapidly search for cells overlapping the area we want to
search and return those entities that fall within that area.

The size of the cells is specified during initialisation. Choose a size
roughly equal to the radius you\'ll most often be searching over. Too
small a value will case SpatialIndexer to spend too long enumerating
through cells. To big a cell size and far more entities will be searched
that necessary.

Entities must provide a getLoc() method that returns a tuple of the
coordinates of that entity.

Use the add(\...) and remove(\...) methods to register and deregister
entities from the spatial index.

If you change the coordinates of an entity, the SpatialIndexer must be
notified by calling its updateLoc(\...) method.
:::
:::

------------------------------------------------------------------------

::: {.section}
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
