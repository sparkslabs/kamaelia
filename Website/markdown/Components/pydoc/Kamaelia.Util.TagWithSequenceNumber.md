---
pagename: Components/pydoc/Kamaelia.Util.TagWithSequenceNumber
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[TagWithSequenceNumber](/Components/pydoc/Kamaelia.Util.TagWithSequenceNumber.html){.reference}
================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [TagWithSequenceNumber](/Components/pydoc/Kamaelia.Util.TagWithSequenceNumber.TagWithSequenceNumber.html){.reference}**
:::

-   [Tags items with an incrementing sequence number](#220){.reference}
    -   [Example Usage](#221){.reference}
    -   [Behaviour](#222){.reference}
:::

::: {.section}
Tags items with an incrementing sequence number {#220}
===============================================

TagWithSequenceNumber tags items with a sequence numbers, for example:
0, 1, 2, 3, \... etc. The default initial value of the sequence is a 0.

It takes in items on its \"inbox\" inbox and outputs (seqnum, item)
tuples on its \"outbox\" outbox.

::: {.section}
[Example Usage]{#example-usage} {#221}
-------------------------------

Tagging frames from a Dirac video file with a frame number, starting
with 1:

``` {.literal-block}
Pipeline( RateControlledFileReader("videofile.dirac", readmode="bytes", rate=... ),
          DiracDecoder(),
          TagWithSequenceNumber(initial=1),
          ...
        )
```
:::

::: {.section}
[Behaviour]{#behaviour} {#222}
-----------------------

At initialisation, specify the initial sequence number to use.

Send an item to TagWithSequenceNumber\'s \"inbox\" inbox, and it will
send (seqnum, item) to its \"outbox\" outbox.

The sequence numbers begin 0, 1, 2, 3, \... etc ad infinitum.

If a producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox. It is immediately sent on out of the \"signal\"
outbox and the component then immediately terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[TagWithSequenceNumber](/Components/pydoc/Kamaelia.Util.TagWithSequenceNumber.html){.reference}.[TagWithSequenceNumber](/Components/pydoc/Kamaelia.Util.TagWithSequenceNumber.TagWithSequenceNumber.html){.reference}
======================================================================================================================================================================================================================================================================================================================================

::: {.section}
class TagWithSequenceNumber([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TagWithSequenceNumber}
-------------------------------------------------------------------------------------------------------------

TagWithSequenceNumber() -\> new TagWithSequenceNumber component.

Send \'item\' to the \"inbox\" inbox and it will be tagged with a
sequence number, and sent out as (seqnum, \'item\') to the \"outbox\"
outbox.

Sequence numbering goes 0, 1, 2, 3, \... etc.

::: {.section}
### [Inboxes]{#symbol-TagWithSequenceNumber.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Items
:::

::: {.section}
### [Outboxes]{#symbol-TagWithSequenceNumber.Outboxes}

-   **outbox** : Items tagged with a sequence number, in the form
    (seqnum, item)
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
#### [\_\_init\_\_(self\[, initial\])]{#symbol-TagWithSequenceNumber.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-TagWithSequenceNumber.main}

Main loop
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
