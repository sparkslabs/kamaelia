---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ParseTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable.ParseTimeAndDateTable.html){.reference}**
:::

-   [Parsing Time And Date Tables in DVB streams](#484){.reference}
    -   [Example Usage](#485){.reference}
    -   [Behaviour](#486){.reference}
:::

::: {.section}
Parsing Time And Date Tables in DVB streams {#484}
===========================================

ParseTimeAndDateTable parses a reconstructed PSI table from a DVB MPEG
Transport Stream, and outputs the current time and date in UTC (GMT).

The purpose of the TDT and details of the fields within in are defined
in the DVB SI specification:

-   ETSI EN 300 468 \"Digital Video Broadcasting (DVB); Specification
    for Service Information (SI) in DVB systems\" ETSI / EBU (DVB group)

The Time Offset Table (TOT) additionally contains information on the
current (and next) timezone offset that applies, as well as duplicating
the datetime information. See ParseTimeOffsetTable component.

::: {.section}
[Example Usage]{#example-usage} {#485}
-------------------------------

A simple pipeline to receive, parse and display the Time and Date Table:

``` {.literal-block}
FREQUENCY = 505.833330
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

TDT_PID = 0x14

Pipeline( DVB_Multiplex(FREQUENCY, [TDT_PID], feparams),
          DVB_Demuxer({ TDT_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseTimeAndDateTable(),
          PrettifyTimeAndDateTable(),
          ConsoleEchoer(),
        ).run()
```

The output will look like this:

``` {.literal-block}
[2006, 12, 21, 15, 1, 3]
[2006, 12, 21, 15, 1, 4]
[2006, 12, 21, 15, 1, 5]
[2006, 12, 21, 15, 1, 6]

.....
```
:::

::: {.section}
[Behaviour]{#behaviour} {#486}
-----------------------

Send reconstructed PSI table \'sections\' to the \"inbox\" inbox. When
all sections of the table have arrived, ParseServiceDescriptionTable
will parse the table and send it out of its \"outbox\" outbox.

The table is output every time it is received. In practice a multiplex
is likely to transmit about 1 instance of this table per second, giving
a reasonably accurate measure of the current time.

The value output is a simple list/tuple describing the current UTC (GMT)
date and time, in the form (year,month,day,hour,minute,second).

For example: 21st December 2006 15:01:03 GMT is represented as:

``` {.literal-block}
[2006, 12, 21, 15, 1, 3]
```

If this data is sent on through a PrettifyTimeAndDateTable component,
then the equivalent output is a string of the following form:

``` {.literal-block}
TDT received:
   UTC Date now (y,m,d) : 2006 12 21
   UTC Time now (h,m,s) : 15:01:03
```

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox, then it will immediately be sent on out of the
\"signal\" outbox and the component will then immediately terminate.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable.html){.reference}.[ParseTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable.ParseTimeAndDateTable.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class ParseTimeAndDateTable([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ParseTimeAndDateTable}
-------------------------------------------------------------------------------------------------------------

ParseTimeAndDateTable() -\> new ParseTimeAndDateTable component.

Send reconstructed PSI table sections to the \"inbox\" inbox. When a
complete table is assembled and parsed, the result is sent out of the
\"outbox\" outbox in the form \[year,month,day,hour,minute,second\]. The
times are UTC (GMT).

::: {.section}
### [Inboxes]{#symbol-ParseTimeAndDateTable.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : DVB PSI Packets from a single PID containing a TDT table
:::

::: {.section}
### [Outboxes]{#symbol-ParseTimeAndDateTable.Outboxes}

-   **outbox** : Current date and time (UTC)
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
#### [\_\_init\_\_(self)]{#symbol-ParseTimeAndDateTable.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-ParseTimeAndDateTable.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ParseTimeAndDateTable.shutdown}
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
