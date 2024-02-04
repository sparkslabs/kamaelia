---
pagename: Components/pydoc/Kamaelia.Util.RateFilter.OnDemandLimit
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RateFilter](/Components/pydoc/Kamaelia.Util.RateFilter.html){.reference}.[OnDemandLimit](/Components/pydoc/Kamaelia.Util.RateFilter.OnDemandLimit.html){.reference}
=====================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.RateFilter.html){.reference}

------------------------------------------------------------------------

::: {.section}
class OnDemandLimit([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-OnDemandLimit}
-----------------------------------------------------------------------------------------------------

OnDemandLimit() -\> new OnDemandLimit component.

A component that receives data items, but only emits them on demand, one
at a time, when \"NEXT\" messages are received on the \"slidecontrol\"
inbox.

::: {.section}
### [Inboxes]{#symbol-OnDemandLimit.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data items to be passed on, on demand.
-   **slidecontrol** : \'NEXT\' requests to emit a data item.
:::

::: {.section}
### [Outboxes]{#symbol-OnDemandLimit.Outboxes}

-   **outbox** : Data items, when requested.
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
#### [main(self)]{#symbol-OnDemandLimit.main}

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
