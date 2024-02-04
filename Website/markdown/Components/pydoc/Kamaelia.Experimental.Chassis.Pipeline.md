---
pagename: Components/pydoc/Kamaelia.Experimental.Chassis.Pipeline
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}.[Pipeline](/Components/pydoc/Kamaelia.Experimental.Chassis.Pipeline.html){.reference}
==================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}

------------------------------------------------------------------------

::: {.section}
prefab: Pipeline {#symbol-Pipeline}
----------------

Pipeline(\*components) -\> new Pipeline component.

Encapsulates the specified set of components and wires them up in a
chain (a Pipeline) in the order you provided them.

Keyword arguments:

-   components \-- the components you want, in the order you want them
    wired up. Any Integers set the \"inbox\" inbox size limit for the
    component that follows them.
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
