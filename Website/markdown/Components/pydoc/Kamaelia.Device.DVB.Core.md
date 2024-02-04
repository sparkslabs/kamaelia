---
pagename: Components/pydoc/Kamaelia.Device.DVB.Core
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Core](/Components/pydoc/Kamaelia.Device.DVB.Core.html){.reference}
======================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [DVB\_Demuxer](/Components/pydoc/Kamaelia.Device.DVB.Core.DVB_Demuxer.html){.reference}**
-   **component
    [DVB\_Multiplex](/Components/pydoc/Kamaelia.Device.DVB.Core.DVB_Multiplex.html){.reference}**
:::

-   [SimpleDVB-T (Digital Terrestrial TV) Tuner](#462){.reference}
    -   [Example Usage](#463){.reference}
    -   [How does it work?](#464){.reference}
-   [SimpleDVB-T (Digital Terrestrial TV) Demuxer](#465){.reference}
    -   [Example Usage](#466){.reference}
    -   [How does it work?](#467){.reference}
:::

::: {.section}
::: {.section}
[SimpleDVB-T (Digital Terrestrial TV) Tuner]{#simpledvb-t-digital-terrestrial-tv-tuner} {#462}
---------------------------------------------------------------------------------------

DVB\_Multiplex tunes to the specified DVB-T multiplex and outputs
received MPEG Transport Stream packets that have a PID in the list of
PIDs specified.

If you need to change which PIDs you receive at runtime, consider using
[Kamaelia.Device.DVB.Tuner](/Components/pydoc/Kamaelia.Device.DVB.Tuner.html){.reference}

::: {.section}
### [Example Usage]{#example-usage} {#463}

Receiving PIDs 600 and 601 from MUX 1 broadcast from Crystal Palace in
the UK (this should, effectively, receive the video and audio for the
channel \'BBC ONE\'):

``` {.literal-block}
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.File.Writing import SimpleFileWriter
import dvb3.frontend

feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

Pipeline( DVB_Multiplex(505.833330, [600,601], feparams),
          SimpleFileWriter("BBC ONE.ts"),
        ).run()
```

Receive and record the whole multiplex (all pids):

``` {.literal-block}
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.File.Writing import SimpleFileWriter
import dvb3.frontend

feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

Pipeline( DVB_Multiplex(505.833330, [0x2000], feparams),
          SimpleFileWriter("BBC ONE.ts"),
        ).run()
```
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#464}

DVB\_Multiplex tunes, using the specified tuning parameters to a DVB-T
transmitted multiplex.

It will output received transport stream packets out of its \"outbox\"
outbox for those packets with a PID in the list of PIDs specified at
initialization.

Most DVB tuner devices understand a special packet ID of 0x2000 to
request the entire transport stream of all packets with all IDs. Specify
a list containing only this PID to receive the whole transport stream.

This component will terminate if a shutdownMicroprocess or
producerFinished message is sent to the \"control\" inbox. The message
will be forwarded on out of the \"signal\" outbox just before
termination.
:::
:::

::: {.section}
[SimpleDVB-T (Digital Terrestrial TV) Demuxer]{#simpledvb-t-digital-terrestrial-tv-demuxer} {#465}
-------------------------------------------------------------------------------------------

DVB\_Demuxer take in MPEG transport stream packets and routes them to
different outboxes, as specified in a mapping table.

If you need to change which PIDs you receive at runtime, consider using
[Kamaelia.Device.DVB.DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.html){.reference}.

::: {.section}
### [Example Usage]{#id1} {#466}

Receiving PIDs 600 and 601 from MUX 1 broadcast from Crystal Palace in
the UK (this should, effectively, receive the video and audio for the
channel \'BBC ONE\') and write them to separate files, plus also to a
combined file. Plus also record PIDS 610 and 611 (audio and video for
\'BBC TWO\') to a fourth file:

``` {.literal-block}
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Device.DVB.Core import DVB_Multiplex
from Kamaelia.Device.DVB.Core import DVB_Demuxer
from Kamaelia.File.Writing import SimpleFileWriter
import dvb3.frontend

feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

Graphline(
    RECV   = DVB_Multiplex(505.833330, [600,601, 610,611], feparams),
    DEMUX  = DVB_Demuxer( { 600 : ["outbox","video"],
                            601 : ["outbox","audio"],
                            610 : ["two"],
                            611 : ["two"] } ),
    REC_A  = SimpleFileWriter("audio.ts"),
    REC_V  = SimpleFileWriter("video.ts"),
    REC_AV = SimpleFileWriter("audio_and_video.ts"),
    REC_2  = SimpleFileWriter("audio_and_video2.ts"),

    linkages = { ("RECV",  "outbox")  : ("DEMUX",  "inbox"),

                 ("DEMUX", "outbox") : ("REC_AV", "inbox"),
                 ("DEMUX", "audio")  : ("REC_A",  "inbox"),
                 ("DEMUX", "video")  : ("REC_V",  "inbox"),

                 ("DEMUX", "two")    : ("REC_2",  "inbox"),
               }
).run()
```
:::

::: {.section}
### [How does it work?]{#id2} {#467}

DVB\_Demuxer takes MPEG transport stream packets, sent to its \"inbox\"
inbox and determines the packet ID (PID) of each, then distributes them
to different outboxes according to a mapping dictionary specified at
intialization.

The dictionary maps individual PIDs to lists of outbox names (the
outboxes to which packets with that given PID should be sent), for
example:

``` {.literal-block}
{
  600 : ["outbox","video"],
  601 : ["outbox","audio"],
  610 : ["two"],
  611 : ["two"]
}
```

This example mapping specified that packets with 600 and 601 should be
sent to the \"outbox\" outbox. Packets with PID 600 should also be sent
to the \"video\" outbox and packets with PID 601 should also be sent to
the \"audio\" outbox. Finally, packets with PIDs 610 and 611 should b
sent to the \"two\" outbox.

The relevant outboxes are automatically created.

If a packet arrives with a PID not featured in the mapping table, that
packet will be discarded.

As in the above example, a packet with a given PID can be mapped to more
than one destination outbox. It will be sent to all outboxes to which it
is mapped.

Packets which have their \'error\' or \'scrambled\' flag bits set will
be discarded.

This component will terminate if a shutdownMicroprocess or
producerFinished message is sent to the \"control\" inbox. The message
will be forwarded on out of the \"signal\" outbox just before
termination.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Core](/Components/pydoc/Kamaelia.Device.DVB.Core.html){.reference}.[DVB\_Demuxer](/Components/pydoc/Kamaelia.Device.DVB.Core.DVB_Demuxer.html){.reference}
==============================================================================================================================================================================================================================================================================================================================================

::: {.section}
class DVB\_Demuxer([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-DVB_Demuxer}
--------------------------------------------------------------------------------------------------------------------------------------------------------

This demuxer expects to recieve the output from a DVB\_Multiplex
component on its primary inbox. It is also provided with a number of
pids. For each pid that it knows about, it forwards the data received on
that PID to an appropriate outbox. Data associated with unknown PIDs in
the datastream is thrown away.

The output here is still transport stream packets. Another layer is
required to decide what to do with these - to yank out the PES and ES
packets.

::: {.section}
### [Inboxes]{#symbol-DVB_Demuxer.Inboxes}

-   **control** : We will receive shutdown messages here
-   **inbox** : This is where we expect to recieve a transport stream
:::

::: {.section}
### [Outboxes]{#symbol-DVB_Demuxer.Outboxes}
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
#### [\_\_init\_\_(self, pidmap)]{#symbol-DVB_Demuxer.__init__}
:::

::: {.section}
#### [errorIndicatorSet(self, packet)]{#symbol-DVB_Demuxer.errorIndicatorSet}
:::

::: {.section}
#### [main(self)]{#symbol-DVB_Demuxer.main}
:::

::: {.section}
#### [scrambledPacket(self, packet)]{#symbol-DVB_Demuxer.scrambledPacket}
:::

::: {.section}
#### [shutdown(self)]{#symbol-DVB_Demuxer.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Core](/Components/pydoc/Kamaelia.Device.DVB.Core.html){.reference}.[DVB\_Multiplex](/Components/pydoc/Kamaelia.Device.DVB.Core.DVB_Multiplex.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class DVB\_Multiplex([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-DVB_Multiplex}
--------------------------------------------------------------------------------------------------------------------------------------

This is a DVB Multiplex Tuner.

This tunes the given DVB card to the given frequency. This then sets up
the dvr0 device node to recieve the data recieved on a number of PIDs.

A special case use of these is to tune to 2 specific PIDs - the audio
and video for a specific TV channel. If you pass just 2 PIDs then
you\'re tuning to a specific channel.

NOTE 1: This multiplex tuner deliberately does not know what frequency
the multiplex is on, and does not know what PIDs are inside that
multiplex. You are expected to find out this information independently.

NOTE 2: This means also that producing a mock for the next stages in
this system should be relatively simple - we run this code once and dump
to disk.

::: {.section}
### [Inboxes]{#symbol-DVB_Multiplex.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-DVB_Multiplex.Outboxes}
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
#### [\_\_init\_\_(self, freq, pids\[, feparams\]\[, card\])]{#symbol-DVB_Multiplex.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-DVB_Multiplex.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-DVB_Multiplex.shutdown}
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
