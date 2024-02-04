---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.html){.reference}
================================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.ReassemblePSITables.html){.reference}**
-   **component
    [ReassemblePSITablesService](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.ReassemblePSITablesService.html){.reference}**
:::

-   [Reassembly of DVB PSI Tables](#518){.reference}
    -   [Example Usage](#519){.reference}
    -   [ReassemblePSITables](#520){.reference}
        -   [Behaviour](#521){.reference}
    -   [ReassemblePSITablesService](#522){.reference}
        -   [Behaviour](#523){.reference}
        -   [How does it work?](#524){.reference}
:::

::: {.section}
Reassembly of DVB PSI Tables {#518}
============================

Components that take a stream of MPEG Transport stream packets
containing Programme Status Information (PSI) tables and reassembles the
table sections, ready for parsing of the data within them.

ReassemblePSITables can do this for a stream of packets containing a
single table.

ReassemblePSITablesService provides a full service capable of
reassembling multiple tables from a multiplexed stream of packets, and
distributing them to subscribers.

::: {.section}
[Example Usage]{#example-usage} {#519}
-------------------------------

A simple pipeline to receive, parse and display the Event Information
Table in a multiplex:

``` {.literal-block}
FREQUENCY = 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

EIT_PID = 0x12

Pipeline( OneShot( msg=["ADD", [0x2000] ] ),    # take all packets of all PIDs
          Tuner(FREQUENCY, feparams),
          DVB_SoftDemuxer( { EIT_PID : ["outbox"] } ),
          ReassemblePSITables(),
          ParseEventInformationTable(),
          PrettifyEventInformationTable(),
          ConsoleEchoer(),
        ).run()
```

Set up a dvb tuner and demultiplexer as a service; then set up a PSI
tables service (that subscribes to the demuxer); then finally subscribe
to the PSI tables service to get Event Information Tables and parse and
display them:

``` {.literal-block}
RegisterService( Receiver( FREQUENCY, FE_PARAMS, 0 ),
                {"DEMUXER":"inbox"},
            ).activate()

RegisterService(         Graphline( PSI     = ReassemblePSITablesService(),
               DEMUXER = ToService("DEMUXER"),
               linkages = {
                   ("PSI", "pid_request") : ("DEMUXER", "inbox"),
                   ("",    "request")     : ("PSI",     "request"),
               }
             ),
    {"PSI_Tables":"request"}
).activate()

Pipeline( Subscribe("PSI", [EIT_PID]),
          ParseEventInformationTable(),
          PrettifyEventInformationTable(),
          ConsoleEchoer(),
        ).run()
```

In the above example, the final pipeline subscribes to the \'PSI\'
service, requesting the PSI tables in MPEG Transport Stream packets with
packet id 0x12.

The ReassemblePSITablesService service uses a ToService component to
send its own requests to the \'DEMUXER\' service to ask for MPEG
Transport Stream packets with the packet ids it needs.
:::

::: {.section}
[ReassemblePSITables]{#reassemblepsitables} {#520}
-------------------------------------------

ReassemblePSITables reassembles one PSI table at a time from a stream of
MPEG transport stream packets containing that table.

::: {.section}
### [Behaviour]{#behaviour} {#521}

Send individual MPEG Transport Stream packets to the \"inbox\" inbox
containing fragments of a particular PSI table.

ReassemblePSITables will reconstruct the table sections. As soon as a
section is complete, it will be sent, as a raw binary string, out of the
\"outbox\" outbox. The process repeats indefinitely.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::
:::

::: {.section}
[ReassemblePSITablesService]{#reassemblepsitablesservice} {#522}
---------------------------------------------------------

ReassemblePSITablesService provides a full service capable of
reassembling multiple tables from a multiplexed stream of packets, and
distributing them to subscribers.

::: {.section}
### [Behaviour]{#id1} {#523}

ReassemblePSITablesServices takes individual MPEG Transport Stream
packets sent to its \"inbox\" inbox and reconstructs table sections,
distributing them to clients/subscribers that have requested them.

To be a client you can wrap ReassemblePSITablesService into a named
service by using a Kamaelia.Experiment.Services.RegisterService
component, and then subscribe to it using a
Kamaelia.Experiment.Services.SubscribeTo component.

Alternatively, send a \'ADD\' or \'REMOVE\' message to its \"request\"
inbox, requesting to be sent (or no longer be sent) tables from packets
of particular PIDs, and specifying the inbox to which you want the
packets to be sent. The format of these requests is:

``` {.literal-block}
("ADD",    [pid, pid, ...], (dest_component, dest_inboxname))
("REMOVE", [pid, pid, ...], (dest_component, dest_inboxname))
```

ReassemblePSITablesService will automatically do the wiring or unwiring
needed to ensure the packets you have requested get sent to the inbox
you specified.

Send an \'ADD\' request, and you will immediately start receiving tables
in those PIDs. Send a \'REMOVE\' request and you will shortly no longer
receive tables in the PIDs you specify. Note that you may still receive
some tables after your \'REMOVE\' request.

ReassemblePSITablesService will also send its own requests (in the same
format) out of its \"pid\_request\" outbox. You can wire this up to the
source of transport stream packets, so that ReassemblePSITablesService
can tell that source what PIDs it needs. Alternatively, simply ensure
that your source is already sending all the PIDs your
ReassemblePSITablesService component will need.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#524}

ReassemblePSITablesService creates an outbox for each subscriber
destination, and wires from it to the destination.

For each PID that needs to be processed, a ReassemblePSITables component
is created to handle reconstruction of that particular table.Transport
Stream packets arriving at the \"inbox\" inbox are sent to the relevant
ReassemblePSITables component for table reconstruction. Reconstructed
tables coming back from each ReassemblePSITables component are forwarded
to all destinations that have subscribed to it.

When ReassemblePSITablesServices starts or stops using packets of a
given PID, an \'add\' or \'remove\' message is also sent out of the
\"pid\_request\" outbox:

``` {.literal-block}
("ADD",    [pid], (self, "inbox"))
("REMOVE", [pid], (self, "inbox"))
```

This can be wired up to the source of transport stream packets, so that
ReassemblePSITablesService can tell that source what PIDs it needs.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.html){.reference}.[ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.ReassemblePSITables.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ReassemblePSITables([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ReassemblePSITables}
-----------------------------------------------------------------------------------------------------------

Takes DVB Transport stream packets for a given PID and reconstructs the
PSI packets from within the stream.

Will only handle stream from a single PID.

::: {.section}
### [Inboxes]{#symbol-ReassemblePSITables.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-ReassemblePSITables.Outboxes}
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
#### [main(self)]{#symbol-ReassemblePSITables.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ReassemblePSITables.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.html){.reference}.[ReassemblePSITablesService](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.ReassemblePSITablesService.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ReassemblePSITablesService([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-ReassemblePSITablesService}
----------------------------------------------------------------------------------------------------------------------------------------------------------------------

ReassemblePSITablesService() -\> new ReassemblePSITablesService
component.

Subscribe to PSI packets by sending (\"ADD\", (component,inbox),
\[PIDs\] ) to \"request\" Unsubscribe by sending (\"REMOVE\",
(component,inbox), \[PIDs\] ) to \"request\"

::: {.section}
### [Inboxes]{#symbol-ReassemblePSITablesService.Inboxes}

-   **control** : Shutdown signalling
-   **request** : Place for subscribing/unsubscribing from different PSI
    packet streams
-   **inbox** : Incoming DVB TS packets
:::

::: {.section}
### [Outboxes]{#symbol-ReassemblePSITablesService.Outboxes}

-   **outbox** : NOT USED
-   **signal** : Shutdown signalling
-   **pid\_request** : For issuing requests for PIDs
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
#### [\_\_init\_\_(self)]{#symbol-ReassemblePSITablesService.__init__}
:::

::: {.section}
#### [handleSubscribeUnsubscribe(self, msg)]{#symbol-ReassemblePSITablesService.handleSubscribeUnsubscribe}
:::

::: {.section}
#### [main(self)]{#symbol-ReassemblePSITablesService.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ReassemblePSITablesService.shutdown}
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
