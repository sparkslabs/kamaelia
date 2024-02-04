---
pagename: Components/pydoc/Kamaelia.Chassis.Seq.Seq
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Seq](/Components/pydoc/Kamaelia.Chassis.Seq.html){.reference}.[Seq](/Components/pydoc/Kamaelia.Chassis.Seq.Seq.html){.reference}
========================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Chassis.Seq.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Seq([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Seq}
-------------------------------------------------------------------------------------------

Seq(\*sequence) -\> new Seq component.

Runs a set of components in sequence, one after the other. Their
\"inbox\" inbox and \"outbox\" outbox are forwarded to the \"inbox\"
inbox and \"outbox\" outbox of the Seq component.

Keyword arguments:

-   \*sequence \-- Components that will be run, in sequence. Can also
    include strings that will be output to the console.

::: {.section}
### [Inboxes]{#symbol-Seq.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Seq.Outboxes}
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
#### [\_\_init\_\_(self, \*sequence)]{#symbol-Seq.__init__}
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Seq.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-Seq.main}
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
