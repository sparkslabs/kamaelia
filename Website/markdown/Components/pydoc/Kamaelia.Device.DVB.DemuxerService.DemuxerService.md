---
pagename: Components/pydoc/Kamaelia.Device.DVB.DemuxerService.DemuxerService
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.html){.reference}.[DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.DemuxerService.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.html){.reference}

------------------------------------------------------------------------

::: {.section}
class DemuxerService([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-DemuxerService}
----------------------------------------------------------------------------------------------------------------------------------------------------------

DemuxerService() -\> new DemuxerService component.

Demultiplexes packets from an MPEG transport stream, sent to its
\"inbox\" inbox and sends them, based on their packet ID (PID) to client
who have requested to receive packets with that PID.

::: {.section}
### [Inboxes]{#symbol-DemuxerService.Inboxes}

-   **control** : We will receive shutdown messages here
-   **request** : \'ADD\' and \'REMOVE\' requests from clients
-   **inbox** : This is where we expect to recieve a transport stream
:::

::: {.section}
### [Outboxes]{#symbol-DemuxerService.Outboxes}

-   **outbox** : NOT USED
-   **signal** : Shutdown signalling
-   **pid\_request** : Messages to the source of the transport stream,
    requesting to subscribe/unsubscribe from PIDs
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
#### [errorIndicatorSet(self, packet)]{#symbol-DemuxerService.errorIndicatorSet}
:::

::: {.section}
#### [handleCommand(self, cmd)]{#symbol-DemuxerService.handleCommand}
:::

::: {.section}
#### [main(self)]{#symbol-DemuxerService.main}
:::

::: {.section}
#### [scrambledPacket(self, packet)]{#symbol-DemuxerService.scrambledPacket}
:::

::: {.section}
#### [shutdown(self)]{#symbol-DemuxerService.shutdown}
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
