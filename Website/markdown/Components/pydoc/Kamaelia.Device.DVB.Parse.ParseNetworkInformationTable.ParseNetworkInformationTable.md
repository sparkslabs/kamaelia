---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.html){.reference}.[ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable.html){.reference}
=========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.html){.reference}

------------------------------------------------------------------------

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
