---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.Particles3D
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.html){.reference}.[Particles3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.Particles3D.html){.reference}
=================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Particle3D: Simple generic/ supertype particle for 3D Topology
    visualisation](#420){.reference}
    -   [Example Usage](#421){.reference}
    -   [How does it work?](#422){.reference}
-   [CuboidParticle3D: cuboid rendering particle for 3D Topology
    visualisation](#423){.reference}
    -   [Example Usage](#424){.reference}
    -   [How does it work?](#425){.reference}
-   [SphereParticle3D: sphere rendering particle for 3D Topology
    visualisation](#426){.reference}
    -   [Example Usage](#427){.reference}
    -   [How does it work?](#428){.reference}
-   [TeapotParticle3D: teapot rendering particle for 3D Topology
    visualisation](#429){.reference}
    -   [Example Usage](#430){.reference}
    -   [How does it work?](#431){.reference}
:::

::: {.section}
::: {.section}
[Particle3D: Simple generic/ supertype particle for 3D Topology visualisation]{#particle3d-simple-generic-supertype-particle-for-3d-topology-visualisation} {#420}
-----------------------------------------------------------------------------------------------------------------------------------------------------------

This is an implementation of a simple supertype particle for 3D topology
visualisation.

::: {.section}
### [Example Usage]{#example-usage} {#421}

Subclass it and extend it by adding draw() method to render any shape
you want the particle to be.
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#422}

This object subclasses
[Kamaelia.Support.Particles.Particle](/Components/pydoc/Kamaelia.Support.Particles.Particle.html){.reference}
and adds 3D elements.

At initialisation, provide a unique ID, a starting (x,y,z) position
tuple, and a name. The name is displayed as a label on top of the
particle. For other parameters, such as bgcolour and fgcolour, see its
doc string below.

If the particle becomes selected it changes its visual appearance to
reflect this.

There are two kinds of textures, i.e. text label and image textures.
When the \'image\' argument is provided, it uses image textures;
otherwise, it uses text label textures in which particle name is used as
the caption of the label. Note, the value of the \'image\' argument is
the uri of the image; it could be a path in local drive, a network
address or an internet address.

It only serves as a superclass of 3D particle and has no rendering
(draw) method, so it leaves the shape rendering to subclasses.
:::
:::

::: {.section}
[CuboidParticle3D: cuboid rendering particle for 3D Topology visualisation]{#cuboidparticle3d-cuboid-rendering-particle-for-3d-topology-visualisation} {#423}
------------------------------------------------------------------------------------------------------------------------------------------------------

This is an implementation of a simple cuboid particle for 3D topology
visualisation.

::: {.section}
### [Example Usage]{#id1} {#424}

A 3D topology viewer where particles of type \"-\" are rendered by
CuboidParticle3D instances:

``` {.literal-block}
TopologyViewer3D( particleTypes = {"-":CuboidParticle3D},
                laws = Kamaelia.Support.Particles.SimpleLaws(bondLength=2),
              ).run()
```

SimpleLaws are used that apply the same simple physics laws for all
particle types.
:::

::: {.section}
### [How does it work?]{#id2} {#425}

This object subclasses
Kamaelia.Visualisation.PhysicsGraph3D.Particles3D.Particle3D and adds
methods to support rendering (draw).
:::
:::

::: {.section}
[SphereParticle3D: sphere rendering particle for 3D Topology visualisation]{#sphereparticle3d-sphere-rendering-particle-for-3d-topology-visualisation} {#426}
------------------------------------------------------------------------------------------------------------------------------------------------------

This is an implementation of a simple sphere particle for 3D topology
visualisation.

Note: it would be much slower than CuboidParticle3D because it uses GLU
library.

::: {.section}
### [Example Usage]{#id3} {#427}

A 3D topology viewer where particles of type \"sphere\" are rendered by
SphereParticle3D instances:

``` {.literal-block}
TopologyViewer3D( particleTypes = {"sphere":SphereParticle3D},
                laws = Kamaelia.Support.Particles.SimpleLaws(bondLength=2),
              ).run()
```

SimpleLaws are used that apply the same simple physics laws for all
particle types.
:::

::: {.section}
### [How does it work?]{#id4} {#428}

This object subclasses
Kamaelia.Visualisation.PhysicsGraph3D.Particles3D.Particle3D and adds
methods to support rendering (draw).
:::
:::

::: {.section}
[TeapotParticle3D: teapot rendering particle for 3D Topology visualisation]{#teapotparticle3d-teapot-rendering-particle-for-3d-topology-visualisation} {#429}
------------------------------------------------------------------------------------------------------------------------------------------------------

This is an implementation of a simple teapot particle for 3D topology
visualisation.

Note: it would be much slower than CuboidParticle3D and SphereParticle3D
because it uses GLUT library.

::: {.section}
### [Example Usage]{#id5} {#430}

A 3D topology viewer where particles of type \"teapot\" are rendered by
CuboidParticle3D instances:

``` {.literal-block}
TopologyViewer3D( particleTypes = {"teapot":TeapotParticle3D},
                laws = Kamaelia.Support.Particles.SimpleLaws(bondLength=2),
              ).run()
```

SimpleLaws are used that apply the same simple physics laws for all
particle types.
:::

::: {.section}
### [How does it work?]{#id6} {#431}

This object subclasses
Kamaelia.Visualisation.PhysicsGraph3D.Particles3D.Particle3D and adds
methods to support rendering (draw).

References: 1.
[Kamaelia.UI.OpenGL.Button](/Components/pydoc/Kamaelia.UI.OpenGL.Button.html){.reference}
2.
[Kamaelia.UI.OpenGL.OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html){.reference}
:::
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
