---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.html){.reference}.[TopologyViewer3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html){.reference}.[TopologyViewer3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html){.reference}

------------------------------------------------------------------------

::: {.section}
class TopologyViewer3D([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TopologyViewer3D}
--------------------------------------------------------------------------------------------------------

TopologyViewer3D(\...) -\> new TopologyViewer3D component.

A component that takes incoming topology (change) data and displays it
live using pygame OpenGL. A simple physics model assists with visual
layout. Particle types, appearance and physics interactions can be
customised.

Keyword arguments (in order):

-   screensize \-- (width,height) of the display area (default =
    (800,600))
-   fullscreen \-- True to start up in fullscreen mode (default = False)
-   caption \-- Caption for the pygame window (default = \"3D Topology
    Viewer\")
-   particleTypes \-- dict(\"type\" -\> klass) mapping types of particle
    to classes used to render them (default = {\"-\":CuboidParticle3D})
-   initialTopology \-- (nodes,bonds) where bonds=list((src,dst))
    starting state for the topology (default=(\[\],\[\]))
-   laws \-- Physics laws to apply between particles (default =
    SimpleLaws(bondlength=2))
-   simCyclesPerRedraw \-- number of physics sim cycles to run between
    each redraw (default=1)
-   border \-- Minimum distance from edge of display area that new
    particles appear (default=0)

::: {.section}
### [Inboxes]{#symbol-TopologyViewer3D.Inboxes}

-   **control** : Shutdown signalling
-   **callback** : for the response after a displayrequest
-   **inbox** : Topology (change) data describing an
    [Axon](/Docs/Axon/Axon.html){.reference} system
-   **events** : Place where we recieve events from the outside world
:::

::: {.section}
### [Outboxes]{#symbol-TopologyViewer3D.Outboxes}

-   **outbox** : Notification and topology output
-   **signal** : Control signalling
-   **display\_signal** : Requests to Pygame Display service
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self\[, screensize\]\[, fullscreen\]\[, caption\]\[, particleTypes\]\[, initialTopology\]\[, laws\]\[, simCyclesPerRedraw\]\[, border\])]{#symbol-TopologyViewer3D.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [\_generatePos(self, posSpec)]{#symbol-TopologyViewer3D._generatePos}

generateXY(posSpec) -\> (x,y,z) or raises ValueError

posSpec == \"randompos\" or \"auto\" -\> random (x,y,z) within the
surface (specified border distance in from the edege) posSpec ==
\"(XXX,YYY,ZZZ)\" -\> specified x,y,z (positive or negative integers)
spaces are allowed within the tuple, but quotation is needed in this
case. E.g., \" ( 0 , 0 , -10 ) \"
:::

::: {.section}
#### [addListenEvents(self, events)]{#symbol-TopologyViewer3D.addListenEvents}

Sends listening request for pygame events to the display service. The
events parameter is expected to be a list of pygame event constants.
:::

::: {.section}
#### [addParticle(self, \*particles)]{#symbol-TopologyViewer3D.addParticle}

Add particles to the system
:::

::: {.section}
#### [breakBond(self, source, dest)]{#symbol-TopologyViewer3D.breakBond}

Break a bond from source to destination particle, specified by IDs
:::

::: {.section}
#### [deselectAll(self)]{#symbol-TopologyViewer3D.deselectAll}

Deselect all particles.
:::

::: {.section}
#### [doCommand(self, msg)]{#symbol-TopologyViewer3D.doCommand}

Proceses a topology command tuple: \[ \"ADD\", \"NODE\", \<id\>,
\<name\>, \<positionSpec\>, \<particle type\> \] \[ \"DEL\", \"NODE\",
\<id\> \] \[ \"ADD\", \"LINK\", \<id from\>, \<id to\> \] \[ \"DEL\",
\"LINK\", \<id from\>, \<id to\> \] \[ \"DEL\", \"ALL\" \] \[ \"GET\",
\"ALL\" \]
:::

::: {.section}
#### [draw(self)]{#symbol-TopologyViewer3D.draw}

Dummy method reserved for future use

Invoke draw() and save its commands to a newly generated displaylist.

The displaylist name is then sent to the display service via a
\"DISPLAYLIST\_UPDATE\" request.
:::

::: {.section}
#### [drawParticles(self, \*particles)]{#symbol-TopologyViewer3D.drawParticles}

Sends particles drawing opengl command to the display service.
:::

::: {.section}
#### [getParticleLabel(self, node\_id)]{#symbol-TopologyViewer3D.getParticleLabel}

getParticleLabel(node\_id) -\> particle\'s name

Returns the name/label of the specified particle.
:::

::: {.section}
#### [getTopology(self)]{#symbol-TopologyViewer3D.getTopology}

getTopology() -\> list of command tuples that would build the current
topology
:::

::: {.section}
#### [gotoDisplayLevel(self, dlevel)]{#symbol-TopologyViewer3D.gotoDisplayLevel}

Switch to another display level.
:::

::: {.section}
#### [handleEvents(self)]{#symbol-TopologyViewer3D.handleEvents}

Handle events.
:::

::: {.section}
#### [handleKeyEvents(self, event)]{#symbol-TopologyViewer3D.handleKeyEvents}

Handle keyboard events.
:::

::: {.section}
#### [handleMouseEvents(self, event)]{#symbol-TopologyViewer3D.handleMouseEvents}

Handle mouse events.
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-TopologyViewer3D.initialiseComponent}

Initialises.
:::

::: {.section}
#### [main(self)]{#symbol-TopologyViewer3D.main}

Main loop.
:::

::: {.section}
#### [makeBond(self, source, dest)]{#symbol-TopologyViewer3D.makeBond}

Make a bond from source to destination particle, specified by IDs
:::

::: {.section}
#### [quit(self\[, msg\])]{#symbol-TopologyViewer3D.quit}

Cause termination.
:::

::: {.section}
#### [removeListenEvents(self, events)]{#symbol-TopologyViewer3D.removeListenEvents}

Sends stop listening request for pygame events to the display service.
The events parameter is expected to be a list of pygame event constants.
:::

::: {.section}
#### [removeParticle(self, \*ids)]{#symbol-TopologyViewer3D.removeParticle}

Remove particle(s) specified by their ids.

Also breaks any bonds to/from that particle.
:::

::: {.section}
#### [rotateParticles(self, particles, dAngle)]{#symbol-TopologyViewer3D.rotateParticles}

Rotate the particles around their common centre dAngle degree. Particles
is a list; dAngle is a triple tuple of degree. If particles are given an
empty list, rotate all particles instead.
:::

::: {.section}
#### [scroll(self)]{#symbol-TopologyViewer3D.scroll}

Scroll the surface by resetting gluLookAt.
:::

::: {.section}
#### [selectParticle(self, particle)]{#symbol-TopologyViewer3D.selectParticle}

Select the specified particle.
:::

::: {.section}
#### [updateParticleLabel(self, node\_id, new\_name)]{#symbol-TopologyViewer3D.updateParticleLabel}

updateParticleLabel(node\_id, new\_name) -\> updates the given nodes
name & visual label if it exists

node\_id - an id for an already existing node new\_name - a string (may
include spaces) defining the new node name
:::
:::

::: {.section}
:::
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
