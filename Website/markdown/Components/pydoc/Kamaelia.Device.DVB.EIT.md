---
pagename: Components/pydoc/Kamaelia.Device.DVB.EIT
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[EIT](/Components/pydoc/Kamaelia.Device.DVB.EIT.html){.reference}
====================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [EITPacketParser](/Components/pydoc/Kamaelia.Device.DVB.EIT.EITPacketParser.html){.reference}**
-   **component
    [NowNextChanges](/Components/pydoc/Kamaelia.Device.DVB.EIT.NowNextChanges.html){.reference}**
-   **component
    [NowNextServiceFilter](/Components/pydoc/Kamaelia.Device.DVB.EIT.NowNextServiceFilter.html){.reference}**
-   **component
    [PSIPacketReconstructor](/Components/pydoc/Kamaelia.Device.DVB.EIT.PSIPacketReconstructor.html){.reference}**
-   **component
    [TimeAndDatePacketParser](/Components/pydoc/Kamaelia.Device.DVB.EIT.TimeAndDatePacketParser.html){.reference}**
:::
:::

::: {.section}
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[EIT](/Components/pydoc/Kamaelia.Device.DVB.EIT.html){.reference}.[EITPacketParser](/Components/pydoc/Kamaelia.Device.DVB.EIT.EITPacketParser.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class EITPacketParser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-EITPacketParser}
-------------------------------------------------------------------------------------------------------

Parses EIT packets and extracts NOW & NEXT short event descriptions for
channels within this transport stream.

(Ignores events belonging to other multiplexes)

::: {.section}
### [Inboxes]{#symbol-EITPacketParser.Inboxes}

-   **control** : NOT USED
-   **inbox** : PES packets
:::

::: {.section}
### [Outboxes]{#symbol-EITPacketParser.Outboxes}

-   **outbox** : Parsed NOW and NEXT EIT events
-   **signal** : NOT USED
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
#### [main(self)]{#symbol-EITPacketParser.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-EITPacketParser.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[EIT](/Components/pydoc/Kamaelia.Device.DVB.EIT.html){.reference}.[NowNextChanges](/Components/pydoc/Kamaelia.Device.DVB.EIT.NowNextChanges.html){.reference}
================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class NowNextChanges([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-NowNextChanges}
------------------------------------------------------------------------------------------------------

Simple attempt to filter DVB now and next info for multiple services,
such that we only send output when the data changes.

::: {.section}
### [Inboxes]{#symbol-NowNextChanges.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-NowNextChanges.Outboxes}
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
#### [main(self)]{#symbol-NowNextChanges.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-NowNextChanges.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[EIT](/Components/pydoc/Kamaelia.Device.DVB.EIT.html){.reference}.[NowNextServiceFilter](/Components/pydoc/Kamaelia.Device.DVB.EIT.NowNextServiceFilter.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class NowNextServiceFilter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-NowNextServiceFilter}
------------------------------------------------------------------------------------------------------------

Filters now/next event data for only specified services.

::: {.section}
### [Inboxes]{#symbol-NowNextServiceFilter.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-NowNextServiceFilter.Outboxes}
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
#### [\_\_init\_\_(self, \*services)]{#symbol-NowNextServiceFilter.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-NowNextServiceFilter.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-NowNextServiceFilter.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[EIT](/Components/pydoc/Kamaelia.Device.DVB.EIT.html){.reference}.[PSIPacketReconstructor](/Components/pydoc/Kamaelia.Device.DVB.EIT.PSIPacketReconstructor.html){.reference}
================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class PSIPacketReconstructor([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PSIPacketReconstructor}
--------------------------------------------------------------------------------------------------------------

Takes DVB Transport stream packets for a given PID and reconstructs the
PSI packets from within the stream.

Will only handle stream from a single PID.

::: {.section}
### [Inboxes]{#symbol-PSIPacketReconstructor.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-PSIPacketReconstructor.Outboxes}
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
#### [main(self)]{#symbol-PSIPacketReconstructor.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-PSIPacketReconstructor.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[EIT](/Components/pydoc/Kamaelia.Device.DVB.EIT.html){.reference}.[TimeAndDatePacketParser](/Components/pydoc/Kamaelia.Device.DVB.EIT.TimeAndDatePacketParser.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class TimeAndDatePacketParser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TimeAndDatePacketParser}
---------------------------------------------------------------------------------------------------------------

Parses \"Time and Date\" packets.

::: {.section}
### [Inboxes]{#symbol-TimeAndDatePacketParser.Inboxes}

-   **control** : NOT USED
-   **inbox** : PES packets
:::

::: {.section}
### [Outboxes]{#symbol-TimeAndDatePacketParser.Outboxes}

-   **outbox** : Parsed date and time
-   **signal** : NOT USED
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
#### [main(self)]{#symbol-TimeAndDatePacketParser.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-TimeAndDatePacketParser.shutdown}
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
