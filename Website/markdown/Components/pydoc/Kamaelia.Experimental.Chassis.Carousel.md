---
pagename: Components/pydoc/Kamaelia.Experimental.Chassis.Carousel
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}.[Carousel](/Components/pydoc/Kamaelia.Experimental.Chassis.Carousel.html){.reference}
==================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}

------------------------------------------------------------------------

::: {.section}
prefab: Carousel {#symbol-Carousel}
----------------

Carousel(componentFactory\[,make1stRequest\]\[,boxSize\]) -\> new
Carousel component

Create a Carousel component that makes child components one at a time
(in carousel fashion) using the supplied factory function.

Keyword arguments:

-   componentFactory \-- function that takes a single argument and
    returns a component
-   make1stRequest \-- if True, Carousel will send an initial \"NEXT\"
    request. (default=False)
-   boxsize \-- size limit for \"inbox\" inbox of the created child
    component
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
