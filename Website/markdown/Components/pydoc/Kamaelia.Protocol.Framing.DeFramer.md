---
pagename: Components/pydoc/Kamaelia.Protocol.Framing.DeFramer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Framing](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}.[DeFramer](/Components/pydoc/Kamaelia.Protocol.Framing.DeFramer.html){.reference}
==================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}

------------------------------------------------------------------------

::: {.section}
class DeFramer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DeFramer}
------------------------------------------------------------------------------------------------

DeFramer -\> new DeFramer component.

Converts string that were framed using the Framer component back into
(tag, data) pairs.

::: {.section}
### [Inboxes]{#symbol-DeFramer.Inboxes}

-   **control** : shutdown messages (producerFinished)
-   **inbox** : framed data strings
:::

::: {.section}
### [Outboxes]{#symbol-DeFramer.Outboxes}

-   **outbox** : deframed (tag, data) pairs
-   **signal** : producerFinished shutdown messages
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
#### [main(self)]{#symbol-DeFramer.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-DeFramer.shutdown}

Shutdown on producerFinished message arriving at \"control\" inbox.
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
