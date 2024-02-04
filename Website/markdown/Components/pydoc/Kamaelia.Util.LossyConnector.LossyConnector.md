---
pagename: Components/pydoc/Kamaelia.Util.LossyConnector.LossyConnector
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[LossyConnector](/Components/pydoc/Kamaelia.Util.LossyConnector.html){.reference}.[LossyConnector](/Components/pydoc/Kamaelia.Util.LossyConnector.LossyConnector.html){.reference}
===================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.LossyConnector.html){.reference}

------------------------------------------------------------------------

::: {.section}
class LossyConnector([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-LossyConnector}
------------------------------------------------------------------------------------------------------

LossyConnector() -\> new LossyConnector component

Component that forwards data from inbox to outbox, but discards data if
destination is full.

::: {.section}
### [Inboxes]{#symbol-LossyConnector.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data to be passed on
:::

::: {.section}
### [Outboxes]{#symbol-LossyConnector.Outboxes}

-   **outbox** : Data received on \'inbox\' inbox
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
#### [mainBody(self)]{#symbol-LossyConnector.mainBody}

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
