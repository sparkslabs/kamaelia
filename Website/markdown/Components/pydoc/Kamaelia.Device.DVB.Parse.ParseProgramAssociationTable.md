---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramAssociationTable
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramAssociationTable.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ParseProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramAssociationTable.ParseProgramAssociationTable.html){.reference}**
:::

-   [Parsing Program Association Tables in DVB
    streams](#504){.reference}
    -   [Example Usage](#505){.reference}
    -   [Behaviour](#506){.reference}
    -   [How does it work?](#507){.reference}
:::

::: {.section}
Parsing Program Association Tables in DVB streams {#504}
=================================================

ParseProgramAssociationTable parses a reconstructed PSI table from a DVB
MPEG Transport Stream, and outputs a dictionary containing the data in
the table.

The purpose of the PAT and details of the fields within in are defined
in the MPEG systems specification:

-   ISO/IEC 13818-1 (aka \"MPEG: Systems\") \"GENERIC CODING OF MOVING
    PICTURES AND ASSOCIATED AUDIO: SYSTEMS\" ISO / Motion Picture
    Experts Group

::: {.section}
[Example Usage]{#example-usage} {#505}
-------------------------------

A simple pipeline to receive, parse and display the Program Association
Table in a multiplex:

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
:::

::: {.section}
[Behaviour]{#behaviour} {#506}
-----------------------

Send reconstructed PSI table \'sections\' to the \"inbox\" inbox. When
all sections of the table have arrived, ParseProgramAssociationTable
will parse the table and send it out of its \"outbox\" outbox.

If the table is unchanged since last time it was parsed, then it will
not be sent out. Parsed tables are only sent out when they are new or
have just changed.

The parsed table is sent out as a dictionary data structure, like this:

``` {.literal-block}
{
    'table_id'         : 0
    'table_type'       : 'PAT',
    'current'          : 1,
    'NIT_PID'          : 16,
    'transport_streams': { 4100: { 4228: 4228,
                                   4351: 4351,
                                   4479: 4479,
                                   4164: 4164,
                                   4415: 4415,
                                   4671: 4671
                                 }
                         },
}
```

This is an instantaneous snapshot of the PAT for Crystal Palace MUX 1
transmission (505.8MHz) in the UK on 20th Dec 2006. If this data is sent
on through a PrettifyProgramAssociationTable component, then the
equivalent output is a string containing this:

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

ParseProgramAssociationTable can collect the sections of, and then
parse, both \'current\' and \'next\' tables simultaneously.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#507}
--------------------------------------

ParseProgramAssociationTable logs all the table sections it receives,
until it determines it has the complete set; then it parses them.

If the version number field in any table section changes, then the log
is cleared, and the component starts collecting the sections again from
scratch.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramAssociationTable.html){.reference}.[ParseProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramAssociationTable.ParseProgramAssociationTable.html){.reference}
=========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ParseProgramAssociationTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ParseProgramAssociationTable}
--------------------------------------------------------------------------------------------------------------------

ParseProgramAssociationTable() -\> new ParseProgramAssociationTable
component.

Send reconstructed PSI table sections to the \"inbox\" inbox. When a
complete table is assembled and parsed, the result is sent out of the
\"outbox\" outbox as a dictionary.

Doesn\'t emit anything again until the version number of the table
changes.

Outputs both \'current\' and \'next\' tables.

::: {.section}
### [Inboxes]{#symbol-ParseProgramAssociationTable.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : DVB PSI Packets containing PAT table sections
:::

::: {.section}
### [Outboxes]{#symbol-ParseProgramAssociationTable.Outboxes}

-   **outbox** : Parsed PAT table (only when it changes)
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
#### [main(self)]{#symbol-ParseProgramAssociationTable.main}
:::

::: {.section}
#### [parseTable(self, table\_id, current\_next, sections)]{#symbol-ParseProgramAssociationTable.parseTable}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ParseProgramAssociationTable.shutdown}
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
