---
pagename: Components/pydoc/Kamaelia.Support.Data.Rationals
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Data](/Components/pydoc/Kamaelia.Support.Data.html){.reference}.[Rationals](/Components/pydoc/Kamaelia.Support.Data.Rationals.html){.reference}
=======================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Rational fraction conversion/handling](#38){.reference}
    -   [Conversion from floating point to rational
        fraction](#39){.reference}
    -   [Examples](#40){.reference}
    -   [How does conversion work?](#41){.reference}
:::

::: {.section}
Rational fraction conversion/handling {#38}
=====================================

This set of functions assist in creating rational fractions (numbers
represented by a fraction with an integer numerator and denominator).

::: {.section}
[Conversion from floating point to rational fraction]{#conversion-from-floating-point-to-rational-fraction} {#39}
-----------------------------------------------------------------------------------------------------------

The rational(\...) function converts a floating point value to a
rational fraction.

It aims to generate as close an approximation as is reasonably possible,
and to use as small (simple) a numerator and denominator as possible.
:::

::: {.section}
[Examples]{#examples} {#40}
---------------------

Conversion of a floating point number to a rational fraction:

``` {.literal-block}
>>> rational(0.75)
(3, 4)
```

Scale a rational\'s numerator and denominator to fit within limits:

``` {.literal-block}
>>> limit( (1500,2000), 80, -80)
(60, 80)
```

Find the greatest common divisor:

``` {.literal-block}
>>> gcd(18,42)
6
```
:::

::: {.section}
[How does conversion work?]{#how-does-conversion-work} {#41}
------------------------------------------------------

rational(\...) uses the \"continuous fractions\" recursive approximation
technique.

The algorithm effectively generates a continuous fractions up to a
specified depth, and then multiplies them out to generate an integer
numerator and denominator.

All depths are tried up to the maximum depth specified. The least deep
one that yields an exact match is returned. This is also the simplest.

The numerator and denominator are simplified further by dividing them by
their greatest common denominator.

For more information on continuous fractions try these: -
<http://mathworld.wolfram.com/ContinuedFraction.html> -
<http://ourworld.cs.com/christopherereed/confracs.htm> -
<http://www.cut-the-knot.org/do_you_know/fraction.shtml> -
<http://www.mcs.surrey.ac.uk/Personal/R.Knott/Fibonacci/cfINTRO.html#real>
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
