---
pagename: Components/pydoc/Kamaelia.Chassis.Pipeline.Pipeline
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.html){.reference}.[Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.Pipeline.html){.reference}
=================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Chassis.Pipeline.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Pipeline([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Pipeline}
------------------------------------------------------------------------------------------------

Pipeline(\*components) -\> new Pipeline component.

Encapsulates the specified set of components and wires them up in a
chain (a Pipeline) in the order you provided them.

Keyword arguments:

-   components \-- the components you want, in the order you want them
    wired up

::: {.section}
### [Inboxes]{#symbol-Pipeline.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Pipeline.Outboxes}
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
#### [\_\_init\_\_(self, \*components, \*\*argv)]{#symbol-Pipeline.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Pipeline.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-Pipeline.main}

Main loop.
:::
:::

::: {.section}
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
