---
pagename: Components/pydoc/Kamaelia.Device.DVB.PSITables
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[PSITables](/Components/pydoc/Kamaelia.Device.DVB.PSITables.html){.reference}
================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [FilterOutNotCurrent](/Components/pydoc/Kamaelia.Device.DVB.PSITables.FilterOutNotCurrent.html){.reference}**
:::

-   [Processing Parsed DVB PSI Tables](#478){.reference}
    -   [Selecting \'currently\' valid tables](#479){.reference}
        -   [Example Usage](#480){.reference}
        -   [Behaviour](#481){.reference}
        -   [How does it work?](#482){.reference}
:::

::: {.section}
Processing Parsed DVB PSI Tables {#478}
================================

Components for filtering and processing parsed Programme Status
Information (PSI) tables - that is the output from components in
[Kamaelia.Device.DVB.Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}

::: {.section}
[Selecting \'currently\' valid tables]{#selecting-currently-valid-tables} {#479}
-------------------------------------------------------------------------

FilterOutNotCurrent takes in parsed DVB PSI tables, but only outputs the
ones that are marked as being currently-valid. Tables that are not yet
valid are simply dropped.

NOTE: whether a table is currently-valid or not is *different* from
concepts such as present-following (now & next) used for event/programme
information. See DVB specification documents for a more detailed
explanation.

::: {.section}
### [Example Usage]{#example-usage} {#480}

Tuning to a particular broadcast multiplex and displaying the current
selection of services (channels) in the multiplex (as opposed to any
future descriptions of services that may be appearing later):

``` {.literal-block}
frequency = 505833330.0/1000000.0
feparams = {
    "inversion" : dvb3.frontend.INVERSION_AUTO,
    "constellation" : dvb3.frontend.QAM_16,
    "code_rate_HP" : dvb3.frontend.FEC_3_4,
    "code_rate_LP" : dvb3.frontend.FEC_3_4,
}

PAT_PID=0

Pipeline( DVB_Multiplex([PAT_PID], feparams),
          DVB_Demuxer({ PAT_PID:["outbox"]}),
          ReassemblePSITables(),
          ParseProgramAssociationTable(),
          FilterOutNotCurrent(),
          PrettifyProgramAssociationTable(),
          ConsoleEchoer(),
        ).run()
```
:::

::: {.section}
### [Behaviour]{#behaviour} {#481}

Send parsed DVB PSI tables to this component\'s \"inbox\" inbox. If the
table is a currently-valid one it will immediately be sent on out of the
\"outbox\" outbox.

Tables that are not-yet-valid will be ignored.

If a shutdownMicroprocess or producerFinished message is received on
this component\'s \"control\" inbox, it will be immediately sent on out
of the \"signal\" outbox and the component will terminate.
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#482}

The parsed tables you send to this component are dictionaries. This
component simply checks the value of the \'current\' key in the
dictionary.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[PSITables](/Components/pydoc/Kamaelia.Device.DVB.PSITables.html){.reference}.[FilterOutNotCurrent](/Components/pydoc/Kamaelia.Device.DVB.PSITables.FilterOutNotCurrent.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class FilterOutNotCurrent([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-FilterOutNotCurrent}
-----------------------------------------------------------------------------------------------------------

Filters out any parsed tables not labelled as currently valid

::: {.section}
### [Inboxes]{#symbol-FilterOutNotCurrent.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-FilterOutNotCurrent.Outboxes}
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
#### [main(self)]{#symbol-FilterOutNotCurrent.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-FilterOutNotCurrent.shutdown}
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
