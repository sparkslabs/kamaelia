---
pagename: Components/pydoc/Kamaelia.Util.LossyConnector
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[LossyConnector](/Components/pydoc/Kamaelia.Util.LossyConnector.html){.reference}
==================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [LossyConnector](/Components/pydoc/Kamaelia.Util.LossyConnector.LossyConnector.html){.reference}**
:::

-   [Lossy connections between components](#186){.reference}
    -   [Example Usage](#187){.reference}
    -   [How does it work?](#188){.reference}
:::

::: {.section}
Lossy connections between components {#186}
====================================

A component that passes on any data it receives, but will throw it away
if the next component\'s inbox is unable to accept new items.

::: {.section}
[Example Usage]{#example-usage} {#187}
-------------------------------

Using a lossy connector to drop excess data::

:   src = fastProducer().activate() lsy = LossyConnector().activate()
    dst = slowConsumer().activate()

    src.link( (src,\"outbox\"), (lsy,\"inbox\") ) src.link(
    (lsy,\"outbox\"), (dst,\"inbox\"), pipewidth=1 )

The outbox of the lossy connector is joined to a linkage that can buffer
a maximum of one item. Once full, the lossy connector causes items to be
dropped.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#188}
--------------------------------------

This component receives data on its \"inbox\" inbox and immediately
sends it on out of its \"oubox\" outbox.

If the act of sending the data causes a noSpaceInBox exception, then it
is caught, and the data that it was trying to send is simply discarded.

I a producerFinished or shutdownMicroprocess message is received on the
component\'s \"control\" inbox, then the message is forwarded on out of
its \"signal\" outbox and the component then immediately terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[LossyConnector](/Components/pydoc/Kamaelia.Util.LossyConnector.html){.reference}.[LossyConnector](/Components/pydoc/Kamaelia.Util.LossyConnector.LossyConnector.html){.reference}
===================================================================================================================================================================================================================================================================================================

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
