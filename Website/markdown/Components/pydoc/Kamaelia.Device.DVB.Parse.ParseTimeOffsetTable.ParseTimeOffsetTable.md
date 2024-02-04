---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.ParseTimeOffsetTable
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.html){.reference}.[ParseTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.ParseTimeOffsetTable.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.html){.reference}

------------------------------------------------------------------------

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
