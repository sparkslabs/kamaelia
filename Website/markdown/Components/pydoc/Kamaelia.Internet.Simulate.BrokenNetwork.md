---
pagename: Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[Simulate](/Components/pydoc/Kamaelia.Internet.Simulate.html){.reference}.[BrokenNetwork](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.html){.reference}
===============================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Duplicate](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.Duplicate.html){.reference}**
-   **component
    [Reorder](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.Reorder.html){.reference}**
-   **component
    [Throwaway](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.Throwaway.html){.reference}**
:::

-   [Broken Network Simulation](#133){.reference}
    -   [Example Usage](#134){.reference}
    -   [Duplicate, Throwaway, Reorder](#135){.reference}
    -   [More details](#136){.reference}
    -   [History](#137){.reference}
:::

::: {.section}
Broken Network Simulation {#133}
=========================

Components to simulate properties of an unreliable network connection.
Specifically: out of order delivery, duplication, and loss of packets.

Original author: Tom Gibson (whilst at BBC)

::: {.section}
[Example Usage]{#example-usage} {#134}
-------------------------------

Testing a forward-error correction scheme to cope with an unreliable
network:

``` {.literal-block}
Pipeline( RateControlledFileReader("sourcefile",rate=1000000),
          MyForwardErrorCorrector(),
          Duplicate(),
          Throwaway(),
          Reorder(),
          MyErrorRecoverer(),
          SimpleFileWriter("receiveddata")
        ).activate()
```
:::

::: {.section}
[Duplicate, Throwaway, Reorder]{#duplicate-throwaway-reorder} {#135}
-------------------------------------------------------------

These three components all receive data and, respectively, randomly
duplicate packets, re-order packets or throw some packets away.

They can be used to simulate the effects of multicast delivery over
wireless or a WAN.
:::

::: {.section}
[More details]{#more-details} {#136}
-----------------------------

These component all receive data on their \"inbox\" inbox and send it on
to their \"outbox\" outbox. However, they will sometimes tamper with the
data in the manners described!

None of these components terminate when sent shutdown messages.
:::

::: {.section}
[History]{#history} {#137}
-------------------

This was used for the development of a simple recovery protocol. The
actual version in use replaces the string2tuple and tuple2string code
(in sketches in tomg.py, omitted here), with something more robust.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[Simulate](/Components/pydoc/Kamaelia.Internet.Simulate.html){.reference}.[BrokenNetwork](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.html){.reference}.[Duplicate](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.Duplicate.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Duplicate([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Duplicate}
-------------------------------------------------------------------------------------------------

Duplicate() -\> new component.

This component passes on data it receives. Sometimes it randomly
duplicates items.

::: {.section}
### [Inboxes]{#symbol-Duplicate.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Duplicate.Outboxes}
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
#### [main(self)]{#symbol-Duplicate.main}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[Simulate](/Components/pydoc/Kamaelia.Internet.Simulate.html){.reference}.[BrokenNetwork](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.html){.reference}.[Reorder](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.Reorder.html){.reference}
==============================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Reorder([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Reorder}
-----------------------------------------------------------------------------------------------

Reorder() -\> new component

This component passes on data it receives, but will sometimes jumble it
up (reordering it).

::: {.section}
### [Inboxes]{#symbol-Reorder.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Reorder.Outboxes}
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
#### [main(self)]{#symbol-Reorder.main}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[Simulate](/Components/pydoc/Kamaelia.Internet.Simulate.html){.reference}.[BrokenNetwork](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.html){.reference}.[Throwaway](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.Throwaway.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Throwaway([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Throwaway}
-------------------------------------------------------------------------------------------------

Throwaway() -\> new component.

This component passes on data it receives, but sometimes it doesn\'t!

::: {.section}
### [Inboxes]{#symbol-Throwaway.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Throwaway.Outboxes}
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
#### [main(self)]{#symbol-Throwaway.main}
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
