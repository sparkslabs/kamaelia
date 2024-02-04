---
pagename: Components/pydoc/Kamaelia.Util.RangeFilter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RangeFilter](/Components/pydoc/Kamaelia.Util.RangeFilter.html){.reference}
============================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [RangeFilter](/Components/pydoc/Kamaelia.Util.RangeFilter.RangeFilter.html){.reference}**
:::

-   [Filter items out that are not in range](#152){.reference}
    -   [Example Usage](#153){.reference}
    -   [Behaviour](#154){.reference}
:::

::: {.section}
Filter items out that are not in range {#152}
======================================

RangeFilter passes through items received on its \"inbox\" inbox where
item\[0\] lies within one or more of a specfied set of ranges of value.
Items that don\'t match this are discarded.

::: {.section}
[Example Usage]{#example-usage} {#153}
-------------------------------

Reading all video frames from a YUV4MPEG format video file, but only
passing on video frames 25-49 and 100-199 inclusive further along the
pipeline:

``` {.literal-block}
Pipeline( RateControlledFileReader("myvideo.yuv4mpeg",readmode="bytes"),
          YUV4MPEGToFrame(),
          TagWithSequenceNumber(),
          RangeFilter(ranges=[ (25,49), (100,199) ]),
          ...
        ).run()
```
:::

::: {.section}
[Behaviour]{#behaviour} {#154}
-----------------------

At initialisation, specify a list of value ranges that RangeFilter
should allow. The list should be of the form:

``` {.literal-block}
[ (low,high), (low,high), (low, high), ... ]
```

The ranges specified are inclusive.

Send an item to the \"inbox\" inbox of the form (value, \....). If the
value matches one or more of the ranges specified, then the whole item
(including the value) will immediately be sent on out of the \"outbox\"
outbox.

RangeFilter can therefore be used to select slices through sequence
numbered or timestamped data.

If the size limited inbox is full, this component will pause until it is
able to send out the data,.

If a producerFinished message is received on the \"control\" inbox, this
component will complete parsing any data pending in its inbox, and
finish sending any resulting data to its outbox. It will then send the
producerFinished message on out of its \"signal\" outbox and terminate.

If a shutdownMicroprocess message is received on the \"control\" inbox,
this component will immediately send it on out of its \"signal\" outbox
and immediately terminate. It will not complete processing, or sending
on any pending data.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RangeFilter](/Components/pydoc/Kamaelia.Util.RangeFilter.html){.reference}.[RangeFilter](/Components/pydoc/Kamaelia.Util.RangeFilter.RangeFilter.html){.reference}
====================================================================================================================================================================================================================================================================================

::: {.section}
class RangeFilter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-RangeFilter}
---------------------------------------------------------------------------------------------------

RangeFilter(ranges) -\> new RangeFilter component.

Filters out items of the form (value, \...) not within at least one of a
specified value set of range. Items within range are passed through.

Keyword arguments:

``` {.literal-block}
- ranges  -- list of (low,high) pairs representing ranges of value. Ranges are inclusive.
```

::: {.section}
### [Inboxes]{#symbol-RangeFilter.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-RangeFilter.Outboxes}

-   **outbox** : items in range
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
#### [\_\_init\_\_(self, ranges)]{#symbol-RangeFilter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [canStop(self)]{#symbol-RangeFilter.canStop}

Checks for any shutdown messages arriving at the \"control\" inbox, and
returns true if the component should terminate when it has finished
processing any pending data.
:::

::: {.section}
#### [handleControl(self)]{#symbol-RangeFilter.handleControl}

Collects any new shutdown messages arriving at the \"control\" inbox,
and ensures self.shutdownMsg contains the highest priority one
encountered so far.
:::

::: {.section}
#### [inRange(self, index)]{#symbol-RangeFilter.inRange}

Returns one of the ranges that the specified index falls within,
otherwise returns None.
:::

::: {.section}
#### [main(self)]{#symbol-RangeFilter.main}

Main loop
:::

::: {.section}
#### [mustStop(self)]{#symbol-RangeFilter.mustStop}

Checks for any shutdown messages arriving at the \"control\" inbox, and
returns true if the component should terminate immediately.
:::

::: {.section}
#### [waitSend(self, data, boxname)]{#symbol-RangeFilter.waitSend}

Generator.

Sends data out of the \"outbox\" outbox. If the destination is full
(noSpaceInBox exception) then it waits until there is space. It keeps
retrying until it succeeds.

If the component is ordered to immediately terminate then \"STOP\" is
raised as an exception.
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
