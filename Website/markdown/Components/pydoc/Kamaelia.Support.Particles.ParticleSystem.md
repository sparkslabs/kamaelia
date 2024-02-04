---
pagename: Components/pydoc/Kamaelia.Support.Particles.ParticleSystem
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Particles](/Components/pydoc/Kamaelia.Support.Particles.html){.reference}.[ParticleSystem](/Components/pydoc/Kamaelia.Support.Particles.ParticleSystem.html){.reference}
================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Discrete time particle physics simulation](#3){.reference}
    -   [Example Usage](#4){.reference}
    -   [How does it work?](#5){.reference}
:::

::: {.section}
Discrete time particle physics simulation {#3}
=========================================

A discrete time simulator of a system of bonded and unbonded particles,
of multiple types.

The actual physics calculations are deferred to the particles
themselves. You can have as many, or few, spatial dimensions as you
like.

::: {.section}
[Example Usage]{#example-usage} {#4}
-------------------------------

Create 3 particles, two of which are bonded and move noticeably closer
after 5 cycles of simulation:

``` {.literal-block}
>>> laws = SimpleLaws(bondLength=5)
>>> sim = ParticleSystem(laws)
>>> sim.add( Particle(position=(10,10)) )
>>> sim.add( Particle(position=(10,20)) )
>>> sim.add( Particle(position=(30,40)) )
>>> sim.particles[0].makeBond(sim.particles, 1)   # bond 1st and 2nd particles
>>> for p in sim.particles: print p.getLoc()
...
(10, 10)
(10, 20)
(30, 40)
>>> sim.run(cycles=5)
>>> for p in sim.particles: print p.getLoc()
...
[10.0, 13.940067328]
[10.0, 16.059932671999999]
[30, 40]
>>>
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#5}
--------------------------------------

Set up ParticleSystem by instantiating, specifying the laws to act
between particles and an (optional) set of initial particles.

Particles should be derived from the Particle base class (or have
equivalent functionality).

Particles can be added or removed from the system by reference, or
removed by their ID.

ParticleSystem will work for particles in space with any number of
dimensions - so long as all particles use the same!

Bonds between particles are up to the particles to manage for
themselves.

The simulation runs in cycles when the run(\...) method is called. Each
cycle advances the \'tick\' count by 1. The tick count starts at zero,
unless otherwise specified during initialization.

The following attributes store the particles registered in
ParticleSystem: - particles \-- simple list - particleDict \--
dictionary, indexed by particle.ID

ParticleSystem uses a SpatialIndexer object to speed up calculations.
SpatialIndexer reduce the search space when determining what particles
lie within a given region (radius of a point).

If your code changes the position of a particle, the simulator must be
informed, so it can update its spatial indexing data, by calling
updateLoc(\...)

The actual interactions between particles are calculated by the
particles themselves, *not* by ParticleSystem.

ParticleSystem calls the doInteractions(\...) methods of all particles
so they can influence each other. It then calls the update(\...) methods
of all particles so they can all update their positions and velocities
ready for the next cycle.

This is a two stage process so that, in a given cycle, all particles see
each other at the same positions, irrespective of which particle\'s
doInteractions(\...) method is called first. Particles should not apply
their velocities to update their position until their update(\...)
method is called.
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
