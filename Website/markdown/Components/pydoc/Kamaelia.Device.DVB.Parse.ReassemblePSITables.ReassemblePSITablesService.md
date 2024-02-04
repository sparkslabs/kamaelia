---
pagename: Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.ReassemblePSITablesService
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}.[ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.html){.reference}.[ReassemblePSITablesService](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.ReassemblePSITablesService.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.html){.reference}

------------------------------------------------------------------------

::: {.section}
class ReassemblePSITablesService([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-ReassemblePSITablesService}
----------------------------------------------------------------------------------------------------------------------------------------------------------------------

ReassemblePSITablesService() -\> new ReassemblePSITablesService
component.

Subscribe to PSI packets by sending (\"ADD\", (component,inbox),
\[PIDs\] ) to \"request\" Unsubscribe by sending (\"REMOVE\",
(component,inbox), \[PIDs\] ) to \"request\"

::: {.section}
### [Inboxes]{#symbol-ReassemblePSITablesService.Inboxes}

-   **control** : Shutdown signalling
-   **request** : Place for subscribing/unsubscribing from different PSI
    packet streams
-   **inbox** : Incoming DVB TS packets
:::

::: {.section}
### [Outboxes]{#symbol-ReassemblePSITablesService.Outboxes}

-   **outbox** : NOT USED
-   **signal** : Shutdown signalling
-   **pid\_request** : For issuing requests for PIDs
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
#### [\_\_init\_\_(self)]{#symbol-ReassemblePSITablesService.__init__}
:::

::: {.section}
#### [handleSubscribeUnsubscribe(self, msg)]{#symbol-ReassemblePSITablesService.handleSubscribeUnsubscribe}
:::

::: {.section}
#### [main(self)]{#symbol-ReassemblePSITablesService.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ReassemblePSITablesService.shutdown}
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
