---
pagename: Components/pydoc/Kamaelia.Support.Particles.Particle
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Particles](/Components/pydoc/Kamaelia.Support.Particles.html){.reference}.[Particle](/Components/pydoc/Kamaelia.Support.Particles.Particle.html){.reference}
====================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Particle in a discrete time physics simulation](#10){.reference}
    -   [Example Usage](#11){.reference}
    -   [How does it work?](#12){.reference}
:::

::: {.section}
Particle in a discrete time physics simulation {#10}
==============================================

The Particle class provides the basis for particles in a ParticleSystem
simulation. The particles handle their own physics interaction
calculations. You can have as many, or few, spatial dimensions as you
like.

Extend this base class to add extra functionality, such as the ability
to render to a graphics display (see RenderingParticle for an example of
this)

::: {.section}
[Example Usage]{#example-usage} {#11}
-------------------------------

See ParticleSystem
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#12}
--------------------------------------

Particle maintains lists of other particles it is bonded to. The bonds
have direction, so the bonding information is stored in two lists -
bondedTo and bondedFrom.

Bonds are made and broken by calling the makeBond(\...), breakBond(\...)
and breakAllBonds(\...) methods.

Particle calculates its interactions with other particles when the
doInteractions(\...) method is called. This must be supplied with an
object containins the laws to apply, and another providing the ability
to search for particles within a given distance of a point. See
SimpleLaws/MultipleLaws and SpatialIndexer respectively. This updates
the velocity of the particle but not its actual position.

The particle\'s position is only updated when the update(\...) method is
called.

A simulation system should calculate each simulation cycle as a two step
process: First, for all particles, calling doInteractions(\...). Second,
for all particles, calling update(\...).

A particle can be frozen in place by calling freeze() and unFreeze().
This forces the particle\'s velocity to zero, meaning it doesn\'t move
because of interactions with other particles.

The simulation must have a \'tick\' counter, whose value changes
(increments) every simulation cycle. Particle stores the last tick value
it was presented with so that, when interacting with other particles, it
can see which others have already been processed in the current cycle.
This way, it avoids accidentaly calculating some interactions twice.
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
