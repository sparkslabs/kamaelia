---
pagename: Components/pydoc/Kamaelia.Support.Particles.SimpleLaws
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Particles](/Components/pydoc/Kamaelia.Support.Particles.html){.reference}.[SimpleLaws](/Components/pydoc/Kamaelia.Support.Particles.SimpleLaws.html){.reference}
========================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Simple Particle Physics Laws](#6){.reference}
    -   [Example usage](#7){.reference}
    -   [The physics model used](#8){.reference}
    -   [How does it work?](#9){.reference}
:::

::: {.section}
Simple Particle Physics Laws {#6}
============================

A class implementing laws for interactions between particles in discrete
time simulations. Can be used with the physics ParticleSystem class.
Laws are based on the inverse square law.

Different laws are applied for \'bonded\' and \'unbonded\' particles.
Unbonded particles repel. Repulsion and attraction forces balance for
bonded particles at a specified \"bond length\".

There are a range of parameters that can be set at initialisation. All
have sensible defaults.

::: {.section}
[Example usage]{#example-usage} {#7}
-------------------------------

Laws for particles that bond at a distance of 200 units:

``` {.literal-block}
>>> laws = SimpleLaws(bondLength=200)
>>> laws.bonded("","", 200, 200**2)
0.0
>>> laws.bonded("","", 210, 210**2)
2.0
>>> laws.bonded("","", 195, 195**2)
1.0
```

Laws for particles that decelerate *fast*:

``` {.literal-block}
>>> laws = SimpleLaws(damp=0.5)
>>> velocity = [10.0, 5.0]
>>> laws.dampening("", velocity)
[5.0, 2.5]
```

Laws for particles that don\'t repel much but bond extra strongly:

``` {.literal-block}
>>> laws = SimpleLaws(repulsionStrength = 1.0, maxBondForce = 40.0)
>>> laws.unbonded("","", 50, 50**2)
-4.0
>>> laws.bonded("","", 50, 50**2)
-20.0
```
:::

::: {.section}
[The physics model used]{#the-physics-model-used} {#8}
-------------------------------------------------

Instances of this class provide methods for calculating the force that
acts between a pair of particles when bonded or unbonded. It can also
calculate any reduction in velocity due to \'friction\'.

Repulsion forces are calculated using the inverse square law (1 /
distance squared).

Bonding attraction and repulsion forces are calculated using Hook\'s law
for springs. However a cut-off is applied so the force is never greater
than when the bond is stretched to twice its resting length.

There are also other cut-offs (described below) to help prevent a
simulation becoming unstable, and to help speed up simulation.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#9}
--------------------------------------

You specify arguments to control the strengths of bonding and repulsion
(unbonded) forces and the distances they act over.

You can also specify friction and cutoffs for maximum and minimum
velocities. These latter arguments are \'fudge factors\' that you can
use to help stop a system spiralling out of control. Note that in a
discrete time simulation, if particle velocities/accelerations are too
great the simulation can become unstable and particles will fly
everywhere!

You may also specify a \'maximum interaction radius\' - the distance at
which, for unbonded particles, a simulator need not bother calculating
the forces acting (because they are too small to worry about). This is
to allow simulators to run faster by reducing the number of calculations
performed per cycle.

For unspecified arguments, their defaults are scaled appropriately for
the bondLength you specify, such that behaviour will appear unchanged,
just at a different scaling.
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
