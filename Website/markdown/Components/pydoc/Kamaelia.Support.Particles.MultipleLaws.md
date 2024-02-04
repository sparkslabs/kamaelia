---
pagename: Components/pydoc/Kamaelia.Support.Particles.MultipleLaws
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Particles](/Components/pydoc/Kamaelia.Support.Particles.html){.reference}.[MultipleLaws](/Components/pydoc/Kamaelia.Support.Particles.MultipleLaws.html){.reference}
============================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Particle Physics Laws for multiple particles](#0){.reference}
    -   [Example Usage](#1){.reference}
    -   [How does it work?](#2){.reference}
:::

::: {.section}
Particle Physics Laws for multiple particles {#0}
============================================

A class implementing laws for interactions between multiple particle
types, in discrete time simulations. Can be used with the physics
ParticleSystem class. This implementation supports different parameters
for interactions between different particle types.

You specify a mapping between pairs of types of particles and the set of
laws to apply between them.

This class provides the same methods as the SimpleLaws class. It is a
drop in replacement for when you wish to specialise a physics model to
apply different laws depending on the types of particles involved.

::: {.section}
[Example Usage]{#example-usage} {#1}
-------------------------------

For two types of particle \"Entity\" and \"Attribute\": - Entities only
repel each other - Attributes bond at a distance of 200 units -
Attributes bond to entities at a distance of 50 units

``` {.literal-block}
mapping = { ("Entity","Entity") :SimpleLaws(maxBondForce=0, repulsionStrength=10),
            ("Attribute","Attribute") : SimpleLaws(bondLength=200),
            ("Entity","Attribute") : SimpleLaws(bondLength=50),
          }

laws = MultipleLaws( typesToLaws=mapping,
                   )
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#2}
--------------------------------------

It provides the same method interface as the SimpleLaws class, but
applies different sets of laws depending on the particle types passed
when methods are called (SimpleLaws always applies the same rules
irrespective).

The different laws provided are stored with the specified mappings. If
you specify a mapping for (typeA,typeB), then it will also be applied to
(typeB,typeA). You do not need to specify the mappings both ways round,
though you may if you wish.

If you do not specify the complete set of mappings for the particle
types to all of each other, then a default law (if specified) will be
used to fill in the gaps.

Note that the default law does not get applied to particle types not
mentioned when in the mappings you provide. For example, if your
mappings only cover particle types \'A\',\'B\', and \'C\', then
interactions involving a new type \'D\' will cause an exception to be
raised.

The \'maximum interaction radius\' for a given particle type is set to
the maximum of the interaction radii for all the different interaction
laws it is involved in.
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
