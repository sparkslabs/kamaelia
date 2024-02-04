---
pagename: Components/pydoc/Kamaelia.Device.DVB.Receiver
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Receiver](/Components/pydoc/Kamaelia.Device.DVB.Receiver.html){.reference}
==============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **prefab
    [Receiver](/Components/pydoc/Kamaelia.Device.DVB.Receiver.Receiver.html){.reference}**
:::

-   [DVB-T (Digital Terrestrial TV) Tuner & Demuxing
    Service](#525){.reference}
    -   [Example Usage](#526){.reference}
    -   [How does it work?](#527){.reference}
:::

::: {.section}
DVB-T (Digital Terrestrial TV) Tuner & Demuxing Service {#525}
=======================================================

Tunes to the specified frequency, using the specified parameters, using
a DVB tuner device; then demultiplexes packets by packet ID (PID) from
DVB/MPEG transport streams. Provides this as a service, to which other
components can subscribe as clients, requesting to receive packets with
certain PIDs.

This is a prefab component built out of a Tuner and DemuxerService
component.

::: {.section}
[Example Usage]{#example-usage} {#526}
-------------------------------

(Using experimental
[Kamaelia.Experimental.Services](/Components/pydoc/Kamaelia.Experimental.Services.html){.reference}
components)

Set up receiver as a named public service, then subscribe to specific
PIDs for recording a stream and some event information:

``` {.literal-block}
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

RegisterService( Receiver(505.833330, feparams),
                 {"DEMUXER":"inbox"}
               ).activate()

Pipeline( Subscribe("DEMUXER", [600,601]),
          SimpleFileWriter("recording_of_600_and_601.ts"),
        ).activate()

Pipeline( Subscribe("DEMUXER", [18]),
          SimpleFileWriter("event_information_data.ts")
        ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#527}
--------------------------------------

This component is a prefab combining a Tuner and a DemuxerService
component.

Use this component in exactly the same way as you would use the
[Kamaelia.Device.DVB.DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.html){.reference}
component. The only difference is that requests should be sent to the
\"inbox\" inbox, instead of a different one.

To request to be sent packets with particular PIDs, send messages of the
form:

> (\"ADD\", (dest\_component, dest\_inboxname), \[pid, pid, \...\])
> (\"REMOVE\", (dest\_component, dest\_inboxname), \[pid, pid, \...\])

For more details, see
[Kamaelia.Device.DVB.DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.html){.reference}.

Internally, the DemuxerService component is wired so that its requests
for PIDs go straight back to the Tuner component. When a client makes a
request, the DemuxerService therefore automatically asks the Tuner to
give it only the packets it needs to satisfy all its current clients.

This component will terminate if a shutdownMicroprocess or
producerFinished message is sent to the \"control\" inbox. The message
will be forwarded on out of the \"signal\" outbox just before
termination.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Receiver](/Components/pydoc/Kamaelia.Device.DVB.Receiver.html){.reference}.[Receiver](/Components/pydoc/Kamaelia.Device.DVB.Receiver.Receiver.html){.reference}
===================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: Receiver {#symbol-Receiver}
----------------
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
