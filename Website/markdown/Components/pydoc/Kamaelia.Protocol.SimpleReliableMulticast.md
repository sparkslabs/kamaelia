---
pagename: Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SimpleReliableMulticast](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.html){.reference}
================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Annotator](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.Annotator.html){.reference}**
-   **component
    [RecoverOrder](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.RecoverOrder.html){.reference}**
-   **prefab
    [SRM\_Receiver](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.SRM_Receiver.html){.reference}**
-   **prefab
    [SRM\_Sender](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.SRM_Sender.html){.reference}**
:::

-   [Simple Reliable Multicast](#606){.reference}
    -   [Example Usage](#607){.reference}
    -   [How does it work?](#608){.reference}
:::

::: {.section}
Simple Reliable Multicast {#606}
=========================

A pair of Pipelines for encoding (and decoding again) a stream of data
such that is can be transported over an unreliable connection that may
lose, duplicate or reorder data.

These components will ensure that data arrives in the right order and
that duplicates are removed. However it cannot recover lost data.

::: {.section}
[Example Usage]{#example-usage} {#607}
-------------------------------

Reliably transporting a file over multicast (assuming no packets are
lost):

``` {.literal-block}
Pipeline(RateControlledFileReader("myfile"),
         SRM_Sender(),
         Multicast_transceiver("0.0.0.0", 0, "1.2.3.4", 1000),
        ).activate()
```

On the client:

``` {.literal-block}
class discardSeqnum(component):
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                (_, data) = self.recv("inbox")
                self.send(data,"outbox")

Pipeline( Multicast_transceiver("0.0.0.0", 1000, "1.2.3.4", 0)
          SRM_Receiver(),
          discardSeqnum(),
          ConsoleEchoer()
        ).activate()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#608}
--------------------------------------

SRM\_Sender is a Pipeline of three components:

-   Annotator \-- annotates a data stream with sequence numbers
-   Framer \-- frames the data
-   DataChunker \-- inserts markers between frames

SRM\_Receiver is a Pipeline of three components:

-   DataDeChunker \-- recovers chunks based on markers
-   DeFramer \-- removes framing
-   RecoverOrder \-- sorts data by sequence numbers

These components will ensure that data arrives in the right order and
that duplicates are removed. However it cannot recover lost data. But
the final output is (seqnum,data) pairs - so there is enough information
for the receiver to know that data has been lost.

The Annotator component receives data on its \"inbox\" inbox, and emits
(seqnum, data) tuples on its \"outbox\" outbox. The sequence numbers
start at 1 and increments by 1 for each item.

The Annotator component does not terminate and ignores messages arriving
on its \"control\" inbox.

See documentation for the other components for details of their design
and behaviour.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SimpleReliableMulticast](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.html){.reference}.[Annotator](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.Annotator.html){.reference}
====================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Annotator([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Annotator}
-------------------------------------------------------------------------------------------------

Annotator() -\> new Annotator component.

Takes incoming data and outputs (n, data) where n is an incrementing
sequence number, starting at 1.

::: {.section}
### [Inboxes]{#symbol-Annotator.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Annotator.Outboxes}
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
#### [main(self)]{#symbol-Annotator.main}

Main loop
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SimpleReliableMulticast](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.html){.reference}.[RecoverOrder](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.RecoverOrder.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================

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

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SimpleReliableMulticast](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.html){.reference}.[SRM\_Receiver](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.SRM_Receiver.html){.reference}
===========================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: SRM\_Receiver {#symbol-SRM_Receiver}
---------------------

Simple Reliable Multicast receiver.

Dechunks, deframes and recovers the order of a data stream that has been
encoded by SRM\_Sender.

Final emitted data is (seqnum, data) pairs.

This is a Pipeline of components.
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[SimpleReliableMulticast](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.html){.reference}.[SRM\_Sender](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.SRM_Sender.html){.reference}
=======================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: SRM\_Sender {#symbol-SRM_Sender}
-------------------

Simple Reliable Multicast sender.

Sequence numbers, frames and chunks a data stream, making it suitable
for sending over an unreliable connection that may lose, reorder or
duplicate data. Can be decoded by SRM\_Receiver.

This is a Pipeline of components.
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
