---
pagename: Components/pydoc/Kamaelia.Util.Comparator.Comparator
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Comparator](/Components/pydoc/Kamaelia.Util.Comparator.html){.reference}.[Comparator](/Components/pydoc/Kamaelia.Util.Comparator.Comparator.html){.reference}
===============================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Comparator.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Comparator([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Comparator}
--------------------------------------------------------------------------------------------------

Comparator() -\> new Comparator component.

Compares items received on \"inA\" inbox with items received on \"inB\"
inbox. For each pair, outputs True if items compare equal, otherwise
False.

::: {.section}
### [Inboxes]{#symbol-Comparator.Inboxes}

-   **control** : NOT USED
-   **inbox** : NOT USED
-   **inB** : Source \'B\' of items to compare
-   **inA** : Source \'A\' of items to compare
:::

::: {.section}
### [Outboxes]{#symbol-Comparator.Outboxes}

-   **outbox** : Result of comparison
-   **signal** : NOT USED
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
#### [combine(self, valA, valB)]{#symbol-Comparator.combine}

Returns result of (valA == valB)

Reimplement this method to change the type of comparison from equality
testing.
:::

::: {.section}
#### [mainBody(self)]{#symbol-Comparator.mainBody}

Main loop body.
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
