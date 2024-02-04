---
pagename: Components/pydoc/Kamaelia.Util.FirstOnly
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[FirstOnly](/Components/pydoc/Kamaelia.Util.FirstOnly.html){.reference}
========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [FirstOnly](/Components/pydoc/Kamaelia.Util.FirstOnly.FirstOnly.html){.reference}**
:::

-   [Pass on the first item only](#238){.reference}
    -   [Example Usage](#239){.reference}
    -   [Behaviour](#240){.reference}
:::

::: {.section}
Pass on the first item only {#238}
===========================

The first item sent to FirstOnly will be passed on. All other items are
ignored.

::: {.section}
[Example Usage]{#example-usage} {#239}
-------------------------------

Displaying the frame rate, just once, from video when it is decoded:

``` {.literal-block}
Pipeline( ...
          DiracDecoder(),
          FirstOnly(),
          SimpleDetupler("frame_rate"),
          ConsoleEchoer(),
        )
```
:::

::: {.section}
[Behaviour]{#behaviour} {#240}
-----------------------

The first data item sent to FirstOnly\'s \"inbox\" inbox is immediately
sent on out of its \"outbox\" outbox.

Any subsequent data sent to its \"inbox\" inbox is discarded.

If a producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox. It is immediately sent on out of the \"signal\"
outbox and the component then immediately terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[FirstOnly](/Components/pydoc/Kamaelia.Util.FirstOnly.html){.reference}.[FirstOnly](/Components/pydoc/Kamaelia.Util.FirstOnly.FirstOnly.html){.reference}
==========================================================================================================================================================================================================================================================================

::: {.section}
class FirstOnly([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-FirstOnly}
-------------------------------------------------------------------------------------------------

FirstOnly() -\> new FirstOnly component.

Passes on the first item sent to it, and discards everything else.

::: {.section}
### [Inboxes]{#symbol-FirstOnly.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data items
:::

::: {.section}
### [Outboxes]{#symbol-FirstOnly.Outboxes}

-   **outbox** : First data item received
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
#### [main(self)]{#symbol-FirstOnly.main}

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
