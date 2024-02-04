---
pagename: Components/pydoc/Kamaelia.Device.DVB.SoftDemux
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[SoftDemux](/Components/pydoc/Kamaelia.Device.DVB.SoftDemux.html){.reference}
================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [DVB\_SoftDemuxer](/Components/pydoc/Kamaelia.Device.DVB.SoftDemux.DVB_SoftDemuxer.html){.reference}**
:::
:::

::: {.section}
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[SoftDemux](/Components/pydoc/Kamaelia.Device.DVB.SoftDemux.html){.reference}.[DVB\_SoftDemuxer](/Components/pydoc/Kamaelia.Device.DVB.SoftDemux.DVB_SoftDemuxer.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class DVB\_SoftDemuxer([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-DVB_SoftDemuxer}
------------------------------------------------------------------------------------------------------------------------------------------------------------

This demuxer expects to recieve the output from a DVB\_Multiplex
component on its primary inbox. It is also provided with a number of
pids. For each pid that it knows about, it forwards the data received on
that PID to an appropriate outbox. Data associated with unknown PIDs in
the datastream is thrown away.

The output here is still transport stream packets. Another layer is
required to decide what to do with these - to yank out the PES and ES
packets.

::: {.section}
### [Inboxes]{#symbol-DVB_SoftDemuxer.Inboxes}

-   **control** : We will receive shutdown messages here
-   **inbox** : This is where we expect to recieve a transport stream
:::

::: {.section}
### [Outboxes]{#symbol-DVB_SoftDemuxer.Outboxes}
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
#### [\_\_init\_\_(self, pidmap)]{#symbol-DVB_SoftDemuxer.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-DVB_SoftDemuxer.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-DVB_SoftDemuxer.shutdown}
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
