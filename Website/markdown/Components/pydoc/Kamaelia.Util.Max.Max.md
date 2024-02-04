---
pagename: Components/pydoc/Kamaelia.Util.Max.Max
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Max](/Components/pydoc/Kamaelia.Util.Max.html){.reference}.[Max](/Components/pydoc/Kamaelia.Util.Max.Max.html){.reference}
============================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Max.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Max([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Max}
-------------------------------------------------------------------------------------------

Max() -\> new Max component.

Send a list of values to its \"inbox\" inbox, and the maximum value from
that list is sent out the \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-Max.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Lists of values
:::

::: {.section}
### [Outboxes]{#symbol-Max.Outboxes}

-   **outbox** : Maximum value from the lists
-   **signal** : Shutdown signalling
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
#### [main(self)]{#symbol-Max.main}

Main loop
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
