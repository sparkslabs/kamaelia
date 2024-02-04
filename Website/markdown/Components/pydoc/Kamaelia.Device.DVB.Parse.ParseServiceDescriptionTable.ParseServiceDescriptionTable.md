---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.html){.reference}.[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable.html){.reference}
=========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.html){.reference}

------------------------------------------------------------------------

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
