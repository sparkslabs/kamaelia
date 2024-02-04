---
pagename: Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.RecoverOrder
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SimpleReliableMulticast](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.html){.reference}.[RecoverOrder](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.RecoverOrder.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.html){.reference}

------------------------------------------------------------------------

::: {.section}
class RecoverOrder([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-RecoverOrder}
----------------------------------------------------------------------------------------------------

RecoverOrder() -\> new RecoverOrder component.

Receives and buffers (seqnum, data) pairs, and reorders them by
ascending sequence number and emits them (when its internal buffer is
full).

::: {.section}
### [Inboxes]{#symbol-RecoverOrder.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-RecoverOrder.Outboxes}
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
#### [main(self)]{#symbol-RecoverOrder.main}

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
