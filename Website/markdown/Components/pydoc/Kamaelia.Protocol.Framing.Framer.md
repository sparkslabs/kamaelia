---
pagename: Components/pydoc/Kamaelia.Protocol.Framing.Framer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[Framing](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}.[Framer](/Components/pydoc/Kamaelia.Protocol.Framing.Framer.html){.reference}
==============================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Framer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Framer}
----------------------------------------------------------------------------------------------

Framer() -\> new Framer component.

Frames (tag, data) pairs into strings containing the same data.

::: {.section}
### [Inboxes]{#symbol-Framer.Inboxes}

-   **control** : shutdown messages (producerFinished)
-   **inbox** : (tag, data) pairs to be framed
:::

::: {.section}
### [Outboxes]{#symbol-Framer.Outboxes}

-   **outbox** : framed data strings
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
#### [main(self)]{#symbol-Framer.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-Framer.shutdown}

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
