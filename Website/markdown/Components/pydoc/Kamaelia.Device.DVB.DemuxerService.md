---
pagename: Components/pydoc/Kamaelia.Device.DVB.DemuxerService
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.html){.reference}
==========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.DemuxerService.html){.reference}**
:::

-   [DVB-T (Digital Terrestrial TV) Demuxing Service](#475){.reference}
    -   [Example Usage](#476){.reference}
    -   [How does it work?](#477){.reference}
:::

::: {.section}
DVB-T (Digital Terrestrial TV) Demuxing Service {#475}
===============================================

A component for demultiplexing packets by packet ID (PID) from DVB/MPEG
transport streams. Provides this as a service, to which other components
can subscribe as clients, requesting to receive packets with certain
PIDs.

::: {.section}
[Example Usage]{#example-usage} {#476}
-------------------------------

See
[Kamaelia.Device.DVB.Receiver](/Components/pydoc/Kamaelia.Device.DVB.Receiver.html){.reference}
for examples of use.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#477}
--------------------------------------

DemuxerService takes MPEG transport stream packets, sent to its
\"inbox\" inbox and determines the packet ID (PID) of each, then
distributes them to all clients who are after packets with that PID.

To be a client, send a \'ADD\' or \'REMOVE\' message to the \"request\"
inbox, requesting to be sent (or no longer be sent) packets with
particular PIDs, and specifying the inbox to which you want the packets
to be sent. The format of these requests is:

``` {.literal-block}
("ADD",    [pid, pid, ...], (dest_component, dest_inboxname))
("REMOVE", [pid, pid, ...], (dest_component, dest_inboxname))
```

DemuxerService will automatically do the wiring or unwiring needed to
ensure the packets you have requested get sent to the inbox you
specified.

Send an \'ADD\' request, and you will immediately start receiving
packets with those PIDs. Send a \'REMOVE\' request and you will shortly
no longer receive packets with the PIDs you specify. Note that you may
still receive some packets after your \'REMOVE\' request.

DemuxerService sends its own identical format \'ADD\' and \'REMOVE\'
requests out of its \"pid\_request\" outbox. Wire this to the source of
MPEG transport stream packets, if that source needs to know what PIDs it
is expected to provide.

This component will terminate if a shutdownMicroprocess or
producerFinished message is sent to the \"control\" inbox. The message
will be forwarded on out of the \"signal\" outbox just before
termination.

When it terminates, this component will unwire itself from all clients
to which it has been sending packets.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.html){.reference}.[DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.DemuxerService.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================================================

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
