---
pagename: Components/pydoc/Kamaelia.Experimental.Chassis.Graphline
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}.[Graphline](/Components/pydoc/Kamaelia.Experimental.Chassis.Graphline.html){.reference}
====================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}

------------------------------------------------------------------------

::: {.section}
prefab: Graphline {#symbol-Graphline}
-----------------

Graphline(\[linkages\]\[,boxsizes\],\*\*components) -\> new Graphline
component

Encapsulates the specified set of components and wires them up with the
specified linkages.

Keyword arguments:

-   linkages \-- dictionary mapping (\"componentname\",\"boxname\") to
    (\"componentname\",\"boxname\")
-   boxsizes \-- dictionary mapping (\"componentname\",\"boxname\") to
    size limit for inbox
-   components \-- dictionary mapping names to component instances
    (default is nothing)
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
