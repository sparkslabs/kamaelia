---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable.html){.reference}**
-   **prefab
    [ParseNetworkInformationTable\_ActualAndOtherNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_ActualAndOtherNetwork.html){.reference}**
-   **prefab
    [ParseNetworkInformationTable\_ActualNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_ActualNetwork.html){.reference}**
-   **prefab
    [ParseNetworkInformationTable\_OtherNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_OtherNetwork.html){.reference}**
:::

-   [Parsing Network Information Tables in DVB
    streams](#487){.reference}
    -   [Example Usage](#488){.reference}
    -   [Behaviour](#489){.reference}
    -   [How does it work?](#490){.reference}
:::

::: {.section}
Parsing Network Information Tables in DVB streams {#487}
=================================================

ParseNetworkInformationTable parses a reconstructed PSI table from a DVB
MPEG Transport Stream, and outputs a dictionary containing the data in
the table.

The purpose of the NIT and details of the fields within in are defined
in the DVB SI specification:

-   ETSI EN 300 468 \"Digital Video Broadcasting (DVB); Specification
    for Service Information (SI) in DVB systems\" ETSI / EBU (DVB group)

See
[Kamaelia.Support.DVB.Descriptors](/Components/pydoc/Kamaelia.Support.DVB.Descriptors.html){.reference}
for information on how they are parsed.

::: {.section}
[Example Usage]{#example-usage} {#488}
-------------------------------

A simple pipeline to receive, parse and display the Network Information
Table in a multiplex:

``` {.literal-block}
FREQUENCY = 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

NIT_PID = 0x10

Pipeline( DVB_Multiplex(FREQUENCY, [NIT_PID], feparams),
          DVB_Demuxer({ NIT_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseNetworkInformationTable_ActualNetwork(),
          PrettifyNetworkInformationTable(),
          ConsoleEchoer(),
        ).run()
```
:::

::: {.section}
[Behaviour]{#behaviour} {#489}
-----------------------

At initialisation, specify whether you want ParseNetworkInformationTable
to parse \'actual\' or \'other\' tables (or both). \'Actual\' tables
describe transport streams/multiplexes within the same actual networks
that this table has been broadcast in. \'Other\' tables describe
transport streams/multiplexes being broadcast for other networks. For
example: \'freeview\' is a network in the UK that broadcasts several
multiplexes.

For example:

``` {.literal-block}
ParseNetworkInformationTable(acceptTables = {0x40:"ACTUAL",0x41:"OTHER"})
```

There are shorthands available for the various combinations:

``` {.literal-block}
ParseNetworkInformationTable_ActualNetwork()
ParseNetworkInformationTable_OtherNetwork()
ParseNetworkInformationTable_ActualAndOtherNetwork():
```

Send reconstructed PSI table \'sections\' to the \"inbox\" inbox. When
all sections of the table have arrived, ParseNetworkInformationTable
will parse the table and send it out of its \"outbox\" outbox.

If the table is unchanged since last time it was parsed, then it will
not be sent out. Parsed tables are only sent out when they are new or
have just changed.

The parsed table is sent out as a dictionary data structure, like this
(list of transport streams abridged for marginally better brevity):

``` {.literal-block}
{
    'table_id'    : 64,
    'table_type'  : 'NIT',
    'current'     : 1,
    'actual_other': 'ACTUAL',
    'network_id'  : 12293,
    'descriptors': [ (64, {'type': 'network_name', 'network_name': 'Crystal Palace'} ) ]
    'transport_streams': [
        { 'transport_stream_id': 4100,
          'descriptors': [
              ( 65, { 'type': 'service_list'
                      'services': [
                          {'service_type': ('digital television service',), 'service_id': 4164},
                          {'service_type': ('digital television service',), 'service_id': 4228},
                          {'service_type': ('digital television service',), 'service_id': 4351},
                          {'service_type': ('digital television service',), 'service_id': 4415},
                          {'service_type': ('digital television service',), 'service_id': 4479},
                          {'service_type': ('digital television service',), 'service_id': 4671}
                      ],
                    } ),
              ( 90, { 'other_frequencies': 1,
                      'params': { 'inversion': 2,
                                  'transmission_mode': 0,
                                  'hierarchy_information': 0,
                                  'code_rate_LP': 3,
                                  'guard_interval': 0,
                                  'bandwidth': 0,
                                  'frequency': 505833330,
                                  'constellation': 1,
                                  'code_rate_HP': 3
                                },
                      'type': 'terrestrial_delivery_system'
                    } ),
              ( 98, { 'type': 'frequency_list',
                      'frequencies': [697833330, 690166670, 554000000]
                    } ),
              ( 95, { 'type': 'private_data_specifier',
                      'private_data_specifier': 9018
                    } ),
              (131, { 'type': 'logical_channel',
                      'mappings': { 4228: 2, 4351: 7, 4479: 105, 4164: 1, 4415: 80, 4671: 70 }
                    } )
          ],
          'original_network_id': 9018
        },

       .....

        { 'transport_stream_id': 24576,
          'descriptors': [
              ( 65, { 'services': [
                          {'service_type': ('digital television service',), 'service_id': 25664},
                          {'service_type': ('digital television service',), 'service_id': 25728},
                          {'service_type': ('digital television service',), 'service_id': 25792},
                          {'service_type': ('digital television service',), 'service_id': 25856},
                          {'service_type': ('digital television service',), 'service_id': 25920},
                          {'service_type': ('digital radio sound service',), 'service_id': 26176},
                          {'service_type': ('digital radio sound service',), 'service_id': 26240},
                          {'service_type': ('digital radio sound service',), 'service_id': 26304},
                          {'service_type': ('digital radio sound service',), 'service_id': 26368},
                          {'service_type': ('digital radio sound service',), 'service_id': 26432},
                          {'service_type': ('digital radio sound service',), 'service_id': 26496},
                          {'service_type': ('digital radio sound service',), 'service_id': 26560},
                          {'service_type': ('digital radio sound service',), 'service_id': 26624},
                          {'service_type': ('digital radio sound service',), 'service_id': 26688},
                          {'service_type': ('data broadcast service',), 'service_id': 27008},
                          {'service_type': ('digital television service',), 'service_id': 27072},
                          {'service_type': ('digital television service',), 'service_id': 27136}
                      ],
                      'type': 'service_list'
                    } ),
              ( 90, { 'other_frequencies': 1,
                      'params': { 'inversion': 2,
                                  'transmission_mode': 0,
                                  'hierarchy_information': 0,
                                  'code_rate_LP': 3,
                                  'guard_interval': 0,
                                  'bandwidth': 0,
                                  'frequency': 537833330,
                                  'constellation': 1,
                                  'code_rate_HP': 3
                                },
                      'type': 'terrestrial_delivery_system'
                    } ),
              ( 98, { 'frequencies': [738000000, 826000000, 834000000],
                      'type': 'frequency_list'
                    } ),
              ( 95, { 'type': 'private_data_specifier',
                      'private_data_specifier': 9018
                    } ),
              (131, { 'type': 'logical_channel',
                      'mappings': { 25664: 18,  25728: 21,  26496: 710, 26432: 717,
                                    26560: 711, 26624: 715, 26688: 716, 25792: 19,
                                    25856: 20,  25920: 22,  27008: 300, 27072: 31,
                                    27136: 29,  26176: 713, 26240: 712, 26304: 722,
                                    26368: 718
                                  }
                    } )
          ],
          'original_network_id': 9018
        }
      ],
}
```

This is an instantaneous snapshot of the NIT for Crystal Palace MUX 1
transmission (505.8MHz) in the UK on 21th Dec 2006. It describes the
each of the transport streams being broadcast, including how to tune to
them (frequency and other parameters) and an overview of the services in
each. It also describes the mapping of channel numbers on the user\'s
remote control, to service ids.

If this data is sent on through a PrettifyNetworkInformationTable
component, then the equivalent output is a string containing this
(again, abridged for brevity):

``` {.literal-block}
NIT received:
    Table ID           : 64
    Table is valid for : CURRENT (valid)
    Actual or Other n/w: ACTUAL
    Network ID         : 12293
    Network descriptors:
    Network Descriptors:
        Descriptor 0x40 : network_name
            network_name : 'Crystal Palace'
    Transport Stream:
        transport stream id : 4100
        original network id : 9018
        Transport Stream Descriptors:
            Descriptor 0x41 : service_list
                services : [   {'service_type': ('digital television service',), 'service_id': 4164},
                               {'service_type': ('digital television service',), 'service_id': 4228},
                               {'service_type': ('digital television service',), 'service_id': 4351},
                               {'service_type': ('digital television service',), 'service_id': 4415},
                               {'service_type': ('digital television service',), 'service_id': 4479},
                               {'service_type': ('digital television service',), 'service_id': 4671}]
            Descriptor 0x5a : terrestrial_delivery_system
                other_frequencies : 1
                params : {   'bandwidth': 0,
                             'code_rate_HP': 3,
                             'code_rate_LP': 3,
                             'constellation': 1,
                             'frequency': 505833330,
                             'guard_interval': 0,
                             'hierarchy_information': 0,
                             'inversion': 2,
                             'transmission_mode': 0}
            Descriptor 0x62 : frequency_list
                frequencies : [697833330, 690166670, 554000000]
            Descriptor 0x5f : private_data_specifier
                private_data_specifier : 9018
            Descriptor 0x83 : logical_channel
                mappings : {4228: 2, 4351: 7, 4479: 105, 4164: 1, 4415: 80, 4671: 70}

    .....

    Transport Stream:
        transport stream id : 24576
        original network id : 9018
        Transport Stream Descriptors:
            Descriptor 0x41 : service_list
                services : [   {'service_type': ('digital television service',), 'service_id': 25664},
                               {'service_type': ('digital television service',), 'service_id': 25728},
                               {'service_type': ('digital television service',), 'service_id': 25792},
                               {'service_type': ('digital television service',), 'service_id': 25856},
                               {'service_type': ('digital television service',), 'service_id': 25920},
                               {'service_type': ('digital radio sound service',), 'service_id': 26176},
                               {'service_type': ('digital radio sound service',), 'service_id': 26240},
                               {'service_type': ('digital radio sound service',), 'service_id': 26304},
                               {'service_type': ('digital radio sound service',), 'service_id': 26368},
                               {'service_type': ('digital radio sound service',), 'service_id': 26432},
                               {'service_type': ('digital radio sound service',), 'service_id': 26496},
                               {'service_type': ('digital radio sound service',), 'service_id': 26560},
                               {'service_type': ('digital radio sound service',), 'service_id': 26624},
                               {'service_type': ('digital radio sound service',), 'service_id': 26688},
                               {'service_type': ('data broadcast service',), 'service_id': 27008},
                               {'service_type': ('digital television service',), 'service_id': 27072},
                               {'service_type': ('digital television service',), 'service_id': 27136}]
            Descriptor 0x5a : terrestrial_delivery_system
                other_frequencies : 1
                params : {   'bandwidth': 0,
                             'code_rate_HP': 3,
                             'code_rate_LP': 3,
                             'constellation': 1,
                             'frequency': 537833330,
                             'guard_interval': 0,
                             'hierarchy_information': 0,
                             'inversion': 2,
                             'transmission_mode': 0}
            Descriptor 0x62 : frequency_list
                frequencies : [738000000, 826000000, 834000000]
            Descriptor 0x5f : private_data_specifier
                private_data_specifier : 9018
            Descriptor 0x83 : logical_channel
                mappings : {   25664: 18,
                               25728: 21,
                               25792: 19,
                               25856: 20,
                               25920: 22,
                               26176: 713,
                               26240: 712,
                               26304: 722,
                               26368: 718,
                               26432: 717,
                               26496: 710,
                               26560: 711,
                               26624: 715,
                               26688: 716,
                               27008: 300,
                               27072: 31,
                               27136: 29}
```

ParseNetworkInformationTable can collect the sections of, and then
parse, both \'current\' and \'next\' tables simultaneously.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#490}
--------------------------------------

ParseNetworkInformationTable logs all the table sections it receives,
until it determines it has the complete set; then it parses them.

If the version number field in any table section changes, then the log
is cleared, and the component starts collecting the sections again from
scratch.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.html){.reference}.[ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable.html){.reference}
=========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ParseNetworkInformationTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ParseNetworkInformationTable}
--------------------------------------------------------------------------------------------------------------------

ParseNetworkInformationTable(\[acceptTables\]) -\> new
ParseNetworkInformationTable component.

Send reconstructed PSI table sections to the \"inbox\" inbox. When a
complete table is assembled and parsed, the result is sent out of the
\"outbox\" outbox as a dictionary.

Doesn\'t emit anything again until the version number of the table
changes.

Keyword arguments:

``` {.literal-block}
- acceptTables  - dict of (table_id,string_description) mappings for tables to be accepted (default={0x40:"ACTUAL",0x41:"OTHER"})
```

::: {.section}
### [Inboxes]{#symbol-ParseNetworkInformationTable.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : DVB PSI Packets from a single PID containing NIT table
    sections
:::

::: {.section}
### [Outboxes]{#symbol-ParseNetworkInformationTable.Outboxes}

-   **outbox** : Parsed NIT (only when it changes)
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
#### [\_\_init\_\_(self\[, acceptTables\])]{#symbol-ParseNetworkInformationTable.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-ParseNetworkInformationTable.main}
:::

::: {.section}
#### [parseTable(self, index, sections)]{#symbol-ParseNetworkInformationTable.parseTable}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ParseNetworkInformationTable.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.html){.reference}.[ParseNetworkInformationTable\_ActualAndOtherNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_ActualAndOtherNetwork.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: ParseNetworkInformationTable\_ActualAndOtherNetwork {#symbol-ParseNetworkInformationTable_ActualAndOtherNetwork}
-----------------------------------------------------------

ParseNetworkInformationTable\_ActualAndOtherNetwork() -\> new
ParseNetworkInformationTable component.

Instantiates a ParseNetworkInformationTable component configured to
parse both \'ACTUAL\' and \'OTHER\' Network tables (table ids 0x40 and
0x41)
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.html){.reference}.[ParseNetworkInformationTable\_ActualNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_ActualNetwork.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: ParseNetworkInformationTable\_ActualNetwork {#symbol-ParseNetworkInformationTable_ActualNetwork}
---------------------------------------------------

ParseNetworkInformationTable\_ActualNetwork() -\> new
ParseNetworkInformationTable component.

Instantiates a ParseNetworkInformationTable component configured to
parse \'ACTUAL\' Network tables only (table id 0x40)
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.html){.reference}.[ParseNetworkInformationTable\_OtherNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_OtherNetwork.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: ParseNetworkInformationTable\_OtherNetwork {#symbol-ParseNetworkInformationTable_OtherNetwork}
--------------------------------------------------

ParseNetworkInformationTable\_OtherNetwork() -\> new
ParseNetworkInformationTable component.

Instantiates a ParseNetworkInformationTable component configured to
parse \'OTHER\' Netowrk tables only (table id 0x41)
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
