---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[PrettifyTables](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [PrettifyEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyEventInformationTable.html){.reference}**
-   **component
    [PrettifyNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyNetworkInformationTable.html){.reference}**
-   **component
    [PrettifyProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyProgramAssociationTable.html){.reference}**
-   **component
    [PrettifyProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyProgramMapTable.html){.reference}**
-   **component
    [PrettifyServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyServiceDescriptionTable.html){.reference}**
-   **component
    [PrettifyTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyTimeAndDateTable.html){.reference}**
-   **component
    [PrettifyTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyTimeOffsetTable.html){.reference}**
:::

-   [Pretty printing of parsed DVB PSI tables](#491){.reference}
    -   [Example Usage](#492){.reference}
    -   [Behaviour](#493){.reference}
:::

::: {.section}
Pretty printing of parsed DVB PSI tables {#491}
========================================

A selection of components for creating human readable strings of the
output of the various components in
[Kamaelia.Device.DVB.Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}
that parse data tables in DVB MPEG Transport Streams.

::: {.section}
[Example Usage]{#example-usage} {#492}
-------------------------------

Pretty printing of a Program Association Table (PAT):

``` {.literal-block}
FREQUENCY = 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

PAT_PID = 0x0

Pipeline( DVB_Multiplex(FREQUENCY, [PAT_PID], feparams),
          DVB_Demuxer({ PAT_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseProgramAssociationTable(),
          PrettifyProgramAssociationTable(),
          ConsoleEchoer(),
        ).run()
```

Example output:

``` {.literal-block}
PAT received:
    Table ID           : 0
    Table is valid for : CURRENT (valid)
    NIT is in PID      : 16
    For transport stream id : 4100
        For service 4228 : PMT is in PID 4228
        For service 4351 : PMT is in PID 4351
        For service 4479 : PMT is in PID 4479
        For service 4164 : PMT is in PID 4164
        For service 4415 : PMT is in PID 4415
        For service 4671 : PMT is in PID 4671
```

This data came from an instantaneous snapshot of the PAT for Crystal
Palace MUX 1 transmission (505.8MHz) in the UK on 20th Dec 2006.
:::

::: {.section}
[Behaviour]{#behaviour} {#493}
-----------------------

The components available are:

``` {.literal-block}
PrettifyProgramAssociationTable
PrettifyNetworkInformationTable
PrettifyProgramMapTable
PrettifyServiceDescriptionTable
PrettifyEventInformationTable
PrettifyTimeAndDateTable
PrettifyTimeOffsetTable
```

Send to the \"inbox\" inbox of any of these components the relevant
parsed table, and a string will be sent out the \"outbox\" outbox
containing a \'prettified\' human readable equivalent of the table data.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[PrettifyTables](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.html){.reference}.[PrettifyEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyEventInformationTable.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PrettifyEventInformationTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PrettifyEventInformationTable}
---------------------------------------------------------------------------------------------------------------------

PrettifyEventInformationTable() -\> new PrettifyEventInformationTable
component.

Send parsed event information tables to the \"inbox\" inbox and a human
readable string version will be sent out the \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-PrettifyEventInformationTable.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PrettifyEventInformationTable.Outboxes}
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
#### [main(self)]{#symbol-PrettifyEventInformationTable.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-PrettifyEventInformationTable.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[PrettifyTables](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.html){.reference}.[PrettifyNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyNetworkInformationTable.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PrettifyNetworkInformationTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PrettifyNetworkInformationTable}
-----------------------------------------------------------------------------------------------------------------------

PrettifyNetworkInformationTable() -\> new
PrettifyNetworkInformationTable component.

Send parsed network information tables to the \"inbox\" inbox and a
human readable string version will be sent out the \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-PrettifyNetworkInformationTable.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PrettifyNetworkInformationTable.Outboxes}
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
#### [main(self)]{#symbol-PrettifyNetworkInformationTable.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-PrettifyNetworkInformationTable.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[PrettifyTables](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.html){.reference}.[PrettifyProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyProgramAssociationTable.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PrettifyProgramAssociationTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PrettifyProgramAssociationTable}
-----------------------------------------------------------------------------------------------------------------------

PrettifyProgramAssociationTable() -\> new
PrettifyProgramAssociationTable component.

Send parsed program association tables to the \"inbox\" inbox and a
human readable string version will be sent out the \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-PrettifyProgramAssociationTable.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PrettifyProgramAssociationTable.Outboxes}
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
#### [main(self)]{#symbol-PrettifyProgramAssociationTable.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-PrettifyProgramAssociationTable.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[PrettifyTables](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.html){.reference}.[PrettifyProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyProgramMapTable.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PrettifyProgramMapTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PrettifyProgramMapTable}
---------------------------------------------------------------------------------------------------------------

PrettifyProgramMapTable() -\> new PrettifyProgramMapTable component.

Send parsed program map tables to the \"inbox\" inbox and a human
readable string version will be sent out the \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-PrettifyProgramMapTable.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PrettifyProgramMapTable.Outboxes}
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
#### [main(self)]{#symbol-PrettifyProgramMapTable.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-PrettifyProgramMapTable.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[PrettifyTables](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.html){.reference}.[PrettifyServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyServiceDescriptionTable.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PrettifyServiceDescriptionTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PrettifyServiceDescriptionTable}
-----------------------------------------------------------------------------------------------------------------------

PrettifyServiceDescriptionTable() -\> new
PrettifyServiceDescriptionTable component.

Send parsed service description tables to the \"inbox\" inbox and a
human readable string version will be sent out the \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-PrettifyServiceDescriptionTable.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PrettifyServiceDescriptionTable.Outboxes}
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
#### [main(self)]{#symbol-PrettifyServiceDescriptionTable.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-PrettifyServiceDescriptionTable.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[PrettifyTables](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.html){.reference}.[PrettifyTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyTimeAndDateTable.html){.reference}
=======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PrettifyTimeAndDateTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PrettifyTimeAndDateTable}
----------------------------------------------------------------------------------------------------------------

PrettifyTimeAndDateTable() -\> new PrettifyTimeAndDateTable component.

Send parsed time and date tables to the \"inbox\" inbox and a human
readable string version will be sent out the \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-PrettifyTimeAndDateTable.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PrettifyTimeAndDateTable.Outboxes}
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
#### [main(self)]{#symbol-PrettifyTimeAndDateTable.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-PrettifyTimeAndDateTable.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[PrettifyTables](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.html){.reference}.[PrettifyTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyTimeOffsetTable.html){.reference}
=====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PrettifyTimeOffsetTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PrettifyTimeOffsetTable}
---------------------------------------------------------------------------------------------------------------

PrettifyTimeOffsetTable() -\> new PrettifyTimeOffsetTable component.

Send parsed time offset tables to the \"inbox\" inbox and a human
readable string version will be sent out the \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-PrettifyTimeOffsetTable.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PrettifyTimeOffsetTable.Outboxes}
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
#### [main(self)]{#symbol-PrettifyTimeOffsetTable.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-PrettifyTimeOffsetTable.shutdown}
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
