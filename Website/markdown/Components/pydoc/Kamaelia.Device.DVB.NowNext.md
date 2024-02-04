---
pagename: Components/pydoc/Kamaelia.Device.DVB.NowNext
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[NowNext](/Components/pydoc/Kamaelia.Device.DVB.NowNext.html){.reference}
============================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [NowNextProgrammeJunctionDetect](/Components/pydoc/Kamaelia.Device.DVB.NowNext.NowNextProgrammeJunctionDetect.html){.reference}**
-   **component
    [NowNextServiceFilter](/Components/pydoc/Kamaelia.Device.DVB.NowNext.NowNextServiceFilter.html){.reference}**
:::

-   [Processing Simplified Now & Next Event
    Information](#468){.reference}
    -   [Example Usage](#469){.reference}
    -   [NowNextServiceFilter](#470){.reference}
        -   [Behaviour](#471){.reference}
    -   [NowNextProgrammeJunctionDetect](#472){.reference}
        -   [Behaviour](#473){.reference}
        -   [How does it work?](#474){.reference}
:::

::: {.section}
Processing Simplified Now & Next Event Information {#468}
==================================================

These components filter or process simplified events, derived from Event
Information Table data containing now and next information.

Convert a parsed EIT table to simplified individual events using the
Kamaelia.Devices.DVB.Parse.ParseEventInformationTable.SimplifyEIT
component.

NowNextServiceFilter selects information relating to only particular
services (channels) in the data.

NowNextProgrammeJunctionDetect detects the point at which one programme
ends and another begins - known as the \"programme junction\". It
distinguishes between programme junctions and ammendments to a
programme\'s details.

::: {.section}
[Example Usage]{#example-usage} {#469}
-------------------------------

Tuning to a particular broadcast multiplex and detecting when a new
programme starts on service 4164, outputting the information about the
new programme:

``` {.literal-block}
frequency = 505833330.0/1000000.0
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

EIT_PID = 0x12
BBC_ONE = 4164       # the 'service id' on this particular multiplex

Pipeline( DVB_Multiplex(505833330.0/1000000.0, [EIT_PID], feparams),
          DVB_Demuxer({ EIT_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseEventInformationTable_Subset(True,False,False,False), # now and next for this mux only
          SimplifyEIT(),
          NowNextProgrammeJunctionDetect(),
          NowNextServiceFilter(BBC_ONE),
          ConsoleEchoer(),
```

The above code receives the broadcast multiplex, reconstructs and parses
the Event Information Table in it, then simplifies it to a stream of
events. These events are then filtered and processed.
:::

::: {.section}
[NowNextServiceFilter]{#nownextservicefilter} {#470}
---------------------------------------------

NowNextServiceFilter selects information relating to only particular
services (channels) in the data.

::: {.section}
### [Behaviour]{#behaviour} {#471}

At initialisation, specify the service id\'s of the services to be
detected as arguments.

Send the parsed and simplified events to this component\'s \"inbox\"
inbox. Those which match the service id\'s specified at initialisation
will immediately be sent on out of the \"outbox\" outbox. Those which do
not match are discarded.

If a shutdownMicroprocess or producerFinished message is sent to this
component\'s \"control\" inbox, it will immediately be sent on out of
the \"signal\" outbox. The component will then immediately terminate.
:::
:::

::: {.section}
[NowNextProgrammeJunctionDetect]{#nownextprogrammejunctiondetect} {#472}
-----------------------------------------------------------------

NowNextProgrammeJunctionDetect detects the point at which one programme
ends and another begins - known as the \"programme junction\". It
distinguishes between programme junctions and ammendments to a
programme\'s details.

::: {.section}
### [Behaviour]{#id1} {#473}

Send the parsed and simplified events to this component\'s \"inbox\"
inbox. This component then distinguishes between ammendments to a
programme (such as (a change to to how long it is, or its description)
and actual programme junctions (the end of one programme and the start
of the next).

A single NowNextProgrammeJunctionDetect instance can handle the events
for an unlimited number of services concurrently.

When a programme junction is detected, the event describing the
programme that has just started is sent out of the \"outbox\" and
\"now\" outboxes. Any event describing the \'next\' programme that will
follow it is sent out the \"next\" outbox.

If the details of a programme have just been ammended (it is not a
junction), then the new event information is sent out of the
\"now\_update\" outbox if it relates to the current programme on air; or
the \"next\_update\" outbox if it relates to the programme that will
follow it.

NowNextProgrammeJunctionDetect only handles \'now\' and \'next\' events.
Events for schedule (electronic programme guide) details are ignored.

If a shutdownMicroprocess or producerFinished message is sent to this
component\'s \"control\" inbox, it will immediately be sent on out of
the \"signal\" outbox. The component will then immediately terminate.
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#474}

NowNextProgrammeJunction detect keeps a record of the ids of the \'now\'
and \'next\' events each service.

When an event is received, it is looked up in this table. If the event
id matches, then it is assumed to be an ammendment of details. If it
does not then it is assumed that a programme junction must be taking
place.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[NowNext](/Components/pydoc/Kamaelia.Device.DVB.NowNext.html){.reference}.[NowNextProgrammeJunctionDetect](/Components/pydoc/Kamaelia.Device.DVB.NowNext.NowNextProgrammeJunctionDetect.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class NowNextProgrammeJunctionDetect([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-NowNextProgrammeJunctionDetect}
----------------------------------------------------------------------------------------------------------------------

NowNextProgrammeJunctionDetect() -\> new NowNextJunctionDetect
component.

Takes simplified events derived from parsed Event Information Table data
and sorts them according to whether they simply ammend/correct details
or whether they represent the start of a new programme (a junction).

::: {.section}
### [Inboxes]{#symbol-NowNextProgrammeJunctionDetect.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-NowNextProgrammeJunctionDetect.Outboxes}

-   **signal** : Shutdown signalling
-   **next** : new NEXT events, at programme junctions only
-   **now\_update** : NOW events, when details change, but its still the
    same programme
-   **outbox** : new NOW events, at programme junctions only
-   **next\_update** : NEXT events, when details change, but its still
    the same programme
-   **now** : same as for \'outbox\' outbox
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
#### [main(self)]{#symbol-NowNextProgrammeJunctionDetect.main}

Main loop
:::

::: {.section}
#### [shutdown(self)]{#symbol-NowNextProgrammeJunctionDetect.shutdown}

Shutdown handling
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[NowNext](/Components/pydoc/Kamaelia.Device.DVB.NowNext.html){.reference}.[NowNextServiceFilter](/Components/pydoc/Kamaelia.Device.DVB.NowNext.NowNextServiceFilter.html){.reference}
========================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class NowNextServiceFilter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-NowNextServiceFilter}
------------------------------------------------------------------------------------------------------------

NowNextServiceFilter(\*services) -\> new NowNextServiceFilter component.

Filters simplified events from Event Information Tables, only letting
through those that match the service ids specified.

Argument list is a list of service id\'s to be let through by the
filter.

::: {.section}
### [Inboxes]{#symbol-NowNextServiceFilter.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-NowNextServiceFilter.Outboxes}
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
#### [\_\_init\_\_(self, \*services)]{#symbol-NowNextServiceFilter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-NowNextServiceFilter.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-NowNextServiceFilter.shutdown}

Shutdown handling.
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
