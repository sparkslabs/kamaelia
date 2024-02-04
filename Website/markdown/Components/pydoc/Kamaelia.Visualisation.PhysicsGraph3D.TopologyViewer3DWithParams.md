---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.html){.reference}.[TopologyViewer3DWithParams](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TopologyViewer3DWithParams](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams.TopologyViewer3DWithParams.html){.reference}**
:::

-   [Generic 3D Topology Viewer With more Parameters
    supports](#410){.reference}
    -   [Example Usage](#411){.reference}
    -   [How does it work?](#412){.reference}
:::

::: {.section}
Generic 3D Topology Viewer With more Parameters supports {#410}
========================================================

Extend TopologyViewer3D by supporting additional parameters of \"ADD\"
and \"UPDATE\" commands.

::: {.section}
[Example Usage]{#example-usage} {#411}
-------------------------------

A simple console driven topology viewer:

``` {.literal-block}
Pipeline( ConsoleReader(),
          lines_to_tokenlists(),
          TopologyViewer3DWithParams(),
        ).run()
```

Then at runtime try typing these commands to change the topology in real
time:

``` {.literal-block}
>>> DEL ALL
>>> ADD NODE 1 "1st node" (0,0,-10) teapot
>>> ADD NODE 2 "2nd node" randompos sphere image=../../../Docs/cat.gif
>>> ADD NODE 3 "3rd node" randompos - bgcolour=(255,255,0);bgcolour=(0,255,255)
>>> UPDATE NODE 1 name=1st;bgcolour=(0,255,0)
>>> UPDATE NODE 3 name=3rd;bgcolour=(255,0,0);fgcolour=(0,0,255);fontsize=100
>>> ADD NODE 1:1 "1st child node of the 1st node" " ( 0 , 0 , -10 ) " -
>>> ADD NODE 1:2 "2nd child node of the 1st node" randompos - "fontsize = 20"
>>> ADD LINK 1 2
>>> ADD LINK 3 2
>>> DEL LINK 1 2
>>> ADD LINK 1:1 1:2
>>> DEL NODE 1
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#412}
--------------------------------------

Extend TopologyViewer3D by supporting additional parameters of \"ADD\"
and \"UPDATE\" commands.

The format of \"ADD\" commands: \[ \"ADD\", \"NODE\", \<id\>, \<name\>,
\<positionSpec\>, \<particle type\>, \<parameters\> \]

The format of \"UPDATE\" commands: \[ \"UPDATE\", \"NODE\", \<id\>,
\<parameters\> \]

The format of parameters: pa=pa\_value;pb=pb\_value

Add quotation if there are spaces within parameters.

Available parameters:

> -   bgcolour \-- Colour of surfaces behind text label
>     (default=(230,230,230)), only apply to label texture
> -   fgcolour \-- Colour of the text label (default=(0,0,0), only apply
>     to label texture
> -   sidecolour \-- Colour of side planes (default=(200,200,244)), only
>     apply to CuboidParticle3D
> -   bgcolourselected \-- Background colour when the particle is
>     selected (default=(0,0,0)
> -   bgcolourselected \-- Frontground colour when the particle is
>     selected (default=(244,244,244))
> -   sidecolourselected \-- Side colour when the particle is selected
>     (default=(0,0,100))
> -   margin \-- Margin size in pixels (default=8)
> -   fontsize \-- Font size for label text (default=50)
> -   pixelscaling \-- Factor to convert pixels to units in 3d, ignored
>     if size is specified (default=100)
> -   thickness \-- Thickness of button widget, ignored if size is
>     specified (default=0.3)
> -   image \-- The uri of image, image texture instead of label texture
>     is used if specified

See Kamaelia.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D for more
information.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.html){.reference}.[TopologyViewer3DWithParams](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams.html){.reference}.[TopologyViewer3DWithParams](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams.TopologyViewer3DWithParams.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class TopologyViewer3DWithParams([Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D.html){.reference}) {#symbol-TopologyViewer3DWithParams}
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

TopologyViewer3DWithParams(\...) -\> new TopologyViewer3DWithParams
component.

A component that takes incoming topology (change) data and displays it
live using pygame OpenGL. A simple physics model assists with visual
layout. Particle types, appearance and physics interactions can be
customised.

It extends TopologyViewer3D by supporting additional parameters of
\"ADD\" commands.

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

::: {.section}
### [Inboxes]{#symbol-TopologyViewer3DWithParams.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-TopologyViewer3DWithParams.Outboxes}
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
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-TopologyViewer3DWithParams.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [doCommand(self, msg)]{#symbol-TopologyViewer3DWithParams.doCommand}

Proceses a topology command tuple: \[ \"ADD\", \"NODE\", \<id\>,
\<name\>, \<positionSpec\>, \<particle type\> \] \[ \"DEL\", \"NODE\",
\<id\> \] \[ \"ADD\", \"LINK\", \<id from\>, \<id to\> \] \[ \"DEL\",
\"LINK\", \<id from\>, \<id to\> \] \[ \"DEL\", \"ALL\" \] \[ \"GET\",
\"ALL\" \]
:::

::: {.section}
#### [updateParticle(self, node\_id, \*\*params)]{#symbol-TopologyViewer3DWithParams.updateParticle}

updateParticle(node\_id, \*\*params) -\> updates the given node\'s
parameters/attributes if it exists

-   node\_id \-- an id for an already existing node
-   params \-- the updated parameters/attributes dictionary of the
    particle, e.g. name, texture, colour and size
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D.html){.reference} :

-   [makeBond](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.makeBond){.reference}(self,
    source, dest)
-   [removeParticle](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.removeParticle){.reference}(self,
    \*ids)
-   [handleKeyEvents](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.handleKeyEvents){.reference}(self,
    event)
-   [quit](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.quit){.reference}(self\[,
    msg\])
-   [drawParticles](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.drawParticles){.reference}(self,
    \*particles)
-   [addParticle](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.addParticle){.reference}(self,
    \*particles)
-   [addListenEvents](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.addListenEvents){.reference}(self,
    events)
-   [updateParticleLabel](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.updateParticleLabel){.reference}(self,
    node\_id, new\_name)
-   [main](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.main){.reference}(self)
-   [rotateParticles](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.rotateParticles){.reference}(self,
    particles, dAngle)
-   [initialiseComponent](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.initialiseComponent){.reference}(self)
-   [draw](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.draw){.reference}(self)
-   [removeListenEvents](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.removeListenEvents){.reference}(self,
    events)
-   [breakBond](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.breakBond){.reference}(self,
    source, dest)
-   [getTopology](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.getTopology){.reference}(self)
-   [deselectAll](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.deselectAll){.reference}(self)
-   [selectParticle](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.selectParticle){.reference}(self,
    particle)
-   [\_generatePos](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D._generatePos){.reference}(self,
    posSpec)
-   [handleEvents](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.handleEvents){.reference}(self)
-   [gotoDisplayLevel](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.gotoDisplayLevel){.reference}(self,
    dlevel)
-   [handleMouseEvents](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.handleMouseEvents){.reference}(self,
    event)
-   [getParticleLabel](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.getParticleLabel){.reference}(self,
    node\_id)
-   [scroll](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html#symbol-TopologyViewer3D.scroll){.reference}(self)
:::
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
