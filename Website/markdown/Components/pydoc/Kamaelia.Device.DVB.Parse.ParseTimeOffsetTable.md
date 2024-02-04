---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ParseTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.ParseTimeOffsetTable.html){.reference}**
:::

-   [Parsing Time Offset Tables in DVB streams](#515){.reference}
    -   [Example Usage](#516){.reference}
    -   [Behaviour](#517){.reference}
:::

::: {.section}
Parsing Time Offset Tables in DVB streams {#515}
=========================================

ParseTimeOffsetTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs the current time and date in UTC (GMT)
aswell as the current time offset, and when the next change will be (due
to daylight saving).

The purpose of the TOT and details of the fields within in are defined
in the DVB SI specification, including the possible \'descriptor\'
fields that feature in the table:

-   ETSI EN 300 468 \"Digital Video Broadcasting (DVB); Specification
    for Service Information (SI) in DVB systems\" ETSI / EBU (DVB group)

::: {.section}
[Example Usage]{#example-usage} {#516}
-------------------------------

A simple pipeline to receive, parse and display the Time Offset Table:

``` {.literal-block}
FREQUENCY = 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

TOT_PID = 0x14

Pipeline( DVB_Multiplex(FREQUENCY, [TOT_PID], feparams),
          DVB_Demuxer({ TOT_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseTimeOffsetDateTable(),
          PrettifyTimeOffsetDateTable(),
          ConsoleEchoer(),
        ).run()
```
:::

::: {.section}
[Behaviour]{#behaviour} {#517}
-----------------------

Send reconstructed PSI table \'sections\' to the \"inbox\" inbox. When
all sections of the table have arrived, ParseTimeOffsetTable will parse
the table and send it out of its \"outbox\" outbox.

The table is output every time it is received. In practice a multiplex
is likely to transmit about 1 instance of this table per second, giving
a reasonably accurate measure of the current time.

The parsed table is sent out as a dictionary data structure, similar to
this:

``` {.literal-block}
{
    'table_type' : 'TOT',
    'country'    : 'GBR'
    'region'     : 0,
    'offset'     : (0, 0),
    'next'       : { 'when'  : [2007, 3, 25, 1, 0, 0],
                     'offset': (1, 0)
                   },
    'UTC_now'    : [2006, 12, 21, 16, 16, 8],
}
```

If this data is sent on through a PrettifyTimeOffsetTable component,
then the equivalent output is a string of the following form:

``` {.literal-block}
TOT received:
   DateTime now (UTC)         : 2006-12-21 16:16:08
   Current local offset (h,m) : 00:00
   Country & region in it     : GBR (0)
   Next change of offset:
       Changes to             : 01:00
       Changes on (y,m,d)     : 2007-03-25 01:00:00
```

Note that this not only includes the current date, time, location and
offset from UTC (GMT), but it also tells you when the next change of
offset will happen (due to Daylight Saving time) and what that new
offset will be.

The above example output shows that it is currently 21st December 2006
16:16:08 GMT but that at 1am on 25th March 2007 it will change to
GMT+0100.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.html){.reference}.[ParseTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.ParseTimeOffsetTable.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ParseTimeOffsetTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ParseTimeOffsetTable}
------------------------------------------------------------------------------------------------------------

Parses a TOT table.

Receives table sections from PSI packets. Outputs the current time and
date (UTC) and time zone offset.

::: {.section}
### [Inboxes]{#symbol-ParseTimeOffsetTable.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : DVB PSI Packets from a single PID containing a TOT table
:::

::: {.section}
### [Outboxes]{#symbol-ParseTimeOffsetTable.Outboxes}

-   **outbox** : Current date and time (UTC) and time zone offset
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
#### [\_\_init\_\_(self)]{#symbol-ParseTimeOffsetTable.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-ParseTimeOffsetTable.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ParseTimeOffsetTable.shutdown}
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
