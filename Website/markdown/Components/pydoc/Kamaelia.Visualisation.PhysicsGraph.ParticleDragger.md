---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.ParticleDragger
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[ParticleDragger](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.ParticleDragger.html){.reference}
===================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Drag handler for Topology Viewer](#454){.reference}
    -   [Example Usage](#455){.reference}
    -   [How does it work?](#456){.reference}
:::

::: {.section}
Drag handler for Topology Viewer {#454}
================================

A subclass of
[Kamaelia.UI.MH.DragHandler](/Components/pydoc/Kamaelia.UI.MH.DragHandler.html){.reference}
that implements \"click and hold\" dragging of particles for the
TopologyViewer.

::: {.section}
[Example Usage]{#example-usage} {#455}
-------------------------------

See source for TopologyViewer.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#456}
--------------------------------------

This is an implementation of
[Kamaelia.UI.MH.DragHandler](/Components/pydoc/Kamaelia.UI.MH.DragHandler.html){.reference}.
See that for more details.

The detect() method uses the withinRadius method of the physics
attribute of the \'app\' to determine which (if any) particle the mouse
is hovering over when the drag is started. If there is no particle, then
the drag does not begin.

At the start of the drag, the particle is \'frozen\' to prevent motion
due to the physics model of the topology viewer. This is achieved by
calling the freeze() and unfreeze() methods of the particle. The
particle is also \'selected\'.

During the drag the particle\'s coordinates are updated and the physics
model is notified of the change.
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
