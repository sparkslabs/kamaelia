---
pagename: Components/pydoc/Kamaelia.Protocol.RecoverOrder
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[RecoverOrder](/Components/pydoc/Kamaelia.Protocol.RecoverOrder.html){.reference}
==========================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Recover Order of Sequence Numbered Items](#640){.reference}
    -   [Example Usage](#641){.reference}
    -   [Behaviour](#642){.reference}
    -   [Implementation details](#643){.reference}
:::

::: {.section}
Recover Order of Sequence Numbered Items {#640}
========================================

Recovers the order of data tagged with sequence numbers. Designed to
cope with sequence numbers that have to eventually wrap.

Send (seqnum, data) tuples to the \"inbox\" inbox and they will be sent
out of the \"outbox\" outbox ordered by ascending sequence number.

::: {.section}
[Example Usage]{#example-usage} {#641}
-------------------------------

Recovering the order of RTP packets received over multicast:

``` {.literal-block}
Pipeline( Multicast_transceiver("0.0.0.0", 1600, "224.168.2.9", 0),
          SimpleDetupler(1),              # discard the source address
          RTPDeframer(),
          RecoverOrder(bufsize=64, modulo=65536),
          SimpleDetupler(1),              # discard sequence numbers
        ).activate()
```
:::

::: {.section}
[Behaviour]{#behaviour} {#642}
-----------------------

At initialisation, specify the size of buffer and the modulo (wrapping
point) for sequence numbers.

Send (seqnum, data) tuples to the \"inbox\" inbox and they will be
buffered. Once the buffer is full, for every item sent to the \"inbox\"
inbox, one will be emitted from the \"outbox\" outbox. The ones that are
emitted will have been reordered by their sequence number.

You must ensure you choose a sufficiently large buffer size for the
expected amount of reordering required. If an item arrives too late, it
RecoverOrder will not be able to place it in its correct position in the
sequence. It will still be emitted, but out of order.

This component does not terminate. It ignores any messages sent to its
\"control\" inbox.
:::

::: {.section}
[Implementation details]{#implementation-details} {#643}
-------------------------------------------------

The items are held in an internal buffer. The buffer is always in order
- with the earliest sequence number at the front. Once the buffer is
full, items are taken out from the front - thereby ensuring any delayed
out-of-order items are given every possible chance to make it.

Since sequence numbers eventually wrap, a given sequence number could
equally represent a data item that is very late, or very early.

This decision is made about a threshold - which is chosen to be the
point in the sequence number line roughly furthest from the sequence
numbers of the items in the buffer. This point is the sequence number of
the middle item in the buffer, plus modulo/2:

``` {.literal-block}
      Data in the buffer
      .-------^--------.
      '                '
|=====XX=X==XXXXXX=XX==X==================================================|
|             ^                                    ^                      |
0             |                                    |                    modulo
           midpoint                             midpoint
              |                                + modulo/2
|<---LATE---->|<--------------EARLY--------------->|<------------LATE---->|
      A       |                 B                  |              C
                                             (aka. threshold)
```

Items with a sequence number after this threshold point are deemed to be
late (rather than ridiculously early). An item arriving with sequence
number B (marked above) has arrived early, and so should be appended to
the end of the data items in the buffer. Conversely, items arriving with
sequence numbers A or C (also marked above) must be late, so will be
inserted at the front of the buffer.

This is implemented by adding modulo to all sequence numbers below the
threshold when performing comparisons to determine where to insert the
new sequence number into the buffer (the insertion point is found by
doing a binary search). You can think of this as moving ranges A and B
after range C.
:::
:::

------------------------------------------------------------------------

::: {.section}
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
