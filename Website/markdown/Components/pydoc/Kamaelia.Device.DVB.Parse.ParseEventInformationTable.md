---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.html){.reference}
==============================================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.ParseEventInformationTable.html){.reference}**
-   **prefab
    [ParseEventInformationTable\_Subset](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.ParseEventInformationTable_Subset.html){.reference}**
-   **component
    [SimplifyEIT](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.SimplifyEIT.html){.reference}**
:::

-   [Parsing Event Information Tables in DVB streams](#494){.reference}
    -   [Example Usage](#495){.reference}
    -   [ParseEventInformationTable /
        ParseEventInformationTable\_Subset](#496){.reference}
        -   [Behaviour](#497){.reference}
    -   [SimplifyEIT](#498){.reference}
        -   [Behaviour](#499){.reference}
:::

::: {.section}
Parsing Event Information Tables in DVB streams {#494}
===============================================

ParseEventInformationTable parses a reconstructed PSI table from a DVB
MPEG Transport Stream, and outputs a dictionary containing the data in
the table.

The Event Information Table carries data about the programmes being
broadcast both now (present-following data) and in the future (schedule
data) and is typically used to drive Electronic Progamme Guides,
scheduled recording and \"now and next\" information displays.

The purpose of the EIT and details of the fields within in are defined
in the DVB SI specification:

-   ETSI EN 300 468 \"Digital Video Broadcasting (DVB); Specification
    for Service Information (SI) in DVB systems\" ETSI / EBU (DVB group)

See
[Kamaelia.Support.DVB.Descriptors](/Components/pydoc/Kamaelia.Support.DVB.Descriptors.html){.reference}
for information on how they are parsed.

::: {.section}
[Example Usage]{#example-usage} {#495}
-------------------------------

A simple pipeline to receive, parse and display the \"now and next\"
information for programmes in the current multiplex, from the Event
Information Table:

``` {.literal-block}
FREQUENCY = 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

EIT_PID = 0x12

Pipeline( DVB_Multiplex(FREQUENCY, [NIT_PID], feparams),
          DVB_Demuxer({ NIT_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseEventInformationTable_Subset(actual_presentFollowing=True),
          PrettifyEventInformationTable(),
          ConsoleEchoer(),
        ).run()
```

A slight modification to the pipeline, to convert the parsed tables into
a stream of inidividual events:

``` {.literal-block}
Pipeline( DVB_Multiplex(FREQUENCY, [NIT_PID], feparams),
          DVB_Demuxer({ NIT_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseEventInformationTable_Subset(actual_presentFollowing=True),
          SimplifyEIT(),
          ConsoleEchoer(),
        ).run()
```
:::

::: {.section}
[ParseEventInformationTable / ParseEventInformationTable\_Subset]{#parseeventinformationtable-parseeventinformationtable-subset} {#496}
--------------------------------------------------------------------------------------------------------------------------------

::: {.section}
### [Behaviour]{#behaviour} {#497}

At initialisation, specify what sub tables you want
ParseEventInformationTable to process (others will be ignored). Event
information is grouped into sub tables according to where it is:

-   \'Actual\' data describes programmes broadcast in the same actual
    multiplex as this data
-   \'Other\' data describes programmes being broadcast in other
    multiplexes

\...and what timeframe it relates to:

-   \'present following\' data describes the now showing (present) and
    next (following) programme to be shown
-   \'schedule\' data describes programmes being shown later, typically
    over the next 7 or 8 days.

Initialise ParseEventInformationTable by providing a dictionary mapping
table ids, to be accepted, to (label, is-present-following-flag) pairs.
For example, to accept tables of present-following data for this and
other multiplexes:

``` {.literal-block}
ParseEventInformationTable(acceptTables = { 0x4e : ("ACTUAL", True),
                                            0x4f : ("OTHER", False),
                                          }
```

However it is much simpler to use the ParseEventInformationTable\_Subset
helper funciton to create it for you. For example, the same effect as
above can be achieved with:

``` {.literal-block}
ParseEventInformationTable_Subset( actual_presentFollowing = True,
                                   other_presentFollowing  = True,
                                   actual_schedule         = False,
                                   other_schedule          = False,
                                 )
```

Send reconstructed PSI table \'sections\' to the \"inbox\" inbox. When
all sections of the table have arrived, ParseNetworkInformationTable
will parse the table and send it out of its \"outbox\" outbox.

If the table is unchanged since last time it was parsed, then it will
not be sent out. Parsed tables are only sent out when they are new or
have just changed.

Note that an EIT table is likely to arrive, and be parsed in lots of
separate fragments. Because of the way the data format is defined, it is
impossible for ParseEventInformationTable to know for certain when it
has received everything!

The parsed table is sent out as a dictionary data structure, like this
(list of event descriptors abridged for brevity):

``` {.literal-block}
{
    'table_id'            : 78,
    'table_type'          : 'EIT',
    'current'             : 1,
    'actual_other'        : 'ACTUAL',
    'is_present_following': True,
    'transport_stream_id' : 4100,
    'original_network_id' : 9018,
    'events': [
        { 'event_id'      : 8735,
          'running_status': 1,
          'free_CA_mode'  : 0,
          'starttime'     : [2006, 12, 22, 11, 0, 0],
          'duration'      : (0, 30, 0),
          'service_id'    : 4164
          'descriptors': [
              (77, {'type': 'short_event', 'name': 'To Buy or Not to Buy', 'text': 'Series that gives buyers the chance to test-drive a property before they buy it. Sarah Walker and Simon Rimmer are in Birmingham, helping a pair of property professionals. [S]', 'language_code': 'eng'}),
              (80, {'type': 'component', 'stream_content': 1, 'component_type': 3, 'text': 'Video 1', 'component_tag': 1, 'content,type': ('video', '16:9 aspect ratio without pan vectors, 25 Hz'), 'language_code': '   '}),
              (80, {'type': 'component', 'stream_content': 2, 'component_type': 3, 'text': 'Audio 2', 'component_tag': 2, 'content,type': ('audio', 'stereo (2 channel)'), 'language_code': 'eng'}),
              (80, {'type': 'component', 'stream_content': 3, 'component_type': 16, 'text': 'Subtitling 5', 'component_tag': 5, 'content,type': ('DVB subtitles (normal)', 'with no monitor aspect ratio criticality'), 'language_code': '   '}),
              (80, {'type': 'component', 'stream_content': 4, 'component_type': 1, 'text': 'Data 6', 'component_tag': 6, 'content,type': (4, 1), 'language_code': '   '}),

              .....

              (84, {'type': 'content', 'contents': '  '})
          ],
        }
    ]
}
```

The above example is an event for the service BBC ONE, broadcast at
10:06 GMT on 22nd December 2006. It describes a \'present-following\'
event that doesn\'t start until 11:00 GMT. It is therefore describing
the \'next\' programme that will be on the channel/service.

If this data is sent on through a PrettifyEventInformationTable
component, then the equivalent output is a string containing this
(again, abridged for brevity):

``` {.literal-block}
EIT received:
    Table ID                      : 78
    Table is valid for            : CURRENT (valid)
    Actual or Other n/w           : ACTUAL
    Present-Following or Schedule : Present-Following
    Transport stream id           : 4100
    Original network id           : 9018
    Events:
        Service id : 4164
            Running status         : 1 (NOT RUNNING)
            Start datetime (UTC)   : 2006-12-22 11:00:00
            Duration               : 00:30:00 (hh:mm:ss)
            Scrambled?             : NO
            Event descriptors:
                Descriptor 0x4d : short_event
                    language_code : 'eng'
                    name : 'To Buy or Not to Buy'
                    text : 'Series that gives buyers the chance to test-drive a property before they buy it. Sarah Walker and Simon Rimmer are in Birmingham, helping a pair of property professionals. [S]'
                Descriptor 0x50 : component
                    component_tag : 1
                    component_type : 3
                    content,type : ('video', '16:9 aspect ratio without pan vectors, 25 Hz')
                    language_code : '   '
                    stream_content : 1
                    text : 'Video 1'
                Descriptor 0x50 : component
                    component_tag : 2
                    component_type : 3
                    content,type : ('audio', 'stereo (2 channel)')
                    language_code : 'eng'
                    stream_content : 2
                    text : 'Audio 2'
                Descriptor 0x50 : component
                    component_tag : 5
                    component_type : 16
                    content,type : ('DVB subtitles (normal)', 'with no monitor aspect ratio criticality')
                    language_code : '   '
                    stream_content : 3
                    text : 'Subtitling 5'
                Descriptor 0x50 : component
                    component_tag : 6
                    component_type : 1
                    content,type : (4, 1)
                    language_code : '   '
                    stream_content : 4
                    text : 'Data 6'

                .....

                Descriptor 0x54 : content
                    contents : '  '
```

ParseEventInformationTable can collect the sections of, and then parse
the various types of EIT table simultaneously.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::
:::

::: {.section}
[SimplifyEIT]{#simplifyeit} {#498}
---------------------------

::: {.section}
### [Behaviour]{#id1} {#499}

Send parsed event information data to the \"inbox\" inbox, and
individual events, in a simplified form, will be sent out the \"outbox\"
outbox one at a time. For example:

``` {.literal-block}
{
    'event_id'       : 8735,
    'when'           : 'NEXT',
    'startdate'      : [2006, 12, 22],
    'starttime'      : [11, 0, 0],
    'duration'       : (0, 30, 0),
    'service'        : 4164,
    'transportstream': 4100,
    'language_code'  : 'eng',
    'name'           : 'To Buy or Not to Buy',
    'description'    : 'Series that gives buyers the chance to test-drive a property before they buy it. Sarah Walker and Simon Rimmer are in Birmingham, helping a pair of property professionals. [S]'
}
```

The possible values of the \'when\' field are:

-   \"NOW\" \-- describes a programme that is happening NOW
-   \"NEXT\" \-- describes a programme that follows the one happening
    now
-   \"SCHEDULED\" \-- part of a schedule describing programmes happening
    over the next few days

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.html){.reference}.[ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.ParseEventInformationTable.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ParseEventInformationTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ParseEventInformationTable}
------------------------------------------------------------------------------------------------------------------

ParseEventInformationTable(\[acceptTables\]) -\> new
ParseEventInformationTable component.

Send reconstructed PSI table sections to the \"inbox\" inbox. When a
complete table is assembled and parsed, the result is sent out of the
\"outbox\" outbox as a dictionary.

Doesn\'t emit anything again until the version number of the table
changes.

Use ParseEventInformationTable\_Subset for simpler initialisation with
convenient presets.

Keyword arguments:

``` {.literal-block}
- acceptTables  - dict of (table_id,string_description) mappings for tables to be accepted (default={0x4e:("ACTUAL",True)})
```

::: {.section}
### [Inboxes]{#symbol-ParseEventInformationTable.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : DVB PSI Packets from a single PID containing EIT table
    sections
:::

::: {.section}
### [Outboxes]{#symbol-ParseEventInformationTable.Outboxes}

-   **outbox** : Parsed EIT table (only when it changes)
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
#### [\_\_init\_\_(self\[, acceptTables\])]{#symbol-ParseEventInformationTable.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-ParseEventInformationTable.main}
:::

::: {.section}
#### [parseTableSection(self, index, section)]{#symbol-ParseEventInformationTable.parseTableSection}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ParseEventInformationTable.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.html){.reference}.[ParseEventInformationTable\_Subset](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.ParseEventInformationTable_Subset.html){.reference}
==============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: ParseEventInformationTable\_Subset {#symbol-ParseEventInformationTable_Subset}
------------------------------------------

ParseEventInformationTable\_Subset(\[actual\_presentFollowing\]\[,other\_presentFollowing\]\[,actual\_schedule\]\[,other\_schedule\]
) -\> new ParseEventInformationTable component

Returns a ParseEventInformationTable component, configured to parse the
table types specified, and ignore all others.

Keyword arguments:

``` {.literal-block}
- actual_presentFollowing  -- If True, parse 'present-following' data for this multiplex (default=True)
- other_presentFollowing   -- If True, parse 'present-following' data for other multiplexes (default=False)
- actual_schedule          -- If True, parse 'schedule' data for this multiplex (default=False)
- other_schedule           -- If True, parse 'schedule' data for other multiplexes (default=False)
```
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.html){.reference}.[SimplifyEIT](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.SimplifyEIT.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SimplifyEIT([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SimplifyEIT}
---------------------------------------------------------------------------------------------------

SimplifyEIT() -\> new SimplifyEIT component.

Send parsed EIT messages to the \"inbox\" inbox, and individual,
simplified events will be sent out the \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-SimplifyEIT.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimplifyEIT.Outboxes}
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
#### [main(self)]{#symbol-SimplifyEIT.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-SimplifyEIT.shutdown}
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
