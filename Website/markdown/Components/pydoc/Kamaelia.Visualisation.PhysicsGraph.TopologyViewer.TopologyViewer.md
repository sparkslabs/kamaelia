---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.TopologyViewer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[TopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.html){.reference}.[TopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.TopologyViewer.html){.reference}
========================================================================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.html){.reference}

------------------------------------------------------------------------

::: {.section}
class TopologyViewer([Kamaelia.UI.MH.PyGameApp](/Components/pydoc/Kamaelia.UI.MH.PyGameApp.html){.reference}, [Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TopologyViewer}
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

TopologyViewer(\...) -\> new TopologyViewer component.

A component that takes incoming topology (change) data and displays it
live using pygame. A simple physics model assists with visual layout.
Particle types, appearance and physics interactions can be customised.

Keyword arguments (in order):

-   screensize \-- (width,height) of the display area (default =
    (800,600))
-   fullscreen \-- True to start up in fullscreen mode (default = False)
-   caption \-- Caption for the pygame window (default = \"Topology
    Viewer\")
-   particleTypes \-- dict(\"type\" -\> klass) mapping types of particle
    to classes used to render them (default = {\"-\":RenderingParticle})
-   initialTopology \-- (nodes,bonds) where bonds=list((src,dst))
    starting state for the topology (default=(\[\],\[\]))
-   laws \-- Physics laws to apply between particles (default =
    SimpleLaws(bondlength=100))
-   simCyclesPerRedraw \-- number of physics sim cycles to run between
    each redraw (default=1)
-   border \-- Minimum distance from edge of display area that new
    particles appear (default=100)
-   extraDrawing \-- Optional extra object to be rendered (default=None)
-   showGrid \-- False, or True to show gridlines (default=True)
-   transparency \-- None, or (r,g,b) colour to make transparent
-   position \-- None, or (left,top) position for surface within pygame
    window

::: {.section}
### [Inboxes]{#symbol-TopologyViewer.Inboxes}

-   **control** : Shutdown signalling
-   **events** : Place where we recieve events from the outside world
-   **displaycontrol** : Replies from Pygame Display service
-   **inbox** : Topology (change) data describing an
    [Axon](/Docs/Axon/Axon.html){.reference} system
-   **alphacontrol** : Alpha (transparency) of the image (value 0..255)
:::

::: {.section}
### [Outboxes]{#symbol-TopologyViewer.Outboxes}

-   **outbox** : Notification and topology output
-   **signal** : NOT USED
-   **displaysignal** : Requests to Pygame Display service
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
#### [\_\_init\_\_(self\[, screensize\]\[, fullscreen\]\[, caption\]\[, particleTypes\]\[, initialTopology\]\[, laws\]\[, simCyclesPerRedraw\]\[, border\]\[, extraDrawing\]\[, showGrid\]\[, transparency\]\[, position\])]{#symbol-TopologyViewer.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [\_generateXY(self, posSpec)]{#symbol-TopologyViewer._generateXY}

generateXY(posSpec) -\> (x,y) or raises ValueError

posSpec == \"randompos\" or \"auto\" -\> random (x,y) within the surface
(specified border distance in from the edege) posSpec == \"(XXX,YYY)\"
-\> specified x,y (positive or negative integers)
:::

::: {.section}
#### [addParticle(self, \*particles)]{#symbol-TopologyViewer.addParticle}

Add particles to the system
:::

::: {.section}
#### [breakBond(self, source, dest)]{#symbol-TopologyViewer.breakBond}

Break a bond from source to destination particle, specified by IDs
:::

::: {.section}
#### [doCommand(self, msg)]{#symbol-TopologyViewer.doCommand}

Proceses a topology command tuple: \[ \"ADD\", \"NODE\", \<id\>,
\<name\>, \<positionSpec\>, \<particle type\> \] \[ \"DEL\", \"NODE\",
\<id\> \] \[ \"ADD\", \"LINK\", \<id from\>, \<id to\> \] \[ \"DEL\",
\"LINK\", \<id from\>, \<id to\> \] \[ \"DEL\", \"ALL\" \] \[ \"GET\",
\"ALL\" \]
:::

::: {.section}
#### [freezeAll(self)]{#symbol-TopologyViewer.freezeAll}
:::

::: {.section}
#### [getParticleLabel(self, node\_id)]{#symbol-TopologyViewer.getParticleLabel}

getParticleLabel(node\_id) -\> particle\'s name

Returns the name/label of the specified particle.
:::

::: {.section}
#### [getTopology(self)]{#symbol-TopologyViewer.getTopology}

getTopology() -\> list of command tuples that would build the current
topology
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-TopologyViewer.initialiseComponent}

Initialises.
:::

::: {.section}
#### [keyDownHandler(self, event)]{#symbol-TopologyViewer.keyDownHandler}

Handle keypresses: ESCAPE, Q : quits F : toggles fullscreen mode arrows
: scroll the view
:::

::: {.section}
#### [keyUpHandler(self, event)]{#symbol-TopologyViewer.keyUpHandler}

Handle releases of keys
:::

::: {.section}
#### [mainLoop(self)]{#symbol-TopologyViewer.mainLoop}

Main loop.

Proceses commands from \"inbox\" inbox, runs physics simulation, then
renders display

FIXME: This is massively broken, this component overrides
initialiseComponent, and also has a main *AND* has a mainLoop.
:::

::: {.section}
#### [makeBond(self, source, dest)]{#symbol-TopologyViewer.makeBond}

Make a bond from source to destination particle, specified by IDs
:::

::: {.section}
#### [quit(self\[, event\])]{#symbol-TopologyViewer.quit}

Cause termination.
:::

::: {.section}
#### [removeParticle(self, \*ids)]{#symbol-TopologyViewer.removeParticle}

Remove particle(s) specified by their ids.

Also breaks any bonds to/from that particle.
:::

::: {.section}
#### [render(self)]{#symbol-TopologyViewer.render}

Render elements to self.screen
:::

::: {.section}
#### [scroll(self, (\'dx\', \'dy\'))]{#symbol-TopologyViewer.scroll}

Scroll the contents being displayed on the surface by (dx,dy) left and
up.
:::

::: {.section}
#### [selectParticle(self, particle)]{#symbol-TopologyViewer.selectParticle}

Select the specified particle.
:::

::: {.section}
#### [unFreezeAll(self)]{#symbol-TopologyViewer.unFreezeAll}
:::

::: {.section}
#### [updateParticleLabel(self, node\_id, new\_name)]{#symbol-TopologyViewer.updateParticleLabel}

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
