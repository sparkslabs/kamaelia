---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[TopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.html){.reference}
=================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.TopologyViewer.html){.reference}**
:::

-   [Generic Topology Viewer](#447){.reference}
    -   [Example Usage](#448){.reference}
    -   [User Interface](#449){.reference}
    -   [How does it work?](#450){.reference}
    -   [Termination](#451){.reference}
        -   [Customising the topology viewer](#452){.reference}
        -   [Writing your own particle class](#453){.reference}
:::

::: {.section}
Generic Topology Viewer {#447}
=======================

Pygame based display of graph topologies. A simple physics model assists
with visual layout. Rendering and physics laws can be customised for
specific applications.

::: {.section}
[Example Usage]{#example-usage} {#448}
-------------------------------

A simple console driven topology viewer:

``` {.literal-block}
Pipeline( ConsoleReader(),
          lines_to_tokenlists(),
          TopologyViewer(),
        ).run()
```

Then at runtime try typing these commands to change the topology in real
time:

``` {.literal-block}
>>> DEL ALL
>>> ADD NODE 1 "1st node" randompos -
>>> ADD NODE 2 "2nd node" randompos -
>>> ADD NODE 3 "3rd node" randompos -
>>> ADD LINK 1 2
>>> ADD LINK 3 2
>>> DEL LINK 1 2
>>> DEL NODE 1
```
:::

::: {.section}
[User Interface]{#user-interface} {#449}
---------------------------------

TopologyViewer manifests as a pygame display surface. As it is sent
topology information nodes and links between them will appear.

You can click a node with the mouse to select it. Depending on the
application, this may display additional data or, if integrated into
another app, have some other effect.

Click and drag with the left mouse button to move nodes around. Note
that a simple physics model or repulsion and attraction forces is always
active. This causes nodes to move around to help make it visually
clearer, however you may still need to drag nodes about to tidy it up.

The surface on which the nodes appear is notionally infinite. Scroll
around using the arrow keys.

Press the \'f\' key to toggle between windowed and fullscreen modes.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#450}
--------------------------------------

TopologyViewer is a specialisation of the Kamaeila.UI.MH.PyGameApp
component. See documentation for that component to understand how it
obtains and handles events for a pygame display surface.

A topology (graph) of nodes and links between them is rendered to the
surface.

You can specify an initial topology by providing a list of instantiated
particles and another list of pairs of those particles to show how they
are linked.

TopologyViewer reponds to commands arriving at its \"inbox\" inbox
instructing it on how to change the topology. A command is a list/tuple.

Commands recognised are:

> \[ \"ADD\", \"NODE\", \<id\>, \<name\>, \<posSpec\>, \<particle type\> \]
>
> :   Add a node, using:
>
>     -   id \-- a unique ID used to refer to the particle in other
>         topology commands. Cannot be None.
>     -   name \-- string name label for the particle
>     -   posSpec \-- string describing initial x,y (see \_generateXY)
>     -   particleType \-- particle type (default provided is \"-\",
>         unless custom types are provided - see below)
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
>
> \[ \"FREEZE\", \"ALL\" \]
> :   Freezes all particles in the system, essentially halting the
>     simulation
>
> \[ \"UNFREEZE\", \"ALL\" \]
> :   Unfreezes all particles in the system, essentially restarting the
>     simulation

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
> \[ \"ERROR\", \<error string\> \]
> :   Notification of errors - eg. unrecognised commands arriving at the
>     \"inbox\" inbox
>
> \[ \"TOPOLOGY\", \<topology command list\> \]
> :   List of commands needed to build the topology, as it currently
>     stands. The list will start with a (\"DEL\",\"ALL\") command. This
>     is sent in response to receiving a (\"GET\",\"ALL\") command.
:::

::: {.section}
[Termination]{#termination} {#451}
---------------------------

If a shutdownMicroprocess message is received on this component\'s
\"control\" inbox this it will pass it on out of its \"signal\" outbox
and immediately terminate.

Historical note for short term: this has changed as of May 2008. In the
past, this component would also shutdown when it recieved a
producerFinished message. This has transpired to be a mistake for a
number of different systems, hence the change to only shutting down when
it recieves a shutdownMicroprocess message.

NOTE: Termination is currently rather cludgy - it raises an exception
which will cause the rest of a kamaelia system to halt. Do not rely on
this behaviour as it will be changed to provide cleaner termination at
some point.

::: {.section}
### [Customising the topology viewer]{#customising-the-topology-viewer} {#452}

You can customise:

-   the \'types\' of particles (nodes)
-   visual appearance of particles (nodes) and the links between them;
-   the physics laws used to assist with layout
-   extra visual furniture to be rendered

For example, see
[Kamaelia.Visualisation.Axon.AxonVisualiserServer](/Components/pydoc/Kamaelia.Visualisation.Axon.AxonVisualiserServer.html){.reference}.
This component uses two types of particle - to represent components and
inboxes/outboxes. Each has a different visual appearance, and the laws
acting between them differ depending on which particle types are
involved in the interaction.

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
class.

Customise the laws used for each particle type by providing a
Kamaelia.Phyics.Simple.MultipleLaws object at initialisation.
:::

::: {.section}
### [Writing your own particle class]{#writing-your-own-particle-class} {#453}

should inherit from
[Kamaelia.Support.Particles.Particle](/Components/pydoc/Kamaelia.Support.Particles.Particle.html){.reference}
and implement the following methods (for rendering purposes):

> setOffset( (left,top) )
> :   Notification that the surface has been scrolled by the user.
>     Particles should adjust the coordinates at which they render. For
>     example, a particle at (x, y) should be rendered at (x-left,
>     y-top). You can assume, until setOffset(\...) is called, that
>     (left,top) is (0,0).
>
> select()
> :   Called to inform the particle that it is selected (has been
>     clicked on)
>
> deselect()
> :   Called to inform the particle that is has been deselected.
>
> render(surface) -\> generator
> :   Called to get a generator for multi-pass rendering of the particle
>     (see below)

The coordinates of the particle are updated automatically both due to
mouse dragging and due to the physics model. See
[Kamaelia.Support.Particles.Particle](/Components/pydoc/Kamaelia.Support.Particles.Particle.html){.reference}
for more information.

The render(\...) method should return a generator that will render the
particle itself and its links/bonds to other particles.

Rendering by the TopologyViewer is multi-pass. This is done so that
irrespective of the order in which particles are chosen to be rendered,
things that need to be rendered before (underneath) other things can be
done consistently.

The generator should yield the number of the rendering pass it wishes to
be next called on. Each time it is subsequently called, it should
perform the rendering required for that pass. It then yields the number
of the next required pass or completes if there is no more rendering
required. Passes go in ascending numerical order.

For example,
[Kamaelia.Visualisation.PhysicsGraph.RenderingParticle](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.RenderingParticle.html){.reference}
renders in two passes:

``` {.literal-block}
def render(self, surface):
    yield 1
    # render lines for bonds *from* this particle *to* others
    yield 2
    # render a blob and the name label for the particle
```

\...in this case it ensures that the blobs for the particles always
appear on top of the lines representing the bonds between them.

Note that rendering passes must be coded in ascending order, but the
numbering can otherwise be arbitrary: The first pass can be any value
you like; subsequent passes can also be any value, provided it is
higher.

When writing rendering code for particle(s), make sure they all agree on
who should render what. It is inefficient if all bonds are being
rendered twice. For example, RenderingParticle only renders links *from*
that particle *to* another, but not in another direction.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[TopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.html){.reference}.[TopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.TopologyViewer.html){.reference}
========================================================================================================================================================================================================================================================================================================================================================================================================================================================

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
