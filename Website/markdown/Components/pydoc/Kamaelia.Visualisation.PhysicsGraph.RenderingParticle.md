---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.RenderingParticle
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[RenderingParticle](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.RenderingParticle.html){.reference}
=======================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Simple generic particle for Topology
    visualisation](#435){.reference}
    -   [Example Usage](#436){.reference}
    -   [How does it work?](#437){.reference}
:::

::: {.section}
Simple generic particle for Topology visualisation {#435}
==================================================

This is an implementation of a simple rendering particle for topology
visualisation.

::: {.section}
[Example Usage]{#example-usage} {#436}
-------------------------------

A topology viewer where particles of type \"-\" are rendered by
RenderingParticle instances:

``` {.literal-block}
TopologyViewer( particleTypes = {"-":RenderingParticle},
                laws = Kamaelia.Support.Particles.SimpleLaws(),
              ).run()
```

SimpleLaws are used that apply the same simple physics laws for all
particle types.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#437}
--------------------------------------

This object subclasses
[Kamaelia.Support.Particles.Particle](/Components/pydoc/Kamaelia.Support.Particles.Particle.html){.reference}
and adds methods to support rendering.

At initialisation, provide a unique ID, a starting (x,y) position tuple,
and a name. The name is displayed as a label ontop of the particle.

If the particle becomes selected it changes its visual appearance to
reflect this.

It also renders bonds *from* this particle *to* another. They are
rendered as simple lines.

Rendering is performed by a generator, returned when the render() method
is called. Its behaviour is that needed for the framework for multi-pass
rendering that is used by TopologyViewer.

The generator yields the number of the rendering pass it wishes to be
next on next. Each time it is subsequently called, it performs the
rendering required for that pass. It then yields the number of the next
required pass or completes if there is no more rendering required.

An setOffset() method is also implemented to allow the particles
coordinates to be offset. This therefore makes it possible to scroll the
particles around the display surface.

See TopologyViewer for more details.
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
