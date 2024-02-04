---
pagename: Components/pydoc/Kamaelia.Device.DVB.EIT.EITPacketParser
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[EIT](/Components/pydoc/Kamaelia.Device.DVB.EIT.html){.reference}.[EITPacketParser](/Components/pydoc/Kamaelia.Device.DVB.EIT.EITPacketParser.html){.reference}
==================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.EIT.html){.reference}

------------------------------------------------------------------------

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
