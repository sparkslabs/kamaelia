---
pagename: Components/pydoc.old/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent.TopologyViewerComponent
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent.TopologyViewerComponent
===================================================================================

class TopologyViewerComponent(Kamaelia.UI.MH.PyGameApp.PyGameApp,Axon.Component.component)
------------------------------------------------------------------------------------------

TopologyViewerComponent(\...) -\> new TopologyViewerComponent component.

A component that takes incoming topology (change) data and displays it
live using pygame. A simple physics model assists with visual layout.
Particle types, appearance and physics interactions can be customised.

Keyword arguments (in order): - screensize \-- (width,height) of the
display area (default = (800,600)) - fullscreen \-- True to start up in
fullscreen mode (default = False) - caption \-- Caption for the pygame
window (default = \"Topology Viewer\") - particleTypes \-- dict(\"type\"
-\> klass) mapping types of particle to classes used to render them
(default = {\"-\":RenderingParticle}) - initialTopology \--
(nodes,bonds) where bonds=list((src,dst)) starting state for the
topology (default=(\[\],\[\])) - laws \-- Physics laws to apply between
particles (default = SimpleLaws(bondlength=100)) - simCyclesPerRedraw
\-- number of physics sim cycles to run between each redraw (default=1)
- border \-- Minimum distance from edge of display area that new
particles appear (default=100) - extraDrawing \-- Optional extra object
to be rendered (default=None) - showGrid \-- False, or True to show
gridlines (default=True) - transparency \-- None, or (r,g,b) colour to
make transparent - position \-- None, or (left,top) position for surface
within pygame window

#### Inboxes

-   control : Shutdown signalling
-   events : Place where we recieve events from the outside world
-   displaycontrol : Replies from PygameDisplay service
-   inbox : Topology (change) data describing an Axon system
-   alphacontrol : Alpha (transparency) of the image (value 0..255)

#### Outboxes

-   outbox : Notification and topology output
-   signal : NOT USED
-   displaysignal : Requests to PygameDisplay service

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, screensize, fullscreen, caption, particleTypes, initialTopology, laws, simCyclesPerRedraw, border, extraDrawing, showGrid, transparency, position)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### \_generateXY(self, posSpec)

generateXY(posSpec) -\> (x,y) or raises ValueError

posSpec == \"randompos\" or \"auto\" -\> random (x,y) within the surface
(specified border distance in from the edege) posSpec == \"(XXX,YYY)\"
-\> specified x,y (positive or negative integers)

### addParticle(self)

Add particles to the system

### breakBond(self, source, dest)

Break a bond from source to destination particle, specified by IDs

### doCommand(self, msg)

Proceses a topology command tuple:
:   \[ \"ADD\", \"NODE\", \<id\>, \<name\>, \<positionSpec\>, \<particle
    type\> \] \[ \"DEL\", \"NODE\", \<id\> \] \[ \"ADD\", \"LINK\", \<id
    from\>, \<id to\> \] \[ \"DEL\", \"LINK\", \<id from\>, \<id to\> \]
    \[ \"DEL\", \"ALL\" \] \[ \"GET\", \"ALL\" \]

### getParticleLabel(self, node\_id)

getParticleLabel(node\_id) -\> particle\'s name

Returns the name/label of the specified particle.

### getTopology(self)

getTopology() -\> list of command tuples that would build the current
topology

### initialiseComponent(self)

Initialises.

### keyDownHandler(self, event)

Handle keypresses:
:   ESCAPE, Q : quits F : toggles fullscreen mode arrows : scroll the
    view

### keyUpHandler(self, event)

Handle releases of keys

### mainLoop(self)

Main loop.

Proceses commands from \"inbox\" inbox, runs physics simulation, then
renders display

### makeBond(self, source, dest)

Make a bond from source to destination particle, specified by IDs

### quit(self, event)

Cause termination.

### removeParticle(self)

Remove particle(s) specified by their ids.

Also breaks any bonds to/from that particle.

### render(self)

Render elements to self.screen

### scroll(self, (dx, dy))

Scroll the contents being displayed on the surface by (dx,dy) left and
up.

### selectParticle(self, particle)

Select the specified particle.

### updateParticleLabel(self, node\_id, new\_name)

updateParticleLabel(node\_id, new\_name) -\> updates the given nodes
name & visual label if it exists

node\_id - an id for an already existing node new\_name - a string (may
include spaces) defining the new node name

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
