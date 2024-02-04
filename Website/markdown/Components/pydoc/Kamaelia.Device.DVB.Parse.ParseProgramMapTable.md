---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramMapTable
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramMapTable.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ParseProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramMapTable.ParseProgramMapTable.html){.reference}**
:::

-   [Parsing Program Map Tables in DVB streams](#500){.reference}
    -   [Example Usage](#501){.reference}
    -   [Behaviour](#502){.reference}
    -   [How does it work?](#503){.reference}
:::

::: {.section}
Parsing Program Map Tables in DVB streams {#500}
=========================================

ParseProgramMapTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs a dictionary containing the data in the
table.

The purpose of the PMT and details of the fields within in are defined
in the MPEG systems specification:

-   ISO/IEC 13818-1 (aka \"MPEG: Systems\") \"GENERIC CODING OF MOVING
    PICTURES AND ASSOCIATED AUDIO: SYSTEMS\" ISO / Motion Picture
    Experts Group

The possible \'descriptor\' fields that feature in the table are
explained in the DVB SI specification:

-   ETSI EN 300 468 \"Digital Video Broadcasting (DVB); Specification
    for Service Information (SI) in DVB systems\" ETSI / EBU (DVB group)

See
[Kamaelia.Support.DVB.Descriptors](/Components/pydoc/Kamaelia.Support.DVB.Descriptors.html){.reference}
for information on how they are parsed.

::: {.section}
[Example Usage]{#example-usage} {#501}
-------------------------------

A simple pipeline to receive, parse and display a particular Program Map
Table in a multiplex, carried in packets with packet id 4228:

``` {.literal-block}
FREQUENCY = 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

PMT_PID = 4228

Pipeline( DVB_Multiplex(FREQUENCY, [PMT_PID], feparams),
          DVB_Demuxer({ PMT_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseProgramMapTable(),
          PrettifyProgramMapTable(),
          ConsoleEchoer(),
        ).run()
```
:::

::: {.section}
[Behaviour]{#behaviour} {#502}
-----------------------

Send reconstructed PSI table \'sections\' to the \"inbox\" inbox. When
all sections of the table have arrived, ParseProgramMapTable will parse
the table and send it out of its \"outbox\" outbox.

If the table is unchanged since last time it was parsed, then it will
not be sent out. Parsed tables are only sent out when they are new or
have just changed.

The parsed table is sent out as a dictionary data structure, similar to
this (the \'streams\' list here is abridged for brevity):

``` {.literal-block}
{
    'table_id' : 2,
    'table_type' : 'PMT',
    'current'  : 1,
    'services' : {
        4228: { 'video_pid'   : 610,
                'audio_pid'   : 611,
                'descriptors' : [],
                'pcr_pid'     : 610,
                'streams'     : [
                    { 'pid'         : 610,
                      'type'        : 2,
                      'descriptors' : [
                          ( 82, { 'type' : 'stream_identifier', 'component_tag' : 1 } )
                      ]
                    },
                    { 'pid'         : 611,
                      'type'        : 3,
                      'descriptors' : [
                          ( 10, { 'type' : 'ISO_639', 'entries' : [ { 'audio_type': '', 'language_code': 'eng' } ] } ),
                          ( 82, { 'type' : 'stream_identifier', 'component_tag' : 2 } )
                      ]
                    },

                    .....

                    { 'pid'        : 1010,
                      'type'       : 11,
                      'descriptors': [
                          ( 82, { 'type' : 'stream_identifier', 'component_tag' : 112 } )
                      ]
                    }
                ]
            }
    }
}
```

This table contains information about one service (with service id
4228), and describes many streams in that service. ParseProgramMapTable
has identified that packets with packet id 610 and 611 probably contain
the primary video and audio making up this service.

This is part of an instantaneous snapshot of a PMT broadcast from
Crystal Palace MUX 1 (505.8MHz) in the UK on 20th Dec 2006.

If this data is sent on through a PrettifyProgramMapTable component,
then the equivalent output is a string containing the following (again,
abridged here for brevity):

``` {.literal-block}
PMT received:
    Table ID           : 2
    Table is valid for : CURRENT (valid)
    Services:
        Service id : 4228
        Program Clock Reference in PID : 610
        Service Descriptors:
            <<NONE>>
        Streams in service:
            Type : 2
                PID  : 610
                Stream Descriptors:
                    Descriptor 0x52 : stream_identifier
                        component_tag : 1
            Type : 3
                PID  : 611
                Stream Descriptors:
                    Descriptor 0xa : ISO_639
                        entries : [{'audio_type': '', 'language_code': 'eng'}]
                    Descriptor 0x52 : stream_identifier
                        component_tag : 2

            .....

            Type : 11
                PID  : 1010
                Stream Descriptors:
                    Descriptor 0x52 : stream_identifier
                        component_tag : 112
```

ParseProgramMapTable can collect the sections of, and then parse, both
\'current\' and \'next\' tables simultaneously.

See the \"MPEG Systems\" and \"DVB SI\" specifications for information
on the purposes of the descriptor fields that appear in various parts of
this table.

See
[Kamaelia.Support.DVB.Descriptors](/Components/pydoc/Kamaelia.Support.DVB.Descriptors.html){.reference}
for information on how each is parsed.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#503}
--------------------------------------

ParseProgramMapTable logs all the table sections it receives, until it
determines it has the complete set; then it parses them.

If the version number field in any table section changes, then the log
is cleared, and the component starts collecting the sections again from
scratch.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramMapTable.html){.reference}.[ParseProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramMapTable.ParseProgramMapTable.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ParseProgramMapTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ParseProgramMapTable}
------------------------------------------------------------------------------------------------------------

ParseProgramMapTable() -\> new ParseProgramMapTable component.

Send reconstructed PSI table sections to the \"inbox\" inbox. When a
complete table is assembled and parsed, the result is sent out of the
\"outbox\" outbox as a dictionary.

Doesn\'t emit anything again until the version number of the table
changes.

Outputs both \'current\' and \'next\' tables.

::: {.section}
### [Inboxes]{#symbol-ParseProgramMapTable.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : DVB PSI Packets from a single PID containing PMT table
    sections
:::

::: {.section}
### [Outboxes]{#symbol-ParseProgramMapTable.Outboxes}

-   **outbox** : Parsed PMT table (only when it changes)
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
#### [main(self)]{#symbol-ParseProgramMapTable.main}
:::

::: {.section}
#### [parseTable(self, table\_id, current\_next, sections)]{#symbol-ParseProgramMapTable.parseTable}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ParseProgramMapTable.shutdown}
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
