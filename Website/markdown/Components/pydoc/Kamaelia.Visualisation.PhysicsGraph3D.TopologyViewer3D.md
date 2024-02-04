---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.html){.reference}.[TopologyViewer3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html){.reference}
===========================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TopologyViewer3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D.html){.reference}**
:::

-   [Generic 3D Topology Viewer](#413){.reference}
    -   [Example Usage](#414){.reference}
    -   [User Interface](#415){.reference}
    -   [How does it work?](#416){.reference}
    -   [Termination](#417){.reference}
        -   [Customising the 3D topology viewer](#418){.reference}
        -   [Writing your own particle class](#419){.reference}
:::

::: {.section}
Generic 3D Topology Viewer {#413}
==========================

A 3D version of TopologyViewer plus hierarchy topology support, pygame
based display of graph topologies. Rendering and physics laws can be
customised for specific applications.

::: {.section}
[Example Usage]{#example-usage} {#414}
-------------------------------

A simple console driven topology viewer:

``` {.literal-block}
Pipeline( ConsoleReader(),
          lines_to_tokenlists(),
          TopologyViewer3D(),
        ).run()
```

Then at runtime try typing these commands to change the topology in real
time:

``` {.literal-block}
>>> DEL ALL
>>> ADD NODE 1 "1st node" (0,0,-10) teapot
>>> ADD NODE 2 "2nd node" randompos sphere
>>> ADD NODE 3 "3rd node" randompos -
>>> ADD NODE 1:1 "1st child node of the 1st node" " ( 0 , 0 , -10 ) " -
>>> ADD NODE 1:2 "2nd child node of the 1st node" randompos -
>>> ADD LINK 1 2
>>> ADD LINK 3 2
>>> DEL LINK 1 2
>>> ADD LINK 1:1 1:2
>>> DEL NODE 1
```
:::

::: {.section}
[User Interface]{#user-interface} {#415}
---------------------------------

TopologyViewer3D manifests as a pygame OpenGL display surface. As it is
sent topology information, nodes and links between them will appear.

You can click a node with the mouse to select it. Depending on the
application, this may display additional data or, if integrated into
another app, have some other effect.

Click and drag with the left mouse button to move nodes around. Note
that a simple physics model or repulsion and attraction forces is always
active. This causes nodes to move around to help make it visually
clearer, however you may still need to drag nodes about to tidy it up.

For hierarchy topology, double-click a particle (or select one then
press return key) to show its child topology; right-click (or press
backspace key) to show last level\'s topology.

Operations supported:

> -   esc \-\-- quit
>
> -   a \-\-- viewer position moves left
>
> -   d \-\-- viewer position moves right
>
> -   w \-\-- viewer position moves up
>
> -   s \-\-- viewer position moves down
>
> -   pgup \-\-- viewer position moves forward (zoom in)
>
> -   pgdn \-\-- viewer position moves backward (zoom out)
>
> -   left \-\-- rotate selected particles to left around y axis (all
>     particles if none of them is selected)
>
> -   right \-\-- rotate selected particles to right around y axis (all
>     particles if none of them is selected)
>
> -   up \-\-- rotate selected particles to up around x axis (all
>     particles if none of them is selected)
>
> -   down \-\-- rotate selected particles to down around x axis (all
>     particles if none of them is selected)
>
> -   \< \-\-- rotate selected particles anticlock-wise around z axis
>     (all particles if none of them is selected)
>
> -   \> \-\-- rotate selected particles clock-wise around z axis (all
>     particles if none of them is selected)
>
> -   return \-\-- show next level\'s topology of the selected particle
>     when only one particle is selected
>
> -   backspace \-\-- show last level\'s topology
>
> -   Mouse click \-\-- click particle to select one, click empty area
>     to deselect all
>
> -   Mouse drag \-\-- move particles
>
> -   Mouse double-click \-\-- show next level\'s topology of the
>     particle clicked
>
> -   Mouse right-click \-\-- show last level\'s topology
>
> -   shift \-\-- multi Select Mode; shift+click for multiple selection/
>     deselection
>
> -   
>
>     ctrl \-\-- rotation Mode; when ctrl is pressed, mouse motion will rotate the selected particle
>
>     :   (all particles if none of them is selected)
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#416}
--------------------------------------

TopologyViewer3D is a Kamaeila component which renders Topology on a
pygame OpenGL display surface.

A 3D topology (graph) of nodes and links between them is rendered to the
surface.

You can specify an initial topology by providing a list of instantiated
particles and another list of pairs of those particles to show how they
are linked.

TopologyViewer3D responds to commands arriving at its \"inbox\" inbox
instructing it on how to change the topology. A command is a list/tuple.

Commands recognised are:

> \[ \"ADD\", \"NODE\", \<id\>, \<name\>, \<posSpec\>, \<particle type\> \]
>
> :   Add a node, using:
>
>     -   
>
>         id \-- a unique ID used to refer to the particle in other topology commands. Cannot be None.
>
>         :   For hierarchy topology, the id is joined by its parent id
>             with \":\" to represent the hierarchy structure. E.g.,
>             suppose the topology has 3 levels. The id of a particle in
>             the 1st level is 1Node; it has a child particle whose id
>             is 2Node; 2Node also has a child particle whose id is
>             3Node; then their ids are represented as 1Node 1Node:2Node
>             1Node:2Node:3Node
>
>     -   name \-- string name label for the particle
>
>     -   
>
>         posSpec \-- string describing initial (x,y,z) (see \_generateXY); spaces are allowed
>
>         :   within the tuple, but quotation is needed in this case.
>             E.g., \" ( 0 , 0 , -10 ) \"
>
>     -   
>
>         particleType \-- particle type (default provided is \"-\", unless custom types are provided - see below)
>
>         :   currently supported: \"-\" same as cuboid, cuboid, sphere
>             and teapot Note: it would be much slower than cuboid if
>             either sphere or teapot is used.
>
> \[ \"DEL\", \"NODE\", \<id\> \]
> :   Remove a node (also removes all links to and from it)
>
> \[ \"ADD\", \"LINK\", \<id from\>, \<id to\> \]
> :   Add a link, directional from fromID to toID
>
> \[ \"DEL\", \"LINK\", \<id from\>, \<id to\> \]
> :   Remove a link, directional from fromID to toID
>
> \[ \"DEL\", \"ALL\" \]
> :   Clears all nodes and links
>
> \[ \"GET\", \"ALL\" \]
> :   Outputs the current topology as a list of commands, just like
>     those used to build it. The list begins with a \'DEL ALL\'.
>
> \[ \"UPDATE\_NAME\", \"NODE\", \<id\>, \<new name\> \]
> :   If the node does not already exist, this does NOT cause it to be
>     created.
>
> \[ \"GET\_NAME\", \"NODE\", \<id\> \]
> :   Returns UPDATE\_NAME NODE message for the specified node

Commands are processed immediately, in the order in which they arrive.
You therefore cannot refer to a node or linkage that has not yet been
created, or that has already been destroyed.

If a stream of commands arrives in quick succession, rendering and
physics will be temporarily stopped, so commands can be processed more
quickly. This is necessary because when there is a large number of
particles, physics and rendering starts to take a long time, and will
therefore bottleneck the handling of commands.

However, there is a 1 second timeout, so at least one update of the
visual output is guaranteed per second.

TopologyViewer sends any output to its \"outbox\" outbox in the same
list/tuple format as used for commands sent to its \"inbox\" inbox. The
following may be output:

> \[ \"SELECT\", \"NODE\", \<id\> \]
> :   Notification that a given node has been selected.
>
> \[ \"SELECT\", \"NODE\", None \]
> :   Notificaion that *no node* is now selected.
>
> \[ \"TOPOLOGY\", \<topology command list\> \]
> :   List of commands needed to build the topology, as it currently
>     stands. The list will start with a (\"DEL\",\"ALL\") command. This
>     is sent in response to receiving a (\"GET\",\"ALL\") command.

Error and tip information is printed out directly when applied.

For hierarchy topology, the id of particles should be joined by its
parent id with \":\" to represent the hierarchy structure. See \"ADD
NODE\" command above for more information.
:::

::: {.section}
[Termination]{#termination} {#417}
---------------------------

If a shutdownMicroprocess message is received on this component\'s
\"control\" inbox, it will pass it on out of its \"signal\" outbox and
immediately terminate.

NOTE: Termination is currently rather cludgy - it raises an exception
which will cause the rest of a kamaelia system to halt. Do not rely on
this behaviour as it will be changed to provide cleaner termination at
some point.

::: {.section}
### [Customising the 3D topology viewer]{#customising-the-3d-topology-viewer} {#418}

You can customise:

-   the \'types\' of particles (nodes)
-   visual appearance of particles (nodes) and the links between them;
-   the physics laws used to assist with layout

Use the particleTypes argument of the initialiser to specify classes
that should be instantiated to render each type of particle (nodes).
particleTypes should be a dictionary mapping names for particle types to
the respective classes, for example:

``` {.literal-block}
{ "major" : BigParticle,  "minor"  : SmallParticle  }
```

See below for information on how to write your own particle classes.

Layout of the nodes on the surface is assisted by a physics model,
provided by an instance of the
[Kamaelia.Support.Particles.ParticleSystem](/Components/pydoc/Kamaelia.Support.Particles.ParticleSystem.html){.reference}
class. Freeze them if you want to make some particles not subject to the
law (particle.freeze()).

Customise the laws used for each particle type by providing a
Kamaelia.Phyics.Simple.MultipleLaws object at initialisation.
:::

::: {.section}
### [Writing your own particle class]{#writing-your-own-particle-class} {#419}

should inherit from Kamaelia.PhysicsGraph3D.Particles3D.Particle3D and
implement the following method (for rendering purposes):

> draw()
> :   draw OpenGL particles and links in this method.

TODO: Reduce CPU usage, improve responsive speed

References: 1.
[Kamaelia.Visualisation.PhysicsGraph.TopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.html){.reference}
2.
[Kamaelia.UI.OpenGL.OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html){.reference}
3.
[Kamaelia.UI.OpenGL.MatchedTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.MatchedTranslationInteractor.html){.reference}
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.html){.reference}.[TopologyViewer3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html){.reference}.[TopologyViewer3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================

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
