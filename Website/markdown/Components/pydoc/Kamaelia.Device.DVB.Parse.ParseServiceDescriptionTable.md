---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable.html){.reference}**
-   **prefab
    [ParseServiceDescriptionTable\_ActualAndOtherTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_ActualAndOtherTS.html){.reference}**
-   **prefab
    [ParseServiceDescriptionTable\_ActualTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_ActualTS.html){.reference}**
-   **prefab
    [ParseServiceDescriptionTable\_OtherTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_OtherTS.html){.reference}**
-   **component
    [SDT\_to\_SimpleServiceList](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.SDT_to_SimpleServiceList.html){.reference}**
:::

-   [Parsing Service Description Tables in DVB
    streams](#508){.reference}
    -   [Example Usage](#509){.reference}
    -   [ParseServiceDescriptionTable](#510){.reference}
        -   [Behaviour](#511){.reference}
        -   [How does it work?](#512){.reference}
    -   [SDT\_to\_SimpleServiceList](#513){.reference}
        -   [Behaviour](#514){.reference}
:::

::: {.section}
Parsing Service Description Tables in DVB streams {#508}
=================================================

ParseServiceDescriptionTable parses a reconstructed PSI table from a DVB
MPEG Transport Stream, and outputs a dictionary containing the data in
the table.

The purpose of the SDT and details of the fields within in are defined
in the DVB SI specification, including the possible \'descriptor\'
fields that feature in the table:

-   ETSI EN 300 468 \"Digital Video Broadcasting (DVB); Specification
    for Service Information (SI) in DVB systems\" ETSI / EBU (DVB group)

See
[Kamaelia.Support.DVB.Descriptors](/Components/pydoc/Kamaelia.Support.DVB.Descriptors.html){.reference}
for information on how they are parsed.

::: {.section}
[Example Usage]{#example-usage} {#509}
-------------------------------

A simple pipeline to receive, parse and display the Service Description
Table applying to the transport stream (MUX) being received (\"actual
TS\"):

``` {.literal-block}
FREQUENCY = 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

SID_Actual_PID = 0x11

Pipeline( DVB_Multiplex(FREQUENCY, [SID_Actual_PID], feparams),
          DVB_Demuxer({ SID_Actual_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseServiceDescriptionTable_ActualTS(),
          PrettifyServiceDescriptionTable(),
          ConsoleEchoer(),
        ).run()
```

A simple pipeline to receive and parse the Service Description Table
then convert it to a simple list mapping service names to service ids:

``` {.literal-block}
Pipeline( DVB_Multiplex(FREQUENCY, [SID_Actual_PID], feparams),
          DVB_Demuxer({ SID_Actual_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseServiceDescriptionTable_ActualTS(),
          SDT_to_SimpleServiceList(),
          ConsoleEchoer(),
        ).run()
```
:::

::: {.section}
[ParseServiceDescriptionTable]{#parseservicedescriptiontable} {#510}
-------------------------------------------------------------

::: {.section}
### [Behaviour]{#behaviour} {#511}

At initialisation, specify whether you want
ParseServiceDescriptionTables to parse \'actual\' or \'other\' tables
(or both). \'Actual\' tables describe services within the actual
transport stream the table is it. \'Other\' tables describe services
carried in other transport streams - ie. broadcast in a different MUX in
the same network. For example:

``` {.literal-block}
ParseServiceDescriptionTable(acceptTables = {0x42:"ACTUAL",0x46:"OTHER"})
```

There are shorthands available for the various combinations:

``` {.literal-block}
ParseServiceDescriptionTable_ActualTS()
ParseServiceDescriptionTable_OtherTS()
ParseServiceDescriptionTable_ActualAndOtherTS():
```

Send reconstructed PSI table \'sections\' to the \"inbox\" inbox. When
all sections of the table have arrived, ParseServiceDescriptionTable
will parse the table and send it out of its \"outbox\" outbox.

If the table is unchanged since last time it was parsed, then it will
not be sent out. Parsed tables are only sent out when they are new or
have just changed.

The parsed table is sent out as a dictionary data structure, similar to
this (the \'streams\' list here is abridged for brevity):

``` {.literal-block}
{
    'actual_other'        : 'ACTUAL',
    'table_type'          : 'SDT',
    'current'             : 1,
    'original_network_id' : 9018,
    'table_id'            : 66,
    'services': {
        4228: { 'running_status'       : 4,
                'free_CA_mode'         : 0,
                'eit_present_following': 1,
                'eit_schedule'         : 2,
                'descriptors': [
                    ( 72, { 'type': 'service',
                            'service_name': 'BBC TWO',
                            'service_type': 'digital television service',
                            'service_provider_name': 'BBC'
                          } ),
                    (115, { 'type': 'UNKNOWN',
                            'contents': 'fp.bbc.co.uk'
                          } )
                ] },
        4164: { 'running_status'       : 4,
                'free_CA_mode'         : 0,
                'eit_present_following': 1,
                'eit_schedule'         : 2,
                'descriptors': [
                    ( 72, { 'type': 'service',
                            'service_name': 'BBC ONE',
                            'service_type': 'digital television service',
                            'service_provider_name': 'BBC'
                          } ),
                    (115, { 'type': 'UNKNOWN',
                            'contents': 'fp.bbc.co.uk'
                          } )
                ] },

        .....

        4671: { 'running_status': 4,
                'free_CA_mode'         : 0,
                'eit_present_following': 1,
                'eit_schedule'         : 2,
                'descriptors': [
                    ( 72, { 'type': 'service',
                            'service_name': 'CBBC Channel',
                            'service_type': 'digital television service',
                            'service_provider_name': 'BBC'
                          } ),
                    (115, { 'type': 'UNKNOWN',
                            'contents': 'fp.bbc.co.uk'
                          } )
                ] }
        },
    'transport_stream_id': 4100
}
```

This table contains information about the services within the transport
stream. It lists the services (channels) including their names. types,
and the fact that there is now & next data (eit\_present\_following) and
Electronic Programme Guide (eit\_schedule) data available for each of
them.

This is part of an instantaneous snapshot of the SDT broadcast from
Crystal Palace MUX 1 (505.8MHz) in the UK on 21th Dec 2006.

If this data is sent on through a PrettifyServiceDescriptionTable
component, then the equivalent output is a string containing the
following (again, abridged here for brevity):

``` {.literal-block}
Table ID           : 66
Table is valid for : CURRENT (valid)
Actual or Other n/w: ACTUAL
Transport stream id: 4100
Original network id: 9018
Services:
    Service id : 4228
        EIT present_following? : YES
        EIT schedule?          : YES
        Running status         : 4 (RUNNING)
        Scrambled?             : NO
        Service descriptors:
            Descriptor 0x48 : service
                service_name : 'BBC TWO'
                service_provider_name : 'BBC'
                service_type : 'digital television service'
            Descriptor 0x73 : UNKNOWN
                contents : 'fp.bbc.co.uk'
    Service id : 4164
        EIT present_following? : YES
        EIT schedule?          : YES
        Running status         : 4 (RUNNING)
        Scrambled?             : NO
        Service descriptors:
            Descriptor 0x48 : service
                service_name : 'BBC ONE'
                service_provider_name : 'BBC'
                service_type : 'digital television service'
            Descriptor 0x73 : UNKNOWN
                contents : 'fp.bbc.co.uk'

    .....

    Service id : 4671
        EIT present_following? : YES
        EIT schedule?          : YES
        Running status         : 4 (RUNNING)
        Scrambled?             : NO
        Service descriptors:
            Descriptor 0x48 : service
                service_name : 'CBBC Channel'
                service_provider_name : 'BBC'
                service_type : 'digital television service'
            Descriptor 0x73 : UNKNOWN
                contents : 'fp.bbc.co.uk'
```

ParseServiceDescriptionTable can collect the sections of, and then
parse, both \'current\' and \'next\' tables simultaneously.

See the \"DVB SI\" specifications for information on the purposes of the
descriptor fields that appear in various parts of this table.

See
[Kamaelia.Support.DVB.Descriptors](/Components/pydoc/Kamaelia.Support.DVB.Descriptors.html){.reference}
for information on how each is parsed.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#512}

ParseServiceDescriptionTable logs all the table sections it receives,
until it determines it has the complete set; then it parses them.

If the version number field in any table section changes, then the log
is cleared, and the component starts collecting the sections again from
scratch.
:::
:::

::: {.section}
[SDT\_to\_SimpleServiceList]{#sdt-to-simpleservicelist} {#513}
-------------------------------------------------------

::: {.section}
### [Behaviour]{#id1} {#514}

Send parsed service description tables to this component\'s \"inbox\"
inbox and a dictionary mapping service names to service ids will be sent
out the \"outbox\" outbox. For example:

``` {.literal-block}
{ 'BBCi'        : 4479,
  'BBC ONE'     : 4164,
  'BBC TWO'     : 4228,
  'CBBC Channel': 4671,
  'BBC NEWS 24' : 4415,
  'BBC THREE'   : 4351
}
```

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.html){.reference}.[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable.html){.reference}
=========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ParseServiceDescriptionTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ParseServiceDescriptionTable}
--------------------------------------------------------------------------------------------------------------------

ParseServiceDescriptionTable(\[acceptTables\]) -\> new
ParseServiceDescriptionTable component.

Send reconstructed PSI table sections to the \"inbox\" inbox. When a
complete table is assembled and parsed, the result is sent out of the
\"outbox\" outbox as a dictionary.

Doesn\'t emit anything again until the version number of the table
changes.

Keyword arguments:

``` {.literal-block}
- acceptTables  - dict of (table_id,string_description) mappings for tables to be accepted (default={0x42:"ACTUAL",0x46:"OTHER"})
```

::: {.section}
### [Inboxes]{#symbol-ParseServiceDescriptionTable.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : DVB PSI Packets from a single PID containing SDT table
    sections
:::

::: {.section}
### [Outboxes]{#symbol-ParseServiceDescriptionTable.Outboxes}

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
#### [\_\_init\_\_(self\[, acceptTables\])]{#symbol-ParseServiceDescriptionTable.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-ParseServiceDescriptionTable.main}
:::

::: {.section}
#### [parseTable(self, index, sections)]{#symbol-ParseServiceDescriptionTable.parseTable}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ParseServiceDescriptionTable.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.html){.reference}.[ParseServiceDescriptionTable\_ActualAndOtherTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_ActualAndOtherTS.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: ParseServiceDescriptionTable\_ActualAndOtherTS {#symbol-ParseServiceDescriptionTable_ActualAndOtherTS}
------------------------------------------------------

ParseServiceDescriptionTable\_ActualAndOtherTS() -\> new
ParseServiceDescriptionTable component.

Instantiates a ParseServiceDescriptionTable component configured to
parse both \'ACTUAL\' and \'OTHER TS\' tables (table ids 0x42 and 0x46)
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.html){.reference}.[ParseServiceDescriptionTable\_ActualTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_ActualTS.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: ParseServiceDescriptionTable\_ActualTS {#symbol-ParseServiceDescriptionTable_ActualTS}
----------------------------------------------

ParseServiceDescriptionTable\_ActualTS() -\> new
ParseServiceDescriptionTable component.

Instantiates a ParseServiceDescriptionTable component configured to
parse \'ACTUAL TS\' tables only (table id 0x42)
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.html){.reference}.[ParseServiceDescriptionTable\_OtherTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_OtherTS.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: ParseServiceDescriptionTable\_OtherTS {#symbol-ParseServiceDescriptionTable_OtherTS}
---------------------------------------------

ParseServiceDescriptionTable\_OtherTS() -\> new
ParseServiceDescriptionTable component.

Instantiates a ParseServiceDescriptionTable component configured to
parse \'OTHER TS\' tables only (table id 0x46)
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.html){.reference}.[SDT\_to\_SimpleServiceList](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.SDT_to_SimpleServiceList.html){.reference}
===================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SDT\_to\_SimpleServiceList([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SDT_to_SimpleServiceList}
------------------------------------------------------------------------------------------------------------------

SDT\_to\_SimpleServiceList() -\> new SDT\_to\_SimpleServiceList
component.

Converts parsed Service Description Tables to a simplified list of
services.

::: {.section}
### [Inboxes]{#symbol-SDT_to_SimpleServiceList.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SDT_to_SimpleServiceList.Outboxes}
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
#### [main(self)]{#symbol-SDT_to_SimpleServiceList.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-SDT_to_SimpleServiceList.shutdown}
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
